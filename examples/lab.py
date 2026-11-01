"""Deterministic tool harness; no model, network, shell, or production data."""
import copy
import hashlib
import json
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Harness:
    ALLOWED = {'sql', 'search', 'metric', 'entity', 'relationship'}

    def __init__(self, budget=5, row_limit=100, vm_steps=100000):
        if type(budget) is not int or budget < 0 or any(type(x) is not int or x <= 0 for x in (row_limit, vm_steps)):
            raise ValueError('budget must be nonnegative; row_limit and vm_steps must be positive integers')
        self.budget, self.row_limit, self.vm_steps = budget, row_limit, vm_steps
        self.trace = []
        loaded = {f: (ROOT / ('examples/'+f)).read_bytes() for f in ('seed.sql','model.json','catalog.json')}
        self.snapshot_sha256 = hashlib.sha256(b''.join(loaded.values())).hexdigest()
        self.model = json.loads(loaded['model.json'])
        self.catalog = json.loads(loaded['catalog.json'])
        self.db = sqlite3.connect(':memory:')
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript(loaded['seed.sql'].decode('utf-8'))
        self.db.execute('PRAGMA query_only=ON')
        if hasattr(self.db, "enable_load_extension"):
            self.db.enable_load_extension(False)
        # This is a demo SQL boundary, not OS isolation or tenant authorization.
        def authorize(op, arg1, arg2, dbname, trigger):
            if op in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_RECURSIVE):
                return sqlite3.SQLITE_OK
            if op == sqlite3.SQLITE_READ and arg1 in ('orders', 'customers'):
                return sqlite3.SQLITE_OK
            if op == sqlite3.SQLITE_FUNCTION and (arg2 or '').lower() in (
                'sum', 'count', 'coalesce', 'min', 'max', 'avg'):
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        self.db.set_authorizer(authorize)

    def _sql(self, sql, params=()):
        if not isinstance(sql, str) or not sql.lstrip().lower().startswith(('select ', 'with ')):
            return {'status': 'error', 'error': 'not_read_only'}
        remaining = self.vm_steps
        def progress():
            nonlocal remaining
            remaining -= 100
            return int(remaining <= 0)
        self.db.set_progress_handler(progress, 100)
        try:
            rows = self.db.execute(sql, params).fetchmany(self.row_limit + 1)
            if len(rows) > self.row_limit:
                return {'status': 'error', 'error': 'row_limit'}
            return {'status': 'ok', 'value': [list(row) for row in rows]}
        except (sqlite3.Error, sqlite3.Warning) as exc:
            return {'status': 'error', 'error': 'execution_budget' if 'interrupt' in str(exc) else 'sql_error'}
        finally:
            self.db.set_progress_handler(None, 0)

    def _dispatch(self, a):
        tool = a.get('tool')
        if tool not in self.ALLOWED:
            return {'status': 'error', 'error': 'tool_denied'}
        if tool == 'sql':
            return self._sql(a.get('sql'))
        if tool == 'search':
            query = a.get('query', '')
            if not isinstance(query, str):
                return {'status': 'error', 'error': 'invalid_input'}
            query = query.strip().lower()
            hits = [x for x in self.catalog if query and query in [t.lower() for t in x['terms']]]
            return {'status': 'ok', 'ids': [x['id'] for x in hits], 'sources': [x['source'] for x in hits], 'assets': hits}
        if tool == 'metric':
            metric = self.model['metrics'].get(a.get('name', ''))
            if metric is None:
                return {'status': 'clarify', 'question': '请指定已批准指标：paid_revenue 或 paid_order_count；其他口径需先确认。'}
            result = self._sql(metric['sql'])
            if result['status'] != 'ok':
                return result
            return {'status': 'ok', 'value': result['value'][0][0], 'source': metric['source'], 'definition': metric['definition'], 'unit': self.model['unit'] if a['name']=='paid_revenue' else 'orders'}
        tenant = a.get('tenant_id')
        key = a.get('customer_id' if tool=='entity' else 'order_id')
        if not tenant or not key:
            return {'status': 'clarify', 'question': '请提供 tenant_id 和完整业务标识。'}
        if tool == 'entity':
            result = self._sql('SELECT name,email FROM customers WHERE tenant_id=? AND customer_id=?', (tenant,key))
            if result['status'] != 'ok': return result
            if not result['value']: return {'status': 'not_found'}
            return {'status': 'ok', 'identity': [tenant,key], 'name': result['value'][0][0], 'email': result['value'][0][1], 'source': 'examples/seed.sql#customers'}
        result = self._sql('SELECT customer_id FROM orders WHERE tenant_id=? AND order_id=?', (tenant,key))
        if result['status'] != 'ok': return result
        if not result['value']: return {'status': 'not_found'}
        mapping = self.model['mapping']
        if mapping['status'] != 'approved': return {'status': 'error','error':'mapping_not_approved'}
        return {'status': 'ok', 'subject': [tenant,key], 'predicate': mapping['relationship'], 'object': [tenant,result['value'][0][0]], 'evidence': mapping['evidence'], 'mapping_version': mapping['version']}

    def call(self, action):
        before = self.budget
        started = time.monotonic()
        if before <= 0:
            result = {'status': 'error', 'error': 'budget_exhausted'}
        else:
            self.budget -= 1
            try:
                result = self._dispatch(action) if isinstance(action, dict) else {'status':'error','error':'invalid_input'}
            except (TypeError, ValueError, KeyError):
                result = {'status':'error','error':'invalid_input'}
        self.trace.append({'input':copy.deepcopy(action),'output':copy.deepcopy(result),'budget_before':before,'row_limit':self.row_limit,'vm_steps':self.vm_steps,'snapshot_sha256':self.snapshot_sha256,'elapsed_ms':round((time.monotonic()-started)*1000,3)})
        return result

    @staticmethod
    def replay(trace):
        if not trace:
            return []
        first = trace[0]
        h = Harness(budget=first['budget_before'], row_limit=first['row_limit'], vm_steps=first['vm_steps'])
        outputs = []
        try:
            for event in trace:
                if h.budget != event['budget_before']:
                    raise ValueError('discontinuous budget')
                if h.row_limit != event['row_limit'] or h.vm_steps != event['vm_steps']:
                    raise ValueError('configuration mismatch')
                if h.snapshot_sha256 != event['snapshot_sha256']:
                    raise ValueError('snapshot mismatch')
                outputs.append(h.call(event['input']))
            return outputs
        finally:
            h.db.close()

if __name__ == '__main__':
    import sys
    h=Harness()
    action=json.loads(sys.argv[1]) if len(sys.argv)>1 else {'tool':'metric','name':'paid_revenue'}
    print(json.dumps(h.call(action),ensure_ascii=False,indent=2))
