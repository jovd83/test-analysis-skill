# Requirement Antipatterns

This file is the project-local persistent memory for `test-analysis-skill`.

Use it as follows:

- Read it before starting an analysis.
- Treat it as reusable guidance, not as a transcript of past runs.
- Propose new entries in analysis output first.
- Persist new entries only with explicit maintainer approval.
- Keep each entry stable, portable, and specific enough to trigger useful questions.

## RP-001 Happy-path-only flow

Signals:

- The requirement only describes what happens when everything goes right.
- External integrations, validation failures, or user mistakes have no branch behavior.

Why it matters:

- Teams miss recovery logic, fallback behavior, and observability requirements.

Questions to ask:

- What are the primary failure modes for each external dependency or user input?
- What should the user see when the flow cannot continue?

## RP-002 Missing empty-state or not-found behavior

Signals:

- Search, lookup, list, or retrieval features only describe success results.

Why it matters:

- Implementations drift into inconsistent empty states, dead ends, or confusing retries.

Questions to ask:

- What happens when zero results are returned?
- Does the user stay in flow, retry, or need escalation?

## RP-003 Vague service-level language

Signals:

- Phrases like "fast", "responsive", "real-time", or "user friendly" appear without measurable targets.

Why it matters:

- Testability drops because pass or fail cannot be judged objectively.

Questions to ask:

- What latency, throughput, availability, or volume thresholds define success?
- Under which workload or device conditions do those thresholds apply?

## RP-004 Role or permission ambiguity

Signals:

- The requirement says "the user" can do something without clarifying roles, tenancy, or authorization rules.

Why it matters:

- Security, auditability, and negative-path testing become under-specified.

Questions to ask:

- Which roles can trigger this action?
- Are there override, approval, or delegation rules?

## RP-005 Concurrency and overwrite risk

Signals:

- The requirement allows updates to shared records with no collision or locking rule.

Why it matters:

- Last-write-wins behavior often appears accidentally and corrupts data or intent.

Questions to ask:

- What happens when two actors edit the same entity at once?
- Should the system merge, reject, warn, or lock?

## RP-006 Undefined dependency failure handling

Signals:

- The flow relies on payment providers, identity services, queues, printers, or APIs with no timeout or degradation path.

Why it matters:

- Reliability and operational support become guesswork.

Questions to ask:

- What happens on timeout, partial success, or downstream outage?
- Is the operation retried, queued, reversed, or abandoned?

## RP-007 Missing data lifecycle rules

Signals:

- Requirements create, display, or export data without retention, correction, or deletion rules.

Why it matters:

- Privacy, audit, and downstream-reporting defects surface late.

Questions to ask:

- How long is this data retained?
- Who can edit, delete, or reconcile it?

## RP-008 Unbounded manual override

Signals:

- A manager or operator can override a system rule, but the requirement omits reason capture, audit trail, or fallback behavior.

Why it matters:

- Overrides become invisible failure paths with weak accountability.

Questions to ask:

- What evidence must be captured for an override?
- Is approval synchronous, asynchronous, or delegated?

## RP-009 Orphaned outputs or derived data

Signals:

- The requirement mentions calculated values, recommendations, scores, or receipts that are never defined or consumed elsewhere.

Why it matters:

- Teams implement placeholders, dead fields, or unverifiable outputs.

Questions to ask:

- How is the value derived?
- Where is it displayed, stored, and validated?

## RP-010 Non-functional requirements disconnected from the flow

Signals:

- Security, accessibility, localization, or performance requirements are listed separately but never tied to concrete behavior.

Why it matters:

- They are easy to forget during design and nearly impossible to validate consistently.

Questions to ask:

- Which steps, roles, devices, or interfaces are affected?
- What evidence demonstrates compliance?
