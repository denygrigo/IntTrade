#!/usr/bin/env python3
"""Render actual PPTX with isolated LibreOffice; no alternate-look PDF substitute."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import fitz
from PIL import Image, ImageDraw

def render(source,out):
    source=Path(source).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    binary=shutil.which("soffice") or shutil.which("libreoffice")
    if not binary: raise RuntimeError("LibreOffice missing; actual PPTX render is NOT RUN")
    with tempfile.TemporaryDirectory(prefix="studio-lo-") as profile, tempfile.TemporaryDirectory(prefix="studio-pdf-") as staging:
        r=subprocess.run([binary,"-env:UserInstallation="+Path(profile).as_uri(),"--headless","--convert-to","pdf","--outdir",staging,str(source)],capture_output=True,text=True,timeout=120)
        pdf=Path(staging)/(source.stem+".pdf")
        if r.returncode or not pdf.exists(): raise RuntimeError(r.stderr+r.stdout)
        target=out/pdf.name;shutil.copy2(pdf,target)
    doc=fitz.open(target)
    for old in out.glob('slide-*.png'):old.unlink()
    thumbs=[]
    for i,page in enumerate(doc):
        f=out/f"slide-{i+1:02}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(f)
        im=Image.open(f).convert("RGB");im.thumbnail((480,270))
        tile=Image.new("RGB",(500,304),"#e9e9e9");tile.paste(im,((500-im.width)//2,10))
        ImageDraw.Draw(tile).text((10,286),f"{source.stem} / {i+1:02}",fill="#222222")
        thumbs.append(tile)
    sheet=Image.new("RGB",(1000,304*((len(thumbs)+1)//2)),"white")
    for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*500,(i//2)*304))
    sheet.save(out/"contact-sheet.png")
    info={"source":str(source),"pdf":str(target),"pages":len(doc),"renderer":"LibreOffice actual PPTX export"}
    (out/"render.json").write_text(json.dumps(info,indent=2))
    print(json.dumps(info))

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("pptx");p.add_argument("--out",required=True);a=p.parse_args();render(a.pptx,a.out)
