#!/usr/bin/env python3
"""Render PPTX to PDF, PNG pages and contact sheets. Requires LibreOffice + pdftoppm.

Rendering is an input for visual review, not proof that design is good.
"""
from pathlib import Path
from shutil import which
from subprocess import run
from tempfile import TemporaryDirectory
from pypdf import PdfReader
from PIL import Image, ImageOps, ImageDraw
import argparse,sys

def checked(command):
    result=run(command,capture_output=True,text=True,timeout=180)
    if result.returncode:
        raise RuntimeError("Command failed: "+str(command)+"\n"+result.stderr[-1500:])
    return result

def convert(pptx,output):
    office=which("libreoffice") or which("soffice")
    if not office or not which("pdftoppm"):
        raise RuntimeError("Cannot render: LibreOffice (libreoffice/soffice) and pdftoppm are both required")
    target=output/pptx.stem
    target.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix="inttrade-lo-") as temporary:
        profile=(Path(temporary)/"profile").resolve().as_uri()
        checked([office,"-env:UserInstallation="+profile,"--headless",
                 "--convert-to","pdf","--outdir",str(target),str(pptx.resolve())])
    pdf=target/(pptx.stem+".pdf")
    if not pdf.exists():raise RuntimeError("LibreOffice did not produce "+str(pdf))
    count=len(PdfReader(str(pdf)).pages)
    for old in target.glob('slide-*.png'):old.unlink()
    checked(["pdftoppm","-f","1","-l",str(count),"-png","-r","110",str(pdf),str(target/"slide")])
    pngs=sorted(target.glob("slide-*.png"))
    if len(pngs)!=count:raise RuntimeError("Expected %s PNG files, got %s"%(count,len(pngs)))
    tile_w,tile_h=480,300;gap=22;caption=34;cols=2;rows=(len(pngs)+1)//2
    sheet=Image.new("RGB",(gap+(tile_w+gap)*cols,gap+(tile_h+caption+gap)*rows),"#e9edf0")
    draw=ImageDraw.Draw(sheet)
    for n,fn in enumerate(pngs):
        with Image.open(fn) as im:
            pic=ImageOps.contain(im.convert("RGB"),(tile_w,tile_h))
            x=gap+(n%cols)*(tile_w+gap)
            y=gap+(n//cols)*(tile_h+caption+gap)
            sheet.paste(pic,(x+(tile_w-pic.width)//2,y+(tile_h-pic.height)//2))
            draw.text((x,y+tile_h+5),"Slide "+str(n+1),fill="#23313f")
    out=target/"contact-sheet.png"
    sheet.save(out)
    print("RENDERED",pptx.name,count,"slides ->",target)
    print("NOTE: Inspect images manually/model visually; PNGs alone do not verify quality.")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("paths",nargs="+",help="PPTX files or directories")
    p.add_argument("--out",default="artifacts/preview")
    a=p.parse_args()
    inputs=[]
    for s in a.paths:
        x=Path(s)
        inputs.extend(sorted(x.rglob("*.pptx")) if x.is_dir() else [x])
    if not inputs:raise SystemExit("No PPTX inputs")
    failures=[]
    for fn in inputs:
        try:convert(fn,Path(a.out))
        except Exception as e:failures.append((str(fn),str(e)));print("FAIL",fn,e,file=sys.stderr)
    return 1 if failures else 0
if __name__=="__main__":sys.exit(main())
