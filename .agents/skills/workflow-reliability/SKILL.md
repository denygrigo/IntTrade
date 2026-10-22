---
name: workflow-reliability
description: Recover interrupted research or design tasks with checkpoints, bounded retries and dependency reuse; prevent repeated failures and endless loops.
---

Use `work/<task>/` for a brief, task state, logs, evidence, reference ledger, source code
and intermediate outputs. Save after research, storyboard, representative slides, build,
render, QA and delivery. Resume by inspecting saved artifacts and state before rerunning.

`run_guard.py` executes a named command with a timeout, input fingerprint, artifact
validation and a persistent circuit breaker. A successful unchanged stage skips only if
its declared outputs still match hashes. Two failures for the same signature block more
attempts. Reset only the failing stage with `--reset-reason` after recording a changed
hypothesis. Maximum two automatic repair/render cycles before escalating a concrete defect.

Classify first: transient timeout/429/5xx may justify one bounded retry; dependency or
syntax failure needs diagnosis; 401/403 requires access correction, not repeated calls;
missing binaries need doctor/bootstrap; memory/resource faults need a smaller workload.
Never rerun external side effects through the generic guard; inspect remote state using an
idempotency key or exact resource ID. It is designed for local builds and read-only probes.

Doctor checks availability and versions. Bootstrap does nothing when the verified tool
works; missing dependencies install from pinned manifests once and log the result. Do not
delete caches, lockfiles or environments speculatively, and do not perform global upgrades.

Use atomic state writes, stage locks, explicit exit codes, timeouts and bounded logs.
Record a concrete blocker after budget exhaustion. No token economy skill, forced short
research, hidden context truncation policy or uncontrolled dependency reinstall loop.
