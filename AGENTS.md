# Research & Design Studio

For research, reports, presentations and visual communication, use the studio in
`studio/`. Ordinary code tasks need no presentation workflow.

Read only the relevant skill on demand from `.agents/skills/`:
- research / primary sources / market analysis → `evidence-first-research`;
- slides / deck / презентация → `presentation-art-director`, then `visual-document-studio`;
- images / references / brand visuals → the reference guide in `presentation-art-director/references/visual-asset-curation.md`;
- business prose / text edits → `professional-writing-editor`; explicit humanization → `humanizer`;
- final research or design deliverable → `independent-quality-reviewer`;
- long tasks, interrupted work or failed tools → `workflow-reliability`.

The user need not name skills. Do not load all skill bodies at startup.
Research like an analyst. Design like an art director. Verify like a reviewer.
Choose the narrative for the audience before choosing its visual language.
No fixed universal template, forced theme picker, text/image ratio or token-saving rule.
Keep one visual system inside each deck; make different briefs differ in composition,
typography, information density and narrative, not merely palette or stock photos.

Start a task with `python3 studio/scripts/studio.py new --id <slug> --brief '<brief>'`.
Keep intermediate files and logs in `work/<slug>/`. Use the output destination
configured by the current session; never silently claim a blocked write succeeded.
Use `python3 studio/scripts/doctor.py` before installing anything. The setup script
only installs missing pinned dependencies. Never reinstall to fix an unrelated error.

Use real, opened primary sources and real visual references where accessible.
Distinguish search-discovered, text-opened and image-inspected references. A search
thumbnail description is not a visual inspection. Log blocks and use an allowed
alternative; never bypass a network policy. Keep an asset rights ledger.
Label demo data, estimates and forecasts where used. Do not invent current facts.

Render the actual PPTX to PDF, inspect every slide and create a contact sheet.
Run `qa.py` against final files; audit claim provenance separately. Deterministic
QA cannot certify semantic truth or aesthetics. A second pass by the author is
not an independent reviewer: report reviewer identity and unavailable checks.
Do not spawn agents unless the user or higher-priority instructions authorize it.
Release only with no unresolved blocking findings; keep FAIL/PARTIAL/NOT RUN honest.

No external publication, sharing, credential, network-policy or environment-setting
changes are implied by writing configuration files. Follow the session's authority.

Preserve existing DOCX/XLSX workflows in `scripts/` and `visual-document-studio`.
Default working language is Russian; deliverable language follows the user.
This repository is public. Do not commit secrets, private client materials, third-party
reference images or commercial font files. WBS, Timetta and sprint/project administration
remain separate in ChatGPT Work.
