"""Run development regression cases; never grade model intelligence."""
import json, platform, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples'))
from lab import Harness

def main():
    cases=json.loads((ROOT/'evals/cases.json').read_text())
    counts=Counter(c['group'] for c in cases)
    assert len({c['id'] for c in cases})==len(cases)
    assert len(counts)==4 and all(v>=10 for v in counts.values())
    results=[]; traces=[]
    for c in cases:
        h=Harness(budget=c['action'].get('_budget',5))
        result=h.call(c['action'])
        passed=all(result.get(k)==v for k,v in c['expected'].items())
        results.append({'id':c['id'],'group':c['group'],'name':c['name'],'passed':passed,'expected':c['expected'],'actual':result})
        traces.append({'case_id':c['id'],'events':h.trace})
        assert Harness.replay(h.trace)==[result]
        h.db.close()
    report={'suite':'deterministic-development-regression','python':platform.python_version(),'total':len(results),'passed':sum(x['passed'] for x in results),'groups':dict(counts),'model_evaluated':False,'replay_verified':True,'results':results}
    (ROOT/'reports/evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'reports/traces.json').write_text(json.dumps(traces,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2))
    return int(report['passed']!=report['total'])
if __name__=='__main__': raise SystemExit(main())
