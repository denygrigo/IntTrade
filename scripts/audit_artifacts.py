#!/usr/bin/env python3
"""Deterministic format checks. NOT visual review, fact checking or calculation certification."""
from pathlib import Path
from zipfile import ZipFile,BadZipFile
from xml.etree import ElementTree
import argparse,sys,json
REQUIRED={".pptx":{"[Content_Types].xml","ppt/presentation.xml"},
".xlsx":{"[Content_Types].xml","xl/workbook.xml"},
".docx":{"[Content_Types].xml","word/document.xml"}}
def audit(path):
    out={"file":str(path),"bytes":path.stat().st_size,"status":"PASS","problems":[]}
    ext=path.suffix.lower()
    if ext in REQUIRED:
        try:
            with ZipFile(path) as z:
                files=set(z.namelist())
                missing=REQUIRED[ext]-files
                if missing:out["problems"].append("required parts missing: "+", ".join(sorted(missing)))
                for n in files:
                    if n.endswith((".xml",".rels")):
                        try:ElementTree.fromstring(z.read(n))
                        except ElementTree.ParseError as e:out["problems"].append("invalid XML "+n+": "+str(e))
                if ext==".pptx":out["slide_xml_count"]=len([x for x in files if x.startswith("ppt/slides/slide") and x.endswith(".xml") and "/" not in x[len("ppt/slides/"):]])
                if ext==".xlsx":out["worksheet_xml_count"]=len([x for x in files if x.startswith("xl/worksheets/sheet") and x.endswith(".xml") and "/" not in x[len("xl/worksheets/"):]])
        except (BadZipFile,OSError) as e:out["problems"].append("invalid ZIP: "+str(e))
    elif ext==".pdf":
        try:
            from pypdf import PdfReader
            r=PdfReader(str(path))
            out["pages"]=len(r.pages)
            if not r.pages:out["problems"].append("PDF contains no pages")
        except Exception as e:out["problems"].append("PDF parse failure: "+str(e))
    else:out["status"]="SKIP"
    if out["problems"]:out["status"]="FAIL"
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("paths",nargs="+");p.add_argument("--json",action="store_true")
    args=p.parse_args()
    files=[]
    for name in args.paths:
        x=Path(name)
        if not x.exists():print("MISSING",x,file=sys.stderr);return 2
        if x.is_dir():files.extend(y for y in x.rglob("*") if y.suffix.lower() in {*REQUIRED,".pdf"})
        else: files.append(x)
    reports=[audit(x) for x in sorted(set(files))]
    if args.json:print(json.dumps(reports,ensure_ascii=False,indent=2))
    else:
        for r in reports:print(r["status"],r["file"],r.get("problems",""))
        print("NOTICE: structural validation only; source, numerical & rendered visual QA NOT TESTED")
    return 1 if any(r["status"]=="FAIL" for r in reports) else 0
if __name__=="__main__":sys.exit(main())
