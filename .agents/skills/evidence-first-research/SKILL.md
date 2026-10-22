---
name: evidence-first-research
description: Research markets or complex questions, verify claims with primary sources and prepare evidence-backed analytical reports.
---

1. Define the decision, geography, period, audience and cutoff date. Use the user's timezone.
2. Write a research plan with subquestions and an evidence table. Separate facts,
   calculations, assumptions, forecasts and recommendations.
3. Prefer primary datasets, regulator filings, original papers and official reports.
   Read the source itself; a search snippet alone is discovery. Corroborate material
   disputed claims with an independent source. Keep publication and observation dates.
4. In `work/<task>/evidence.json`, record a source ID, URL, publisher, title, accessed
   date, exact locator, a short support excerpt and limitations. Claims link to source
   IDs and record metric, value, unit, period, geography and scope. Do not let different
   currencies, years or denominators create false comparisons.
5. Record calculations with operands and formula; recompute totals, shares and growth.
   If the source is unavailable, mark the claim unverified, omit it or qualify it.
6. Synthesize around the decision. Keep methods, uncertainty, conflicting evidence and
   missing coverage visible. No unsupported recommendation masquerading as a fact.
7. Pass the ledger and frozen report to QA. `python3 studio/scripts/qa.py evidence
   <ledger.json>` checks structured provenance and numeric consistency, not entailment.

For a new job, `studio.py new` creates a ledger scaffold. Research must fill it with
opened evidence. User example prompts are not assignments to perform that market study.
