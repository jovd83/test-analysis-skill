# Requirements Test Analysis Skill

![version](https://img.shields.io/badge/version-1.0.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/jovd83)

`test-analysis-skill` is an Agent Skill for reviewing requirements before implementation or detailed test design. It helps an agent act like a disciplined senior test analyst: inspect requirement quality, assess testability, surface delivery risk, and turn ambiguity into stakeholder questions.

## What This Skill Is Responsible For

- Reviewing requirement artifacts such as use cases, user stories, functional specs, and acceptance criteria.
- Producing structured outputs for testability, static review, risk assessment, and gap analysis.
- Using deterministic helper scripts for risk scoring and report export.
- Maintaining a small, explicit project-local memory of recurring requirement anti-patterns.

## What This Skill Is Not Responsible For

- Writing executable test cases, automation code, or product code.
- Acting as a shared-memory system across repositories or teams.
- Providing ALM connectors, Jira/Xray API integrations, or document-conversion pipelines.
- Replacing stakeholder decisions when the requirement is incomplete.

## Repository Layout

```text
.github/
  workflows/
    ci.yml
agents/
  openai.yaml
evals/
  output-quality-checklist.md
  trigger-queries.json
examples/
  calculator-requirement.md
  calculator-report.md
  library-checkout-requirement.md
  library-checkout-report.md
  pos-checkout-requirement.md
  pos-checkout-report.md
memory/
  requirement-antipatterns.md
references/
  analysis-framework.md
  risk-model.md
scripts/
  calculate_risk.py
  export_report.py
  validate_skill.py
tests/
  test_calculate_risk.py
  test_export_report.py
  test_validate_skill.py
CHANGELOG.md
CONTRIBUTING.md
.gitignore
README.md
SKILL.md
```

## Installation

Place this folder in a location your agent scans for skills, such as:

- `~/.agents/skills/test-analysis-skill`
- `<project>/.agents/skills/test-analysis-skill`

The skill name is `test-analysis-skill`, so explicit invocations should use `$test-analysis-skill`.

## How To Use It

Example prompts:

- `Use $test-analysis-skill to review this checkout use case for testability, static issues, risk, and gaps.`
- `Use $test-analysis-skill to assess whether these acceptance criteria are testable before we hand them to QA.`
- `Use $test-analysis-skill to produce a risk-based requirement review for this story and list stakeholder questions.`

The skill defaults to four analysis areas unless the user narrows the scope:

- Testability analysis
- Static review
- Risk assessment
- Gaps and stakeholder questions

## Memory Model

This repository uses a deliberately scoped memory architecture:

- Runtime memory: working notes for the current analysis only. It is ephemeral.
- Project or skill memory: `memory/requirement-antipatterns.md`. This is the only bundled persistent memory file.
- Shared memory: intentionally not bundled here. If broader reuse is needed, integrate with an external shared-memory skill or platform capability.

The skill does not auto-promote runtime observations into persistent memory. New anti-patterns should be proposed first and persisted only with explicit approval.

## Scripts

- `scripts/calculate_risk.py`: validates allowed scales, computes inherent and residual risk, and can emit JSON for traceable scoring.
- `scripts/export_report.py`: converts Markdown reports to styled HTML without requiring third-party Python packages.
- `scripts/validate_skill.py`: validates the repository layout, skill metadata, examples, eval assets, and agent metadata.

## Validation And Tests

Run the validator:

```bash
python scripts/validate_skill.py
```

Run the unit tests:

```bash
python -m unittest discover -s tests -v
```

Generate an HTML report from a Markdown example:

```bash
python scripts/export_report.py examples/pos-checkout-report.md --output pos-checkout-report.html
```

## Evaluation Assets

- `evals/trigger-queries.json` contains should-trigger and should-not-trigger prompts for description tuning.
- `evals/output-quality-checklist.md` is a lightweight reviewer checklist for forward-testing the skill's outputs.

## Optional Integrations And Out Of Scope Items

- Ticket import JSON is supported as an output format, not as a live connector.
- HTML export is bundled; PDF and Word remain downstream conversions.
- Shared memory is an external integration boundary, not an embedded subsystem in this skill.
- A license file is provided (MIT License).

## Standards Alignment

This repository is aligned with the Agent Skills progressive-disclosure model, the `SKILL.md` frontmatter conventions, and the recommended `agents/openai.yaml` metadata pattern:

- https://agentskills.io/client-implementation/adding-skills-support
- https://agentskills.io/skill-creation/optimizing-descriptions
- https://agentskills.io/skill-creation/evaluating-skills
