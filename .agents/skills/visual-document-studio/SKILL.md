---
name: visual-document-studio
description: Build editable PowerPoint slides and readable PDF reports, render them and preserve reproducible source files.
---

Use PptxGenJS for PPTX, native text/shapes/tables and charts with embedded workbooks.
Preserve XLSX support with openpyxl, formulas and native Excel charts; DOCX with
python-docx and semantic paragraph/table styles. Extraction tools do not preserve
document fidelity. Keep the existing `scripts/create_demo.py` and
`scripts/audit_artifacts.py` path for DOCX/XLSX smoke checks. Check chart source rows,
formulas, units, denominators and scales. Preserve originals when editing user files.
Avoid flattened slides. Images remain images; tell the user which components are editable.
Never copy Anthropic's PPTX, PDF, DOCX or XLSX skill materials into this studio.
Prefer existing runtimes. Run `python3 studio/scripts/doctor.py`; only if missing run
`python3 studio/scripts/bootstrap.py --install-missing`. See pinned dependency manifests.

Author source code and content separately. Set language, document metadata, slide size,
font availability, meaningful notes and source locators. Keep a mapping of each claim
to the ledger and each asset to the rights ledger. Native charts need units, time periods,
denominators and correct axes. Do not turn figures into decorative shapes without data.

`node studio/scripts/build-demos.cjs <directory>` is an acceptance example only, not a
universal layout engine. Author new task-specific source instead of recoloring demos.
`python3 studio/scripts/render.py <deck.pptx> --out <directory>` renders the actual file
via LibreOffice and makes per-slide PNGs plus a contact sheet. A matching PDF made by
another renderer does not verify the PPTX. Render in an isolated LibreOffice profile.

Reports: use ReportLab with embedded installed fonts; include executive findings,
methods, evidence, uncertainty, calculations, source links and date. `report.py` produces
the studio acceptance report; it is a reference implementation, not a report template
for every topic. Inspect PDF pages for clipping and Cyrillic font substitution.

Keep PPTX/PDF and their sources, data, references and QA together. Verify exported
files exist and are non-empty before marking a checkpoint complete. PowerPoint on the
user's device may differ from LibreOffice; list that compatibility limit honestly.
