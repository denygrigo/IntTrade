#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="action", required=True)
n = sub.add_parser("new")
n.add_argument("--id", required=True)
n.add_argument("--brief", required=True)
args = p.parse_args()
if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", args.id): p.error("Use a lowercase ASCII slug")
d = ROOT / "work" / args.id
d.mkdir(parents=True, exist_ok=True)
files = {
    "brief.md": args.brief + "\n",
    "evidence.json": json.dumps({"sources": [], "claims": [], "calculations": []}, indent=2),
    "references.json": "[]\n",
    "assets.json": "[]\n",
    "art-direction.md": "# Art direction\n\nAudience / mode / decision:\n\nReferences and access:\n\nGrid / type / color / images / chart language:\n\nSlide storyboard:\n",
    "review.json": json.dumps({"status":"NOT RUN", "reviewer":None,"independent":False,"slides":[],"findings":[]},indent=2),
    "CHECKPOINTS.md": "# Checkpoints\n\n- [ ] Brief\n- [ ] Research + evidence\n- [ ] Reference inspection\n- [ ] Storyboard + visual system\n- [ ] Two slides inspected\n- [ ] Build\n- [ ] Actual PPTX rendered\n- [ ] Every slide inspected\n- [ ] Fact review\n- [ ] Independent review status disclosed\n- [ ] Delivery\n"
}
for name, content in files.items():
    f = d / name
    if not f.exists(): f.write_text(content, encoding="utf-8")
print(d)
