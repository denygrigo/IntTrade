#!/usr/bin/env python3
"""Actual LibreOffice recalculation / export with isolated profile and no source overwrite."""
import argparse,json,shutil,subprocess,tempfile
from pathlib import Path
import fitz
from PIL import Image,ImageDraw

p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--to',choices=['pdf','xlsx'],default='pdf');p.add_argument('--out',required=True);a=p.parse_args()
source=Path(a.source).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
binary=shutil.which('soffice') or shutil.which('libreoffice')
if not binary:raise SystemExit('LibreOffice unavailable: export NOT TESTED')
if out==source.parent:raise SystemExit('Export to a separate directory to preserve the source')
with tempfile.TemporaryDirectory(prefix='inttrade-office-') as profile,tempfile.TemporaryDirectory(prefix='inttrade-export-') as stage:
    cmd=[binary,'-env:UserInstallation='+Path(profile).as_uri(),'--headless','--convert-to',a.to,'--outdir',stage,str(source)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    generated=Path(stage)/(source.stem+'.'+a.to)
    if r.returncode or not generated.is_file():raise RuntimeError(r.stdout+r.stderr)
    target=out/generated.name;shutil.copy2(generated,target)
result={'source':str(source),'output':str(target),'engine':'LibreOffice actual conversion'}
if a.to=='pdf':
    doc=fitz.open(target);thumbs=[]
    for old in out.glob('page-*.png'):old.unlink()
    for i,page in enumerate(doc):
        f=out/f'page-{i+1:02}.png';page.get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).save(f)
        image=Image.open(f).convert('RGB');image.thumbnail((370,505));tile=Image.new('RGB',(390,535),'#eeeeee');tile.paste(image,((390-image.width)//2,10));ImageDraw.Draw(tile).text((10,519),str(i+1),fill='#222222');thumbs.append(tile)
    sheet=Image.new('RGB',(390*min(3,len(thumbs)),535*((len(thumbs)+2)//3)),'white')
    for i,tile in enumerate(thumbs):sheet.paste(tile,((i%3)*390,(i//3)*535))
    sheet.save(out/'contact-sheet.png');result['pages']=len(doc)
(out/'export.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
