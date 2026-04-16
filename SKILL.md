---
name: test-analysis-skill
description: Use when reviewing use cases, user stories, acceptance criteria, business requirements, or functional specifications for testability, ambiguity, requirement quality, delivery risk, or missing stakeholder decisions before implementation or detailed test design. Use for static requirement reviews, risk-based analysis, and readiness triage. Do not use when the primary goal is writing executable test cases or application code.
metadata:
    dispatcher-layer: execution
    dispatcher-lifecycle: active
  author: jovd83
  version: 1.1.0
  dispatcher-output-artifacts: analysis_report, ambiguity_findings, risk_summary
  dispatcher-risk: low
  dispatcher-writes-files: true
  dispatcher-input-artifacts: requirements, acceptance_criteria, business_rules, project_context
  dispatcher-capabilities: requirements-test-analysis, ambiguity-review, delivery-risk-analysis
  dispatcher-stack-tags: analysis, testing, requirements
  dispatcher-accepted-intents: analyze_requirements_for_testability, review_requirement_quality, assess_delivery_risk
  dispatcher-category: analysis
---
# Requirements Test Analysis

Analyze requirement quality before implementation starts. Produce a decision-ready review that helps product, engineering, and QA teams spot ambiguity, hidden risk, and missing information early.


## Telemetry & Logging
> [!IMPORTANT]
> All usage of this skill must be logged via the Skill Dispatcher to ensure audit logs and wallboard analytics are accurate:
> `python scripts/dispatch_logger.py --skill <skill_name> --intent <intent> --reason <reason>`

## Scope

- Review requirement artifacts such as use cases, user stories, workflow specs, acceptance criteria, and mixed requirement drafts.
- Default to four analysis areas unless the user narrows the scope: testability, static review, risk assessment, and gaps/stakeholder questions.
- Stay at requirement-analysis level. Do not drift into implementation design, code generation, or detailed test-case authoring.

## Required Inputs

Do not start scoring until you have the requirement text or a readable file. If the request names a requirement but does not provide it, stop and ask for the artifact.

Useful optional inputs:

- requested analysis scope
- business criticality or release context
- known constraints or non-functional requirements
- preferred export format

## Load These Resources

Read these files before scoring:

- `references/analysis-framework.md`
- `memory/requirement-antipatterns.md`

Read `references/risk-model.md` whenever risk analysis is requested or included by default.

Read one matching example from `examples/` only when you need a formatting exemplar. Use examples as style references, not as authoritative scoring logic.

## Working Method

1. Identify the target artifact, requested scope, domain context, actors, flows, rules, integrations, data, and stated success criteria.
2. Separate observed facts from inference. Quote or point to requirement evidence when it materially supports a finding.
3. Run each requested analysis area using the rubrics in `references/analysis-framework.md`.
4. If risk analysis is in scope, calculate every inherent risk score with `scripts/calculate_risk.py`. Prefer JSON mode:
   ```bash
   python scripts/calculate_risk.py --impact 8 --likelihood 3 --json
   ```
5. If mitigation materially changes the risk, calculate residual risk with the same script instead of estimating it by feel.
6. Convert missing rules, unclear terminology, hidden assumptions, or unresolved branch behavior into direct stakeholder questions.
7. If the requirement is too weak to support a reliable conclusion, say so plainly and score accordingly.

## Guardrails

- Do not write executable tests, numbered test cases, or implementation code.
- Do not invent business rules, acceptance criteria, UI behavior, or failure handling that the requirement does not support.
- Do not guess numeric risk values outside the allowed scales in `references/risk-model.md`.
- Do not modify project-local memory during normal analysis. Propose memory updates in the report; only persist them when the user explicitly approves a repository or skill update.
- Do not present opinions as facts. Mark inferred concerns as analysis or likely implications.

## Gotchas

