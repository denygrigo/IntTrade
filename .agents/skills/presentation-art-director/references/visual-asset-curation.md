# Visual reference and asset curation

Reference discovery is not image licensing. Search relevant portfolios; open the original
work and inspect images before making compositional claims. Record separately:
`discovered`, `text_accessed`, `image_accessed`, `visually_inspected`, `blocked`.
Retain exact URLs and short factual notes. Do not store third-party full-resolution
works in published deliverables without permission. Keep private reference caches private.

`python3 studio/scripts/probe_references.py <references.json>` makes bounded HTTP probes
under the inherited network policy, logs MIME/status/hash, and optionally caches permitted
images under `work/`. It cannot prove visual inspection or grant a license. A web connector
may have different access; log that route too. A 403 is terminal until policy/access changes.

Analyze 3–6 works matched to purpose, audience and medium; do not use arbitrary templates.
Extract principles, not identity or distinctive graphics. For included assets record creator,
original URL, license/permission, attribution and use. Use original vectors, generated visuals
or licensed photos. Never use a reference screenshot as the deck's background by default.
Keep generated imagery labelled in the asset ledger and do not present it as documentary.

User-licensed templates may be adapted closely within their terms; preserve editability and
record which parts were reused. Missing imagery should prompt an appropriate allowed
substitute or explicit limitation, not repeated downloads or invented visual inspection.
