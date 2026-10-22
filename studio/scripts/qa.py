#!/usr/bin/env python3
"""Separate artifact/provenance auditor. No builder imports and no semantic PASS claim."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS={"a":"http://schemas.openxmlformats.org/drawingml/2006/main","p":"http://schemas.openxmlformats.org/presentationml/2006/main"}

def issue(code,message,**extra): return {"severity":"blocking","code":code,"message":message,**extra}

def evidence(data):
    findings=[]; sources={}; values=defaultdict(set)
    for source in data.get("sources",[]):
        sid=source.get("id")
        if not sid or sid in sources: findings.append(issue("SOURCE_ID","Missing or duplicate source ID",source=sid))
        sources[sid]=source
        for field in ("url","title","publisher","accessed","locator","support"):
            if not source.get(field): findings.append(issue("SOURCE_FIELD",f"Missing {field}",source=sid))
        if not str(source.get("url","")).startswith(("https://","http://","file:")):
            findings.append(issue("SOURCE_URL","Invalid source URL",source=sid))
        if source.get("access_state") not in ("opened","local_dataset"):
            findings.append(issue("SOURCE_NOT_OPENED","Source not opened",source=sid))
    claims=data.get("claims",[])
    if not claims: findings.append(issue("NO_CLAIMS","Empty claim ledger cannot pass research QA"))
    for c in claims:
        cid=c.get("id"); kind=c.get("kind","fact")
        if not c.get("text"): findings.append(issue("CLAIM_TEXT","Missing claim text",claim=cid))
        if kind in ("fact","synthetic"):
            if not c.get("source_ids"): findings.append(issue("UNSUPPORTED_CLAIM","No supporting source",claim=cid))
            for sid in c.get("source_ids",[]):
                if sid not in sources: findings.append(issue("BROKEN_SOURCE",f"Unknown source {sid}",claim=cid))
            if kind=="synthetic" and not c.get("disclosure"):
                findings.append(issue("UNLABELLED_DEMO","Synthetic data needs visible disclosure",claim=cid))
        elif kind not in ("inference","recommendation","forecast","calculation"):
            findings.append(issue("CLAIM_KIND","Unknown claim kind",claim=cid))
        elif not c.get("basis"):
            findings.append(issue("CLAIM_BASIS","Non-factual claim needs basis",claim=cid))
        if "value" in c:
            for field in ("metric","unit","period","geography","scope"):
                if not c.get(field): findings.append(issue("METRIC_SCOPE",f"Missing {field}",claim=cid))
            if isinstance(c["value"],bool) or not isinstance(c["value"],(int,float)) or not math.isfinite(c["value"]):
                findings.append(issue("METRIC_VALUE","Value must be a finite number",claim=cid))
                continue
            key=tuple(c.get(f) for f in ("metric","unit","period","geography","scope"))
            values[key].add(c["value"])
    for key,nums in values.items():
        if len(nums)>1: findings.append(issue("INCONSISTENT_NUMBER",f"Same metric/scope has conflicting values: {sorted(nums)}",metric=key))
    for calc in data.get("calculations",[]):
        try:
            a,b=calc["inputs"]
            computed={"sum":lambda:a+b,"ratio":lambda:a/b,"change_pct":lambda:(b-a)/a*100,"reduction_pct":lambda:(a-b)/a*100}[calc["operation"]]()
            if not math.isfinite(computed) or not math.isclose(computed,calc["result"],abs_tol=calc.get("tolerance",0.01)):
                findings.append(issue("CALCULATION",f"Expected {computed:g}; recorded {calc['result']}",calculation=calc.get("id")))
        except (KeyError,ValueError,TypeError,ZeroDivisionError):
            findings.append(issue("CALCULATION_FORMAT","Invalid calculation",calculation=calc.get("id")))
    return {"status":"FAIL" if findings else "PASS","scope":"Structured provenance and numeric consistency only; source entailment requires semantic review","claims":len(claims),"sources":len(sources),"findings":findings}

def norm(s): return re.sub(r"\W+","",s.lower(),flags=re.UNICODE)

def deck(pptx,pdf=None):
    findings=[];slides=[]
    try:
        with zipfile.ZipFile(pptx) as z:
            corrupt=z.testzip()
            if corrupt: return {"status":"FAIL","findings":[issue("ZIP_CRC",corrupt)]}
            pres=ET.fromstring(z.read("ppt/presentation.xml"));sz=pres.find("p:sldSz",NS)
            width,height=int(sz.get("cx")),int(sz.get("cy"))
            names=sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml",n)],key=lambda n:int(re.search(r"slide(\d+)",n).group(1)))
            for idx,name in enumerate(names,1):
                root=ET.fromstring(z.read(name));text=[n.text or "" for n in root.findall(".//a:t",NS)]
                charts=len(root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart"))
                info={"slide":idx,"text_runs":len(text),"charts":charts,"text":" ".join(text),"fonts":sorted({n.get("typeface") for n in root.findall(".//a:latin",NS) if n.get("typeface")})}
                if not text:findings.append(issue("NO_EDITABLE_TEXT","Slide lacks native text",slide=idx))
                if not text and not root.findall(".//p:pic",NS):findings.append(issue("EMPTY_SLIDE","Empty slide",slide=idx))
                for shape in list(root.findall(".//p:sp",NS))+list(root.findall(".//p:pic",NS))+list(root.findall(".//p:graphicFrame",NS)):
                    xfrm=shape.find(".//a:xfrm",NS)
                    if xfrm is None:xfrm=shape.find("p:xfrm",NS)
                    if xfrm is not None:
                        off=xfrm.find("a:off",NS);ext=xfrm.find("a:ext",NS)
                        if off is not None and ext is not None:
                            x,y,cx,cy=[int(v) for v in (off.get("x"),off.get("y"),ext.get("cx"),ext.get("cy"))]
                            if x < -9144 or y < -9144 or x+cx>width+9144 or y+cy>height+9144:
                                findings.append(issue("OFF_CANVAS","Element exceeds slide bounds",slide=idx))
                    for r in shape.findall(".//a:r",NS):
                        prop=r.find("a:rPr",NS);t=r.find("a:t",NS)
                        if prop is not None and t is not None and (t.text or "").strip() and int(prop.get("sz","1000"))<800:
                            findings.append(issue("TINY_TYPE","Text below 8 pt",slide=idx,text=t.text[:80]))
                slides.append(info)
            embedded=[n for n in z.namelist() if n.startswith("ppt/embeddings/") and n.endswith(".xlsx")]
    except (OSError,KeyError,ET.ParseError,zipfile.BadZipFile) as e:
        return {"status":"FAIL","findings":[issue("INVALID_PPTX",str(e))]}
    if not slides:findings.append(issue("NO_SLIDES","PPTX has no slides"))
    if pdf:
        import fitz
        doc=fitz.open(pdf)
        if len(doc)!=len(slides):findings.append(issue("PAGE_COUNT","PDF/PPTX page counts differ"))
        for i,page in enumerate(doc):
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines",[]):
                    for span in line["spans"]:
                        x0,y0,x1,y1=span["bbox"]
                        if x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                            findings.append(issue("PDF_TEXT_BOUNDS","Rendered text outside PDF page",slide=i+1,text=span["text"][:80]))
            if i<len(slides):
                expected=norm(slides[i]["text"]);actual=norm(page.get_text())
                # Multiset character coverage survives line wrapping and chart text ordering.
                from collections import Counter
                coverage=sum((Counter(expected)&Counter(actual)).values())/max(1,len(expected))
                slides[i]["rendered_text_coverage"]=round(coverage,3)
                if coverage<0.90:findings.append(issue("PDF_TEXT_LOSS",f"Rendered character coverage {coverage:.1%}",slide=i+1))
    return {"status":"FAIL" if findings else "PASS","scope":"Artifact structure and rendered text; visual/semantic review separate","slides":slides,"embedded_workbooks":len(embedded),"findings":findings}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("mode",choices=("evidence","deck"));p.add_argument("file");p.add_argument("--pdf");p.add_argument("--out");a=p.parse_args()
    r=evidence(json.loads(Path(a.file).read_text())) if a.mode=="evidence" else deck(a.file,a.pdf)
    serialized=json.dumps(r,ensure_ascii=False,indent=2)
    if a.out:Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(serialized)
    print(serialized);sys.exit(1 if r["status"]=="FAIL" else 0)
