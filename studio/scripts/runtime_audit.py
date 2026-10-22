#!/usr/bin/env python3
"""Bounded, non-secret runtime inventory; no environment or credential dumping."""
import argparse,importlib.util,json,os,shutil,subprocess,hashlib
from datetime import datetime,timezone
from pathlib import Path
from doctor import inventory

p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--font-config');p.add_argument('--catalog-snapshot');a=p.parse_args()
root=Path(__file__).resolve().parents[2]
r={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'runtime':inventory(full=True),'commands':{},'fonts':{},'extractors':{},'project_skill_files':[]}
commands={'node':['node','--version'],'npm':['npm','--version'],'pip':['python3','-m','pip','--version'],'libreoffice':['soffice','--version'],'poppler':['pdftoppm','-v'],'codex_cli':['codex','--version'],'git':['git','--version']}
for label,cmd in commands.items():
    if not shutil.which(cmd[0]):r['commands'][label]={'status':'NOT TESTED','reason':'binary missing'};continue
    proc=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
    lines=(proc.stdout+proc.stderr).strip().splitlines()
    r['commands'][label]={'status':'PASS' if proc.returncode==0 else 'WARN','version':lines[0][:200] if lines else ''}
env=os.environ.copy()
if a.font_config:env['FONTCONFIG_FILE']=str(Path(a.font_config).resolve())
installed=subprocess.check_output(['fc-list',':','family'],env=env,text=True)
families={f.strip().lower() for line in installed.splitlines() for f in line.split(',')}
for family in ['Inter','Manrope','IBM Plex Sans','DM Sans','Plus Jakarta Sans','Lora','Libre Baskerville','Playfair Display','Noto Sans','Liberation Sans','DejaVu Sans','Aptos']:
    r['fonts'][family]='FOUND' if family.lower() in families else 'MISSING'
r['fonts_scope']='Command-scoped Fontconfig plus existing system fonts; not a published environment setting'
for module in ['markitdown','docling','fitz','pptx','openpyxl','docx','matplotlib','fontTools']:r['extractors'][module]=bool(importlib.util.find_spec(module))
for f in sorted((root/'.agents/skills').glob('*/SKILL.md')):r['project_skill_files'].append({'name':f.parent.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
if a.catalog_snapshot:r['catalog_observation']=json.loads(Path(a.catalog_snapshot).read_text())
r['recognition_limit']='Seven files and successful workflow execution do not establish automatic skill activation by this running session or a future task.'
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(a.out)
