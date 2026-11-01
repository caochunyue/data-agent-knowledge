"""Validate provenance fields and local Markdown targets (no network requests)."""
import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES={'数据研发','资产检索答疑','数据分析','数据agent'}
REQUIRED={'id','title','publisher','published_date','url','read_status','primary_category','tags','summary'}
STATES={'read','read_relevant_sections','title_only','blocked','unavailable'}
def validate_records(records):
    errors=[]; ids=set(); urls=set()
    for n,row in enumerate(records):
        missing=REQUIRED-set(row)
        if missing: errors.append(f'{n}: missing {sorted(missing)}')
        if row.get('id') in ids: errors.append(f'{n}: duplicate id')
        if row.get('url') in urls: errors.append(f'{n}: duplicate URL')
        ids.add(row.get('id')); urls.add(row.get('url'))
        if row.get('primary_category') not in CATEGORIES: errors.append(f'{n}: category')
        if row.get('read_status') not in STATES: errors.append(f'{n}: reading status')
        if not isinstance(row.get('tags'),list): errors.append(f'{n}: tags')
        url=row.get('url','')
        parsed=urlsplit(url)
        if parsed.scheme!='https' or not parsed.netloc: errors.append(f'{n}: URL')
        date=row.get('published_date')
        if date is None:
            if not row.get('date_note'): errors.append(f'{n}: unknown date without note')
        else:
            try: datetime.date.fromisoformat(date)
            except (ValueError,TypeError): errors.append(f'{n}: invalid date')
        if row.get('read_status')=='read' and not row.get('reading_evidence'):
            errors.append(f'{n}: full read without evidence')
    return errors

def validate_links():
    errors=[]
    for p in ROOT.rglob('*.md'):
        if '.venv' in p.parts or '.git' in p.parts: continue
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('https://','http://','#','mailto:')): continue
            local=unquote(target.split('#')[0])
            if local and not (p.parent/local).exists(): errors.append(f'{p.relative_to(ROOT)}: {target}')
    return errors
if __name__=='__main__':
    errors=[]
    for filename in ('references.json','wechat-articles.json','public-articles.json'):
        errors.extend(validate_records(json.loads((ROOT/'sources'/filename).read_text())))
    errors.extend(validate_links())
    report={'status':'fail' if errors else 'pass','errors':errors,'checks':'source fields, dates, categories, duplicate IDs/URLs, local Markdown targets; remote link reachability not checked'}
    (ROOT/'reports/index-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
