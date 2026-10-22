#!/usr/bin/env python3
"""Master-prompt proof: base decks plus analytical deck, calculated XLSX, DOCX/PDF and seeded QA."""
import argparse,json,os,re,subprocess,sys,zipfile
from datetime import datetime,timezone
from pathlib import Path
import xml.etree.ElementTree as ET
from qa import deck,evidence
from qa_office import evaluate_workbook,document

ROOT=Path(__file__).resolve().parents[2];S=ROOT/'studio/scripts'

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='work/full-tests');p.add_argument('--base-out',default='work/acceptance');a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    def run(cmd,env=None):
        r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=300)
        if r.returncode:raise RuntimeError(r.stdout[-3000:]+r.stderr[-3000:])
        return r
    basepath=Path(a.base_out).resolve()
    base=run([sys.executable,str(S/'acceptance.py'),'--out',str(basepath)]);(out/'base-run.txt').write_text(base.stdout)
    base_result=json.loads((basepath/'acceptance.json').read_text())
    if any(check['status']=='FAIL' for check in base_result['checks']):raise RuntimeError('A base acceptance check failed')
    fonts=ROOT/'work/fonts'
    r=run([sys.executable,'scripts/install_fonts.py','--install','--family','inter','--family','lora','--static','--dest',str(fonts)])
    (out/'font-install.txt').write_text(r.stdout)
    env=os.environ.copy();env['FONTCONFIG_FILE']=str(fonts/'fontconfig.xml')
    env['STUDIO_RESEARCH_FONT']='Inter';env['STUDIO_RESEARCH_SERIF']='Lora'
    def guard(stage,inputs,outputs,cmd,usefonts=False):
        c=[sys.executable,str(S/'run_guard.py'),'--state-dir',str(out/'state'),'--stage',stage,'--timeout','240']
        for f in inputs:c+=['--input',str(f)]
        for f in outputs:c+=['--output',str(f)]
        result=run(c+['--']+cmd,env if usefonts else None);print(result.stdout.strip())
    data=ROOT/'studio/examples/research-data.json';analysis=out/'analysis.json';fontmanifest=fonts/'installed.json'
    guard('analysis',[data,S/'analyze_sample.py'],[analysis],[sys.executable,str(S/'analyze_sample.py'),'--out',str(analysis)])
    pptx=out/'04-research.pptx';render=out/'rendered/04-research'
    guard('research-build',[analysis,S/'build-research.cjs',ROOT/'studio/package-lock.json'],[pptx],['node',str(S/'build-research.cjs'),str(analysis),str(pptx)],True)
    guard('research-render',[pptx,ROOT/'scripts/render_decks.py',fontmanifest,fonts/'fontconfig.xml'],[render/'04-research.pdf',render/'contact-sheet.png']+[render/f'slide-{i}.png' for i in range(1,7)],[sys.executable,'scripts/render_decks.py',str(pptx),'--out',str(out/'rendered')],True)
    guard('office-build',[data,analysis,S/'office_sample.py'],[out/'research-workbook.xlsx',out/'research-note.docx',out/'observations.png'],[sys.executable,str(S/'office_sample.py'),'--analysis',str(analysis),'--out',str(out)])
    calc=out/'recalculated/research-workbook.xlsx'
    guard('xlsx-recalc',[out/'research-workbook.xlsx',S/'office_export.py',fontmanifest],[calc,out/'recalculated/export.json'],[sys.executable,str(S/'office_export.py'),str(out/'research-workbook.xlsx'),'--to','xlsx','--out',str(out/'recalculated')],True)
    for name,source in [('word-preview',out/'research-note.docx'),('excel-preview',calc)]:
        target=out/name
        guard(name,[source,S/'office_export.py',fontmanifest],[target/(source.stem+'.pdf'),target/'contact-sheet.png']+[target/f'page-{i:02}.png' for i in range(1,4)],[sys.executable,str(S/'office_export.py'),str(source),'--out',str(target)],True)
    qa_results={
      'research':deck(pptx,render/'04-research.pdf'),
      'xlsx':evaluate_workbook(calc,json.loads(data.read_text())),
      'docx':document(out/'research-note.docx',out/'word-preview/research-note.pdf')}
    ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
    with zipfile.ZipFile(pptx) as z:
        xml=ET.fromstring(z.read('ppt/charts/chart1.xml'))
        values=[float(v.text) for v in xml.findall('.//c:ser/c:val/c:numRef/c:numCache/c:pt/c:v',ns)]
    raw_source=json.loads(data.read_text())
    expected=[(sorted(raw_source[key])[2]+sorted(raw_source[key])[3])/2 for key in ['control','assisted']]
    qa_results['research_chart_source']={'status':'PASS' if values==expected else 'FAIL','expected':expected,'actual':values}
    for key,result in qa_results.items():
        (out/(key+'-qa.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
        if result['status']!='PASS':raise RuntimeError(key+' failed final artifact audit')
    seed=out/'seeded';seed.mkdir(exist_ok=True)
    guard('seed-build',[S/'create_seeded_qa.py'],[seed/'error-seeded.pptx',seed/'error-seeded.json'],[sys.executable,str(S/'create_seeded_qa.py'),'--out',str(seed)])
    guard('seed-render',[seed/'error-seeded.pptx',S/'render.py'],[seed/'rendered/error-seeded.pdf',seed/'rendered/slide-01.png',seed/'rendered/contact-sheet.png'],[sys.executable,str(S/'render.py'),str(seed/'error-seeded.pptx'),'--out',str(seed/'rendered')])
    seeded_evidence=evidence(json.loads((seed/'error-seeded.json').read_text()));seeded_deck=deck(seed/'error-seeded.pptx',seed/'rendered/error-seeded.pdf')
    codes={f['code'] for r in [seeded_evidence,seeded_deck] for f in r['findings']}
    required={'UNSUPPORTED_CLAIM','INCONSISTENT_NUMBER','WEAK_REFERENCE','PDF_TEXT_LOSS'}
    seed_result={'status':'PASS' if required<=codes else 'FAIL','expected_failure':True,'required_detected':sorted(required&codes),'evidence':seeded_evidence,'overflow':seeded_deck}
    (seed/'qa-result.json').write_text(json.dumps(seed_result,ensure_ascii=False,indent=2))
    if seed_result['status']!='PASS':raise RuntimeError('Seeded defects were missed')
    # Mutation: change the median range while retaining the former Excel cached result.
    bad=seed/'wrong-range.xlsx'
    with zipfile.ZipFile(calc) as zin,zipfile.ZipFile(bad,'w',zipfile.ZIP_DEFLATED) as zout:
        changed=False
        for item in zin.infolist():
            payload=zin.read(item.filename)
            if item.filename.startswith('xl/worksheets/') and item.filename.endswith('.xml'):
                if b'MEDIAN(Raw!B2:B7)' in payload:payload=payload.replace(b'MEDIAN(Raw!B2:B7)',b'MEDIAN(Raw!B2:B6)',1);changed=True
            zout.writestr(item,payload)
    if not changed:raise RuntimeError('Wrong-range mutation was not injected')
    badresult=evaluate_workbook(bad,json.loads(data.read_text()));(seed/'wrong-range-qa.json').write_text(json.dumps(badresult,ensure_ascii=False,indent=2))
    if badresult['status']!='FAIL':raise RuntimeError('Wrong-range mutation was missed')
    result={'date':'2026-10-22','run_at_utc':datetime.now(timezone.utc).isoformat(),'overall':'WARN','automated_checks':'PASS','required_deck_genres':['executive','brand','research'],'bonus_deck':'pitch','presentation_slides':24,'office_formula_count':len(qa_results['xlsx']['formulas']),'word_pages':qa_results['docx']['pages'],'checks':[{'name':'Analytical PPTX + chart/data + render','status':'PASS'},{'name':'Editable Excel, source ranges and recalculated caches','status':'PASS'},{'name':'Editable DOCX, actual pagination and PDF text','status':'PASS'},{'name':'Unsupported / wrong number / weak reference / overflow seeded test','status':'PASS'},{'name':'Wrong Excel formula-range mutation','status':'PASS'},{'name':'Failure recovery (base tests)','status':'PASS'},{'name':'Separate model/person semantic reviewer','status':'NOT TESTED'},{'name':'Automatic runtime skill activation','status':'NOT TESTED'},{'name':'Portfolio images at full resolution','status':'WARN'}],'manual_review':'Required after any changed render; see frozen author-review manifest','independent_model_or_person':False}
    result['presentation_slides']=base_result['slide_count']+len(qa_results['research']['slides'])
    result['base_checks']=base_result['checks']
    (out/'full-acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
