# Analysis Framework

Use this reference to keep scoring, wording, and evidence handling consistent across requirement reviews.

## 1. Build The Analysis Baseline

Before scoring, identify:

- artifact name and type
- actors and permissions
- main flow and alternative flows
- business rules and calculations
- external systems or manual handoffs
- data inputs, outputs, and state changes
- stated acceptance criteria or success conditions
- explicit non-functional requirements
- open assumptions or undefined terms

If the artifact is missing most of this information, continue only to document what is missing and score conservatively.

## 2. Testability Rubric

Score each dimension as `0`, `1`, or `2`.

### Clarity

- `0`: confusing flow, inconsistent terminology, or missing core steps
- `1`: understandable but with notable ambiguity or hidden assumptions
- `2`: clear, internally consistent, and easy to interpret

### Controllability

- `0`: actors, triggers, or setup conditions are unclear
- `1`: some control points exist but key prerequisites or states are implicit
- `2`: roles, triggers, and setup conditions are explicit and reproducible

### Observability

- `0`: expected outputs or state changes are largely invisible
- `1`: some outputs are visible, but important behaviors are hard to verify
- `2`: outputs, state changes, and failure signals are visible and checkable

### Repeatability

- `0`: the flow depends on unstable or undefined setup
- `1`: the flow is repeatable with effort, mocks, or assumptions
- `2`: the flow can be rerun with known inputs and predictable outcomes

### Automatability

- `0`: heavy manual, physical, or subjective behavior dominates
- `1`: automation is possible but blocked by unclear interfaces or manual steps
- `2`: automation is practical with stable interfaces and observable results

Interpretation:

- `9-10`: strong candidate for implementation and downstream test design
- `6-8`: workable but needs clarification or design discipline
- `3-5`: high analysis debt; testing will be inefficient or brittle
- `0-2`: not ready for detailed implementation planning

## 3. Static Review Checklist

Look for issues in these categories:

- Flow integrity: missing steps, impossible transitions, branches without exits
- Rules and calculations: missing formulas, thresholds, precedence, or tie-breakers
- Roles and permissions: unclear ownership, authorization, or escalation rules
- Data and state: hidden inputs, missing outputs, undefined lifecycle or reconciliation rules
- Failure handling: no timeout path, retry policy, rollback behavior, or partial-success handling
- Traceability: acceptance criteria or success conditions do not map to the described behavior
- Non-functional fit: accessibility, performance, localization, audit, or compliance statements are detached from the flow

Suggested severity labels:

- `High`: blocks implementation, testing, approval, or safe release
- `Medium`: likely to cause rework, inconsistency, or coverage gaps
- `Low`: does not block progress but should be tightened

Static review score guidance:

- `9-10`: coherent, low ambiguity, and little hidden risk
- `7-8`: generally sound with a few correctable gaps
- `4-6`: multiple material ambiguities or uncovered branches
- `1-3`: major contradictions or missing structure
- `0`: unusable as a requirement artifact

## 4. Gap And Completeness Analysis

Focus on information still required to proceed safely:

- unresolved decisions
- unclear domain terminology
- missing calculations or business rules
- absent exception handling
- undefined data retention or reporting behavior
- missing actor, role, or permission detail
- unspecified downstream dependencies

Completeness score guidance:

- `9-10`: small clarifications only
- `7-8`: some questions remain, but implementation can be planned
- `4-6`: important questions remain and could cause rework
- `1-3`: major decisions are still open
- `0`: insufficient information to proceed responsibly

## 5. Evidence Rules

- Prefer evidence from the provided requirement over generic domain assumptions.
- If you infer a likely issue, label it as an implication rather than a stated fact.
- When a score is not obvious, explain the tradeoff that pushed it up or down.
- If a requirement is internally contradictory, call that out before assigning a score.

## 6. Recommendation Style

Recommendations should be:

- actionable
- scoped to the requirement problem
- ordered by risk or blocker severity
- phrased so a product owner, analyst, or engineer can act on them directly

Good example:

- "Define how the system behaves when the payment provider times out after authorization but before receipt generation."

Weak example:

- "Improve quality."
