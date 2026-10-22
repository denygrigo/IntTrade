#!/usr/bin/env python3
"""Read-only capability inventory. Never prints credentials or the environment."""
import importlib.metadata as md
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

def inventory():
    result = {"python": sys.version.split()[0], "packages": {}, "tools": {}}
    for name,module in (("Pillow","PIL"), ("PyMuPDF","fitz"), ("reportlab","reportlab"), ("python-pptx","pptx"),("openpyxl","openpyxl"),("python-docx","docx"),("pypdf","pypdf")):
        try:
            importlib.import_module(module)
            result["packages"][name] = md.version(name)
        except (ImportError,md.PackageNotFoundError): result["packages"][name] = None
    for name in ("node", "npm", "soffice", "git", "fc-list"):
        result["tools"][name] = shutil.which(name)
    if result["tools"]["node"]:
        code = "const fs=require('fs'),p=require('path'),P=require('pptxgenjs');new P();let f=require.resolve('pptxgenjs');while(!fs.existsSync(p.join(p.dirname(f),'package.json')))f=p.dirname(f);console.log(JSON.parse(fs.readFileSync(p.join(p.dirname(f),'package.json'))).version)"
        r = subprocess.run(["node", "-e", code], cwd=Path(__file__).resolve().parents[1],capture_output=True, text=True, timeout=20)
        result["pptxgenjs"] = r.stdout.strip() if r.returncode == 0 else None
    else: result["pptxgenjs"] = None
    result["ready"] = all(result["packages"].values()) and all(result["tools"].values()) and bool(result["pptxgenjs"])
    return result

if __name__ == "__main__":
    result = inventory()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ready"] else 1)
