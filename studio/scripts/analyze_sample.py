#!/usr/bin/env python3
import argparse,json,statistics
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
source=Path(__file__).resolve().parents[1]/'examples/research-data.json'
data=json.loads(source.read_text())
result={'source':data['source'],'synthetic':True,'unit':data['unit'],'groups':{}}
for key in ('control','assisted'):
 values=data[key]
 result['groups'][key]={'n':len(values),'median':statistics.median(values),'mean':statistics.mean(values),'min':min(values),'max':max(values),'sum':sum(values),'values':values}
m1,m2=(result['groups'][key]['median'] for key in ('control','assisted'))
result['median_difference']=m1-m2;result['relative_difference']=(m1-m2)/m1
out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(out)
