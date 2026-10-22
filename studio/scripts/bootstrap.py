#!/usr/bin/env python3
"""Install only missing tools. Existing working versions are reported and reused."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from doctor import inventory

p = argparse.ArgumentParser()
p.add_argument("--install-missing", action="store_true")
p.add_argument('--full',action='store_true',help='Also verify optional plotting and font-instancing tools')
args = p.parse_args()
before = inventory(args.full)
if before["ready"]:
    print("READY: existing dependencies reused; no installations performed")
    sys.exit(0)
if not args.install_missing:
    print(json.dumps(before, indent=2))
    print("Missing dependencies. Use --install-missing after reviewing manifests.")
    sys.exit(1)
root = Path(__file__).resolve().parents[1]
missing = [n for n, v in before["packages"].items() if not v]
pin_lines=(root.parent/'requirements.txt').read_text().splitlines()+(root/'requirements.txt').read_text().splitlines()+(root/'requirements-full.txt').read_text().splitlines()
pins = {line.split("==")[0]: line for line in pin_lines if "==" in line}
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", *[pins[n] for n in missing]], check=True, timeout=300)
if (not before["pptxgenjs"] or not before.get('dependency_policy_satisfied')) and before["tools"]["npm"]:
    subprocess.run(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"], cwd=root, check=True, timeout=300)
after = inventory(args.full)
print(json.dumps(after, indent=2))
if not after["tools"]["soffice"]:
    print("LibreOffice missing: configure the environment image; no privileged package changes attempted.")
sys.exit(0 if after["ready"] else 1)
