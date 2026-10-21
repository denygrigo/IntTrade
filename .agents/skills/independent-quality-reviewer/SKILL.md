---
name: independent-quality-reviewer
description: Independently audit source-backed claims, quantitative charts, spreadsheet formulas and generated slide/PDF/Word documents using scripts, real sources and visual rendering.
---

# Independent verification
- Inspect important cited pages, source context, relevant dates and methodology. Distinguish unsupported, weakly supported, contradicted and verified assertions.
- Verify computations against actual source rows and units; checking formula syntax is not checking underlying data truth.
- Run scripts/audit_artifacts.py for file structure. This does NOT validate values or appearance.
- For PPTX/PDF inspect actual full-sized renders and a presentation contact sheet: clipping, broken glyphs, image crop, contrast, slide density, text layout, chart integrity, source notes and style consistency.
- Use deterministic validators and separate audit passes where possible. Never claim an independent second model ran if unavailable.
- Report actual checks as PASS, WARN, FAIL or NOT TESTED; include corrections and remaining limitations. No generic "checked everything" statements.
