# Risk Model

Use this reference for requirement-level risk assessment before detailed test design.

## Core Formula

`Risk Score = Impact x Likelihood`

Assess the risk that the requirement, as currently specified, will produce a costly defect, outage, compliance issue, or release blocker.

## Allowed Scales

### Impact

Use one of these exact values:

| Value | Label | Use When |
| --- | --- | --- |
| 1 | Very Low | Minor inconvenience, limited workaround needed |
| 2 | Low | Small user or operational impact, low remediation cost |
| 4 | Moderate | Noticeable business disruption or rework |
| 8 | High | Significant user, financial, or delivery impact |
| 16 | Severe | Threatens compliance, revenue, safety, or release success |

### Likelihood

Use one of these exact values:

| Value | Label | Use When |
| --- | --- | --- |
| 1 | Rare | Unlikely with current design and context |
| 2 | Unlikely | Possible, but requires specific conditions |
| 3 | Possible | Plausible in normal usage or integration behavior |
| 4 | Likely | Expected unless controls are added |
| 5 | Almost Certain | Highly probable with the requirement as written |

## Categories

Map numeric scores to categories as follows:

| Score Range | Category |
| --- | --- |
| 1-4 | Low |
| 5-12 | Medium |
| 15-32 | High |
| 40-80 | Critical |

The gaps are intentional because the score set is discrete.

## What Counts As A Requirement Risk

Good risks usually come from one of these sources:

- unclear or missing business-rule logic
- fragile manual overrides
- unhandled dependency failures
- hidden data integrity or reconciliation behavior
- missing role and authorization rules
- untestable or unobservable outputs
- ambiguous non-functional expectations

Avoid generic risks like "bugs may happen." Tie the risk to a concrete failure mode in the requirement.

## Mitigation And Residual Risk

For each risk:

1. Describe the mitigation that would lower likelihood, impact, or both.
2. Re-score the residual risk only if the mitigation is concrete enough to justify a new value.
3. Keep residual impact the same unless the mitigation truly reduces business consequences.

## CLI Usage

Preferred text output:

```bash
python scripts/calculate_risk.py --impact 8 --likelihood 3 --label "Payment timeout"
```

Preferred machine-readable output:

```bash
python scripts/calculate_risk.py --impact 16 --likelihood 4 --residual-impact 16 --residual-likelihood 2 --json
```

## ASCII Matrix Convention

Use impact on the X axis and likelihood on the Y axis:

```text
Likelihood
5 |
4 |
3 |
2 |
1 |
  +--------------------> Impact
    1   2   4   8   16
```

Mark each cell with a short risk ID such as `R1`, `R2`, or `R3`.

## Manual Fallback

If the environment cannot execute Python after reasonable retries:

- compute the score manually with the same scale values
- apply the category thresholds in this file
- clearly label the result as `manual fallback`

Do not silently substitute a different formula or category model.
