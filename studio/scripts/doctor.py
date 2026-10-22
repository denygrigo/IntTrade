#!/usr/bin/env python3
"""Read-only capability inventory. Never prints credentials or the environment."""
import importlib.metadata as md
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

def inventory(full=False):
    result = {"python": sys.version.split()[0], "packages": {}, "tools": {}}
    packages=[("Pillow","PIL"), ("PyMuPDF","fitz"), ("reportlab","reportlab"), ("python-pptx","pptx"),("openpyxl","openpyxl"),("python-docx","docx"),("pypdf","pypdf")]
    if full:packages += [('fonttools','fontTools'),('matplotlib','matplotlib')]
    for name,module in packages:
        try:
            importlib.import_module(module)
            result["packages"][name] = md.version(name)
        except (ImportError,md.PackageNotFoundError): result["packages"][name] = None
    for name in ("node", "npm", "soffice", "git", "fc-list"):
        result["tools"][name] = shutil.which(name)
    if result["tools"]["node"]:
        code = "const fs=require('fs'),p=require('path'),P=require('pptxgenjs'),{createRequire}=require('module');new P();const scoped=createRequire(require.resolve('pptxgenjs'));function pkg(m){let d=p.dirname(scoped.resolve(m));while(true){const f=p.join(d,'package.json');if(fs.existsSync(f)){const v=JSON.parse(fs.readFileSync(f)).version;if(v)return v}const next=p.dirname(d);if(next===d)throw Error('No version metadata');d=next}}console.log(JSON.stringify({pptxgenjs:pkg('pptxgenjs'),image_size:pkg('image-size')}))"
        r = subprocess.run(["node", "-e", code], cwd=Path(__file__).resolve().parents[1],capture_output=True, text=True, timeout=20)
        packages=json.loads(r.stdout) if r.returncode==0 else {}
        result["pptxgenjs"] = packages.get('pptxgenjs')
        result['image_size']=packages.get('image_size')
    else: result["pptxgenjs"] = None;result['image_size']=None
    policy=json.loads((Path(__file__).resolve().parents[1]/'package.json').read_text())
    result['required_image_size']=policy.get('overrides',{}).get('image-size')
    result['dependency_policy_satisfied']=bool(result['required_image_size']) and result['image_size']==result['required_image_size']
    result["ready"] = all(result["packages"].values()) and all(result["tools"].values()) and bool(result["pptxgenjs"]) and result['dependency_policy_satisfied']
    return result

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--full',action='store_true');args=p.parse_args()
    result = inventory(args.full)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ready"] else 1)
