# IntTrade — Research & Design Studio

Reusable, project-scoped skills for Codex Cloud: deep research, distinct slide art direction, PowerPoint, Excel, PDF, Word, polished Russian/English writing and independent QA.

The revised PptxGenJS pipeline has been exercised in the cloud runtime on three distinct
six-slide briefs. See the [implementation report](studio/IMPLEMENTATION.ru.md),
[PPTX/PDF examples and QA](studio/examples/acceptance/) and
[runtime instructions](studio/README.ru.md). Acceptance is **PARTIAL**: artifact checks
and author visual review ran; separate semantic review, unrestricted designer-image
access and new-session automatic skill activation remain unverified.

## How to start (iPhone or Mac)
1. In Codex, select repository `denygrigo/IntTrade` and a branch that contains this setup.
2. Ask for your task in Russian. The root `AGENTS.md` routes to task-specific skills under `.agents/skills/`.
3. You can verify discovery with: "List the project skills actually available to you and read their SKILL.md files."
4. For a PPTX: "Create a distinctive 12-slide executive deck, check live design references, build editable PPTX, render and review all slides, verify sources."
5. To try test examples: run `bash scripts/bootstrap.sh`.

## Included
- Six custom workflow skills + MIT-licensed humanizer from blader/humanizer.
- Design/story structures and realistic text-density *heuristics*, not compulsory templates.
- Registers for sources and design inspirations.
- Synthetic PPTX (three designs), XLSX, PDF, DOCX demo generator and integrity checker.
- CI checks via GitHub Actions on commits/pull requests.

## Run from a shell (Python 3.11+)
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python scripts/create_demo.py --out artifacts/demo
.venv/bin/python scripts/audit_artifacts.py artifacts/demo
```

Generated demos deliberately contain synthetic numbers; none are market research.

## What this repository cannot do alone
GitHub access does not grant control over the Safari tab or change Codex Cloud environment settings. Publishing a setup script, font installation, live browser access, skill selection, second-model QA and rendered-slide inspection all require checking **inside** the cloud execution environment. GitHub Actions can verify file formats but not judge factual accuracy or design. Read `quality/VERIFICATION.md`.

**Public repository:** do not commit credentials, personal data, licensed reference imagery, commercial fonts or private client material.
