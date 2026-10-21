---
name: visual-document-studio
description: Build or edit actual PPTX, PDF, DOCX, Excel XLSX, analytical charts and reports with editable elements, source data and proper file-format QA.
---

# Production
- Identify intended deliverable and editability; use presentation-art-director for decks.
- Prefer native components: text, shapes and charts in PPTX; formulas and Excel charts in XLSX; actual paragraph/table styles in DOCX; vector/report exports for PDF.
- Tool options: python-pptx or PptxGenJS, openpyxl, python-docx, reportlab, pypdf, SVG and licensed figures. Install only required dependencies. MarkItDown and Docling are extraction workflows, not fidelity-preserving editors.
- For charts, verify units, source rows, proportion, denominators, labels, scales and uncertainties. No invented illustrative data misrepresented as research.
- Render files when supported, audit all pages and give previews when useful. Use scripts/audit_artifacts.py for structural checks; structural PASS is not visual PASS.
- Preserve originals if modifying existing files. Document changed sections and unresolved limitations.