- **Confusing Risk and Gaps**: A gap is a missing piece of information (e.g., "What happens if X fails?"); a risk is a potential negative outcome (e.g., "If X fails, the system crashes"). Keep them in their respective sections.
- **Soft Scoring**: Avoid giving high scores just because a requirement is "good enough" for a small project. Use the rubrics in `references/analysis-framework.md` strictly.
- **Prescriptive Recommendations**: Recommendations should focus on clarifying or improving the requirement text, not on providing technical implementation designs (e.g., suggest "Define timeout behavior" instead of "Use a try-catch block").
- **Generic Summaries**: Ensure the Executive Summary is specific to the artifact analyzed and doesn't read like a generic template.
- **Prompting for Input**: If the user mentions a requirement but hasn't pasted it or provided a file path, don't generate a placeholder review. Stop and ask for the material.
- **Vague Adjectives**: Don't overlook terms like "fast," "simple," or "intuitive." These are testability gaps. Flag them as ambiguities and suggest measurable thresholds.
- **Missing NFRs**: Look for missing non-functional requirements (performance, security, accessibility) that are implicit in the domain but missing from the text.
- **Disconnected Findings**: Ensure every finding in the Static Review or Risk Assessment maps back to a specific part of the requirement text or a clearly defined gap. Avoid "floating" critiques without evidence.

## Analysis Outputs

Produce only the sections the user requested. If scope is unspecified, include all sections below.

### 1. Executive Summary

Start with a short summary covering:

- analyzed artifact and scope
- overall readiness statement
- top blockers or highest risks

### 2. Testability Analysis

Use the five-dimension rubric from `references/analysis-framework.md`:

- Clarity
- Controllability
- Observability
- Repeatability
- Automatability

For this section include:

- `What was done`
- a table with `Dimension | Score | Evidence | Recommendation`
- `Rationale`
- `Score: **x/10**`

### 3. Static Review

Review the requirement for structure, ambiguity, coverage, and contradiction using the static review checklist in `references/analysis-framework.md`.

For this section include:

- `What was done`
- a findings table with `ID | Category | Severity | Evidence | Why it matters | Recommendation`
- `Rationale`
- `Score: **x/10**`

### 4. Risk Assessment

Use the scales and thresholds in `references/risk-model.md`.

For each identified risk:

1. Assign impact from `{1, 2, 4, 8, 16}`.
2. Assign likelihood from `{1, 2, 3, 4, 5}`.
3. Run `scripts/calculate_risk.py`.
4. Capture the score and category from the script output.

Include:

- `What was done`
- a risk register with `ID | Risk | Impact | Likelihood | Score | Category | Mitigation | Residual`
- an ASCII risk matrix
- `Rationale`
- `Risk posture: **Low / Medium / High / Critical**`

If Python execution is unavailable after reasonable retries, fall back to the documented thresholds in `references/risk-model.md` and clearly label the result as a manual fallback.

### 5. Gaps and Stakeholder Questions

Identify what is still missing to implement, test, or approve the requirement safely.

Include:

- `What was done`
- a gap register with `Area | Missing information or ambiguity | Why it matters | Stakeholder question`
- `Rationale`
- `Score: **x/10**`

### 6. Summary Table

End with a compact decision table:

| Area | Result | Release implication |
| --- | --- | --- |

## Memory Model

Use a scoped, auditable memory model:

- Runtime memory: the working notes for the current analysis only. Do not persist it automatically.
- Project or skill memory: `memory/requirement-antipatterns.md`. Read it before analysis. Treat it as read-only unless the user explicitly approves a durable update.
- Shared memory: out of scope for this repository. If cross-agent reuse is needed, integrate with an external shared-memory skill rather than storing shared state here.

When you discover a candidate new anti-pattern, add a short `Memory promotion candidate` note to the report instead of silently updating the memory file.

## Export Options

If the user asks for export or handoff formatting:

- Save the report as Markdown, then convert it to HTML with:
  ```bash
  python scripts/export_report.py path/to/report.md --output path/to/report.html
  ```
- For ticket import payloads, emit strict JSON only when explicitly requested.
- Treat PDF or Word as optional downstream conversions from the HTML or Markdown output. This skill does not bundle a document-conversion pipeline.

## Bundled Resources

- `references/analysis-framework.md`: scoring rubrics and review checklist
- `references/risk-model.md`: numeric risk model, thresholds, and residual-risk guidance
- `memory/requirement-antipatterns.md`: project-local persistent memory of recurring requirement failures
- `scripts/calculate_risk.py`: deterministic risk scoring
- `scripts/export_report.py`: Markdown-to-HTML report export
- `scripts/validate_skill.py`: repository validation
- `examples/`: paired requirement and report samples

## Quick Prompt Examples

- `Use $test-analysis-skill to review this checkout use case for all four analysis areas.`
- `Use $test-analysis-skill to assess whether these acceptance criteria are testable and what stakeholder questions remain.`
- `Use $test-analysis-skill to produce a risk-focused requirement review before we hand this story to engineering.`
