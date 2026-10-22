---
name: independent-quality-reviewer
description: Audit final research and design outputs for unsupported claims, numeric conflicts, file defects and visual problems, with explicit reviewer independence.
---

Freeze inputs before review. The reviewer reads final artifacts, original sources and
ledgers, not the author's assurance. Use a separate reviewer when authorized and available;
otherwise label the semantic/visual pass as author review. Do not claim a separate person
or model ran it. Automated scripts run separately from construction but are not semantic
independence. Never silently downgrade a requested independent review to PASS.

Run `qa.py evidence <ledger>` and `qa.py deck <pptx> --pdf <rendered.pdf>`. These tools
are separate from the builder and inspect artifact bytes. They check required provenance,
duplicate metric values, calculations, native editability, off-canvas elements, missing
parts, empty slides, tiny type, PDF page/text consistency and visible text bounds.
They do not establish that a cited page entails a claim or detect every overlap.

For the supported XLSX fixture, use `qa_office.py xlsx` after an actual LibreOffice
recalculation. It independently evaluates supported formulas, compares cached results
and source rows, and checks chart references. Unsupported functions are unverified,
not automatically accepted. For Word use `qa_office.py docx --pdf <actual-export>`;
inspect all actual pages and tables. Test the full pipeline with `acceptance_full.py`.

Open each slide PNG at readable resolution. Check takeaway/data agreement, axes and labels,
source placement, contrast, font substitution, cropping, overlaps, line breaks and alignment.
View a contact sheet for coherence and layout variety. Log each slide, finding, severity,
repair and re-rendered result. Review the report separately, including all source pages.

Finding severities: blocking, major, minor; report PASS / WARN / FAIL / NOT TESTED per check.
Release with zero unresolved blockers and disclose unresolved quality limits. If independent
review was requested but unavailable, status remains WARN / NOT TESTED even if automated checks pass.

Test E: run `qa.py evidence studio/tests/qa_bad.json` and confirm unsupported claim,
inconsistent number and broken provenance/calculation are found with exit code 1. Then
run the corrected fixture and verify exit code 0. Never delete the bad case to make CI pass.
