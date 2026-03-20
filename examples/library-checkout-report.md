# Library Checkout Flow Test Analysis Report

## Executive Summary

The requirement communicates the core borrowing flow, but it leaves business-rule behavior underdefined. The largest issues are missing fee logic, orphaned outputs, and no clear path for limit or exception handling.

## 1. Testability Analysis

What was done:
Assessed the requirement with the five testability dimensions.

| Dimension | Score | Evidence | Recommendation |
| --- | --- | --- | --- |
| Clarity | 1 | The flow is readable, but late fees and recommendations are only named, not explained. | Define rule logic for derived outputs. |
| Controllability | 2 | Actors and triggers are stable and easy to reproduce. | Keep exception paths role-specific. |
| Observability | 1 | Receipt output is visible, but loyalty points and recommendations are not traceable to a rule. | Make derived values and display conditions explicit. |
| Repeatability | 2 | Checkout can be rerun with known inputs. | Add branch conditions for member-limit and unavailable-book scenarios. |
| Automatability | 1 | Core flow is automatable, but manual receipt fallback and undefined rules reduce reliability. | Specify automated and manual boundaries. |

Rationale:
Most flow steps are controllable, but important output logic is not observable enough for consistent verification.

Score: **7/10**

## 2. Static Review

What was done:
Checked the requirement for structural defects, ambiguities, and unhandled branches.

| ID | Category | Severity | Evidence | Why it matters | Recommendation |
| --- | --- | --- | --- | --- | --- |
| F1 | Rules and calculations | High | "System applies due dates and any late fees" provides no late-fee rule. | Fees can be inconsistent or contested. | Define fee conditions, grace periods, and precedence rules. |
| F2 | Data and outputs | Medium | Loyalty points and recommendations are listed as outputs but not tied to any step. | The requirement includes unverifiable, orphaned outputs. | Either define derivation and display logic or remove them from scope. |
| F3 | Failure handling | Medium | Printer fallback exists, but there is no guidance for member-limit or unavailable-book overrides. | Operators may improvise unsupported flows. | Add branches for hard limits, overrides, and unavailable inventory. |

Rationale:
The draft is structurally understandable, but the most interesting business behavior still lives outside the actual flow.

Score: **6/10**

## 3. Risk Assessment

What was done:
Scored requirement-level failure modes using the approved risk model.

| ID | Risk | Impact | Likelihood | Score | Category | Mitigation | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Late fees are applied incorrectly | 8 | 3 | 24 | High | Define fee rules by member type, item type, and grace period. | 8 (Medium) |
| R2 | Receipt displays unsupported loyalty data | 4 | 3 | 12 | Medium | Define loyalty calculation and ownership or remove it from scope. | 4 (Low) |
| R3 | Borrowing limit handling is improvised by staff | 8 | 2 | 16 | High | Add a member-limit branch and any override policy. | 8 (Medium) |

```text
Likelihood
5 |
4 |
3 | R1 R2
2 | R3
1 |
  +--------------------> Impact
    1   2   4   8   16
```

Rationale:
The risk posture is driven mostly by undefined rules, not by flow complexity.

Risk posture: **High**

## 4. Gaps And Stakeholder Questions

What was done:
Captured the unresolved information needed before implementation or test design.

| Area | Missing information or ambiguity | Why it matters | Stakeholder question |
| --- | --- | --- | --- |
| Late fees | No formula, scope, or trigger rule is defined. | Billing behavior cannot be tested or defended. | When are late fees applied, and how are they calculated? |
| Loyalty points | Mentioned on the receipt only. | Output becomes unverifiable and potentially misleading. | How are loyalty points calculated, refreshed, and displayed? |
| Recommendations | Mentioned as a special requirement but not in the flow. | The team cannot tell whether this is in scope for checkout. | Should recommendations appear during checkout, on the receipt, or elsewhere? |
| Borrowing limits | No branch handles a member hitting the limit. | Operators will have no defined behavior for a common exception. | What should the system do when a member has reached the borrowing limit? |

Rationale:
The draft can support discussion, but not disciplined implementation planning yet.

Score: **5/10**

## 5. Summary Table

| Area | Result | Release implication |
| --- | --- | --- |
| Testability | 7/10 | Main flow is serviceable, but derived outputs weaken observability. |
| Static review | 6/10 | Business-rule and scope clarity need improvement. |
| Risk assessment | High posture | Undefined fee and exception behavior can drive rework. |
| Gaps | 5/10 | Clarification is needed before downstream teams proceed. |
