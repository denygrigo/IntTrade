#!/usr/bin/env python3
"""Optional, bounded OFL font installer. Project-local by default; no home writes."""
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
from hashlib import sha256
import argparse
import json
import os
import shutil
from xml.sax.saxutils import escape

GOOGLE_FONTS_COMMIT='45e3d5269e4a17d823f6d84470bc084dc5ae46f6'
BASE='https://raw.githubusercontent.com/google/fonts/'+GOOGLE_FONTS_COMMIT+'/ofl/'
FONTS={
 'inter':'Inter[opsz,wght].ttf','manrope':'Manrope[wght].ttf',
 'lora':'Lora[wght].ttf','dmsans':'DMSans[opsz,wght].ttf',
 'plusjakartasans':'PlusJakartaSans[wght].ttf','playfairdisplay':'PlayfairDisplay[wght].ttf',
 'ibmplexsans':'IBMPlexSans[wdth,wght].ttf','librebaskerville':'LibreBaskerville[wght].ttf',
 'montserrat':'Montserrat[wght].ttf','sourcesans3':'SourceSans3[wght].ttf'}

def get(url):
    with urlopen(url,timeout=30) as r:data=r.read(5_000_001)
    if len(data)>5_000_000:raise RuntimeError('Font response exceeds size budget')
    return data

def write(path,data):
    t=path.with_suffix(path.suffix+'.tmp');t.write_bytes(data);os.replace(t,path)

def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true')
    p.add_argument('--family',action='append',choices=sorted(FONTS))
    p.add_argument('--dest',default='work/fonts')
    p.add_argument('--static',action='store_true',help='Create a regular static instance using optional fontTools')
    a=p.parse_args()
    if not a.install:
        print('Dry-run: select only needed OFL families from pinned Google Fonts commit:')
        print(*FONTS.items(),sep='\n');print('Example: --install --family inter --family lora --static --dest work/fonts');return
    if not a.family:p.error('Select explicit --family values; no bulk installation by default')
    if a.static:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
    dest=Path(a.dest).resolve();dest.mkdir(parents=True,exist_ok=True)
    manifest=dest/'installed.json'
    state=json.loads(manifest.read_text()) if manifest.exists() else {'commit':GOOGLE_FONTS_COMMIT,'families':{}}
    if state.get('commit')!=GOOGLE_FONTS_COMMIT:state={'commit':GOOGLE_FONTS_COMMIT,'families':{}}
    for family in dict.fromkeys(a.family):
        old=state['families'].get(family,{})
        records=old.get('files',{})
        target=dest/FONTS[family];regular=dest/(family+'-Regular.ttf')
        verified=state.get('commit')==GOOGLE_FONTS_COMMIT and records and all((dest/f).is_file() and digest(dest/f)==h for f,h in records.items())
        if verified and (not a.static or regular.name in records):print('REUSED',family);continue
        url=BASE+family+'/'
        license_data=get(url+'OFL.txt')
        if b'OPEN FONT LICENSE' not in license_data[:1500].upper():raise RuntimeError('OFL license not confirmed: '+family)
        font=get(url+quote(FONTS[family],safe=''))
        if len(font)<30000 or font[:4] not in (b'OTTO',b'ttcf',bytes([0,1,0,0])):raise RuntimeError('Invalid font signature: '+family)
        license_file=dest/(family+'-OFL.txt');write(license_file,license_data);write(target,font)
        files=[license_file,target]
        if a.static:
            variable=TTFont(target)
            axes={axis.axisTag:axis.defaultValue for axis in variable['fvar'].axes}
            axes['wght']=400
            instance=instantiateVariableFont(variable,axes,inplace=False)
            instance.save(regular);files.append(regular)
        state['families'][family]={'source':url+quote(FONTS[family],safe=''),'license':'SIL-OFL-1.1','files':{f.name:digest(f) for f in files}}
        write(manifest,json.dumps(state,indent=2).encode());print('INSTALLED',family)
    scan_dir=dest
    if a.static:
        scan_dir=dest/'static';scan_dir.mkdir(exist_ok=True)
        for family in a.family:shutil.copy2(dest/(family+'-Regular.ttf'),scan_dir/(family+'-Regular.ttf'))
    cache=dest/'cache';cache.mkdir(exist_ok=True)
    config=dest/'fontconfig.xml'
    config.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><include>/etc/fonts/fonts.conf</include><dir>'+escape(str(scan_dir))+'</dir><cachedir>'+escape(str(cache))+'</cachedir></fontconfig>')
    print('Command-scoped FONTCONFIG_FILE='+str(config))
    print('Current runtime files only; environment publication is separate.')

if __name__=='__main__':main()
