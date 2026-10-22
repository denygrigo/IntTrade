# Actual verification, not marketing promises

## Repository checks
- Each .agents/skills/<name>/SKILL.md has parseable front matter with the folder name and description.
- Generated PPTX/XLSX/DOCX are readable ZIP archives with required Office XML parts; XML parses.
- PDF can be parsed and contains pages.
- Synthetic examples generated without private sources.
- GitHub Actions CI records the outcome of these deterministic checks.

## Must be performed separately in live Codex Cloud
- Skill discovery/activation (a SKILL.md existing in Git is not proof Codex loaded it).
- Live source access, Pinterest/Behance visual reference access, image use permission.
- Whether the current runtime provides actual installed fonts and slide/PDF renderers.
- Real independent citation checks, visual inspection of every rendered slide and meaning/accuracy checks.
- Environment publication, image generation or any optional plugin/API access.

Distinguish PASS, FAIL, WARN and NOT TESTED. Integrity PASS is NOT a claim that the slides look good or facts are verified.

## Observed cloud run, 2026-10-22

The revised PptxGenJS path was actually run in the attached executor: three six-slide
decks, actual PPTX-to-PDF export, per-slide PNGs, native-chart data comparison, author
inspection of every slide, adversarial QA and persistent recovery checks. DOCX/XLSX/PDF
smoke checks also passed. Existing working dependencies were reused.
See [the dated implementation report](../studio/IMPLEMENTATION.ru.md) and
[frozen sample artifacts and QA](../studio/examples/acceptance/).
Separate semantic review, new-session skill activation and PowerPoint on the user's
device remain NOT RUN. Designer-portfolio image access is PARTIAL. These observations
apply to that runtime and those artifact hashes, not all future tasks or CI runs.
