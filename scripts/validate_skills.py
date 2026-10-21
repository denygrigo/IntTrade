#!/usr/bin/env python3
"""Validate static project skill manifests; does not prove runtime discovery."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/".agents/skills"
EXPECTED={"evidence-first-research","presentation-art-director","visual-document-studio",
          "professional-writing-editor","independent-quality-reviewer","workflow-reliability","humanizer"}
def main():
    problems=[]
    found={p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    for missing in sorted(EXPECTED-found): problems.append("missing skill: "+missing)
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        data=path.read_text(encoding="utf-8")
        if not data.startswith("---\n") or "\n---\n" not in data[4:]:
            problems.append(str(path)+" missing YAML header")
            continue
        header=data.split("\n---\n",1)[0][4:]
        name=re.search(r"(?m)^name:\s*([a-z][a-z0-9-]+)\s*$",header)
        if not name or name.group(1)!=path.parent.name:
            problems.append(str(path)+" name/folder mismatch")
        if not re.search(r"(?m)^description:\s*(?:\S|\|)",header):
            problems.append(str(path)+" missing description")
    if not (ROOT/"AGENTS.md").exists(): problems.append("AGENTS.md missing")
    for item in problems: print("FAIL:",item)
    print("Skills found:",len(found))
    if problems: return 1
    print("PASS: static skill manifests; live Codex Cloud discovery remains NOT TESTED")
    return 0
if __name__=="__main__":sys.exit(main())
