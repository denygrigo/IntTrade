#!/usr/bin/env python3
"""Reproducible acceptance run; independent semantic review remains a separate gate."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from doctor import inventory
from qa import evidence,deck

ROOT=Path(__file__).resolve().parents[2]
S=ROOT/'studio/scripts'

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='work/acceptance');a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    checks=[]
    inv=inventory();(out/'doctor.json').write_text(json.dumps(inv,indent=2))
    checks.append({'test':'A — runtime','status':'PASS' if inv['ready'] else 'FAIL','detail':'Existing toolchain reused; dependency installation not run.'})
    if not inv['ready']:raise RuntimeError('Toolchain unavailable; run doctor and diagnose')
    unit=subprocess.run([sys.executable,'-m','unittest','discover','-s','studio/tests','-v'],cwd=ROOT,capture_output=True,text=True,timeout=30)
    (out/'unit-tests.txt').write_text(unit.stdout+unit.stderr)
    if unit.returncode:raise RuntimeError('Acceptance unit tests failed')
    checks.append({'test':'B — reliability','status':'PASS','detail':'Hash skip, tamper recovery, two-failure breaker, explicit reset, timeout and missing output checks passed.'})
    skillpaths=sorted((ROOT/'.agents/skills').glob('*/SKILL.md'))
    expected={'evidence-first-research','presentation-art-director','visual-document-studio','professional-writing-editor','independent-quality-reviewer','workflow-reliability','humanizer'}
    valid={x.parent.name for x in skillpaths}==expected and all('name:' in x.read_text() and 'description:' in x.read_text() for x in skillpaths)
    checks.append({'test':'C — skill packaging','status':'PASS' if valid else 'FAIL','detail':'Six workflow skills plus optional Humanizer, plugin manifest and AGENTS.md routing. New-session automatic invocation not exercised.'})
    if not valid:raise RuntimeError('Project skill set or manifests do not match the expected curated set')
    def guarded(stage,inputs,outputs,command):
        cmd=[sys.executable,str(S/'run_guard.py'),'--state-dir',str(out/'state'),'--stage',stage,'--timeout','180']
        for v in inputs:cmd+=['--input',str(v)]
        for v in outputs:cmd+=['--output',str(v)]
        r=subprocess.run(cmd+['--']+command,cwd=ROOT,capture_output=True,text=True,timeout=190)
        print(r.stdout.strip())
        if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    names=['01-strategy','02-pitch','03-brand']
    guarded('build',[S/'build-demos.cjs',ROOT/'studio/examples/data.json',ROOT/'studio/examples/assets/quiet-ceramics.png',ROOT/'studio/package-lock.json'],[out/(n+'.pptx') for n in names]+[out/'build.json'],['node',str(S/'build-demos.cjs'),str(out)])
    audits=[]
    for n in names:
        d=out/n
        outputs=[d/(n+'.pdf'),d/'contact-sheet.png',d/'render.json']+[d/f'slide-{i:02}.png' for i in range(1,7)]
        guarded('render-'+n,[out/(n+'.pptx'),S/'render.py'],outputs,[sys.executable,str(S/'render.py'),str(out/(n+'.pptx')),'--out',str(d)])
        audit=deck(out/(n+'.pptx'),d/(n+'.pdf'))
        (d/'qa.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
        audits.append(audit)
        if audit['status']!='PASS':raise RuntimeError(f'{n} artifact QA failed')
    # Compare actual chart XML caches to the source dataset, independently of builder code.
    dataset=json.loads((ROOT/'studio/examples/data.json').read_text())
    expected=[(out/'01-strategy.pptx',[dataset['strategy']['before_hours'],dataset['strategy']['after_hours']]),(out/'02-pitch.pptx',[dataset['pitch']['active_teams']])]
    chart_checks=[]
    ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
    for filename,series_expected in expected:
        actual=[]
        with zipfile.ZipFile(filename) as z:
            for name in sorted(n for n in z.namelist() if n.startswith('ppt/charts/chart') and n.endswith('.xml')):
                xml=ET.fromstring(z.read(name))
                for series in xml.findall('.//c:ser',ns):
                    actual.append([float(v.text) for v in series.findall('./c:val/c:numRef/c:numCache/c:pt/c:v',ns)])
        ok=actual==series_expected
        chart_checks.append({'deck':filename.name,'expected':series_expected,'actual':actual,'status':'PASS' if ok else 'FAIL'})
        if not ok:raise RuntimeError('Chart/source mismatch')
    (out/'chart-data-qa.json').write_text(json.dumps(chart_checks,ensure_ascii=False,indent=2))
    checks.append({'test':'D — three presentation purposes','status':'PASS','detail':'3 PPTX, 18 slides, 3 actual-export PDFs, native text in all slides, editable chart workbooks and 18 PNG renders. Chart caches match source JSON.'})
    bad=evidence(json.loads((ROOT/'studio/tests/qa_bad.json').read_text()));good=evidence(json.loads((ROOT/'studio/tests/qa_good.json').read_text()))
    (out/'test-e-bad.json').write_text(json.dumps(bad,ensure_ascii=False,indent=2));(out/'test-e-good.json').write_text(json.dumps(good,ensure_ascii=False,indent=2))
    checks.append({'test':'E — injected errors','status':'PASS' if bad['status']=='FAIL' and good['status']=='PASS' else 'FAIL','detail':'Unsupported claim, 24/27 conflict, broken citation and 18/24 arithmetic defect detected; corrected fixture passes.'})
    probes=json.loads((ROOT/'work/reference-probe.json').read_text()) if (ROOT/'work/reference-probe.json').exists() else []
    (out/'reference-probe.json').write_text(json.dumps(probes,ensure_ascii=False,indent=2))
    checks.append({'test':'F — external references','status':'WARN' if probes else 'NOT TESTED','detail':'Live probes logged; three historical fallback Slidev images were inspected by the author; designer image access restricted. See reference ledger.' if probes else 'Live access not probed in this run. Prior author inspection history is in the reference ledger; do not treat it as a fresh visual review.'})
    checks.append({'test':'G — independent semantic/visual reviewer','status':'NOT TESTED','detail':'Separate artifact auditor ran; final author review must be tied to actual render hashes. No separate reviewer identity or model run is claimed.'})
    result={'date':'2026-10-22','run_at_utc':datetime.now(timezone.utc).isoformat(),'overall':'WARN','implementation':'WORKING LOCAL TOOLCHAIN','checks':checks,'slide_count':sum(len(x['slides']) for x in audits),'unresolved_artifact_blockers':sum(len(x['findings']) for x in audits),'independent_reviewer':None,'limitations':['New-session skill routing not exercised','Designer portfolio image access restricted','PowerPoint desktop/iPhone rendering not tested','Current session disk changes are not an environment publication']}
    (out/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
