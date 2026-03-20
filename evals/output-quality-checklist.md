# Output Quality Checklist

Use this checklist when forward-testing the skill or reviewing a generated report.

## Scope Discipline

- The response stays at requirement-analysis level.
- The response does not drift into executable test cases or implementation code.
- The selected analysis sections match the user request.

## Evidence Quality

- Findings are grounded in the provided requirement.
- Inferred concerns are labeled as analysis, not stated facts.
- Recommendations are concrete and tied to identified issues.

## Scoring Integrity

- Testability and completeness scores are justified, not just announced.
- Static review findings use severity consistently.
- Risk scores match the approved scale and category thresholds.
- Risk calculations come from the bundled script or a clearly labeled manual fallback.

## Stakeholder Usefulness

- Questions are direct and answerable.
- The summary table helps a product or engineering lead decide whether the requirement is ready.
- The report highlights top blockers, not just a long list of observations.

## Memory Safety

- The report may propose a new anti-pattern, but it does not silently mutate project memory.
- Cross-agent shared-memory behavior is not implied or invented.
