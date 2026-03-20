# Contributing

Keep this repository small, explicit, and useful to another agent.

## Principles

- Keep `SKILL.md` focused on workflow, guardrails, and activation guidance.
- Move detailed rubrics or domain references into `references/`.
- Keep scripts dependency-light and deterministic.
- Treat `memory/requirement-antipatterns.md` as project-local memory, not a dumping ground for one-off observations.
- Prefer ASCII unless a file already requires something else.

## When You Change The Skill

1. Update `SKILL.md` only when the agent-facing behavior changes.
2. Update `agents/openai.yaml` when the title, short description, or default prompt becomes stale.
3. Keep examples, evals, and tests aligned with the current workflow.
4. Record user-visible repository changes in `CHANGELOG.md`.

## Validation

Run these commands before opening a PR:

```bash
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

## Evaluation

- Use `evals/trigger-queries.json` for description-trigger checks.
- Use `evals/output-quality-checklist.md` during forward-testing or human review.
- Add or revise examples when the expected report structure changes materially.

## Out Of Scope

- Do not add shared-memory infrastructure to this repository.
- Do not add speculative frameworks, placeholder integrations, or untested scripts.
- Do not silently change the scoring model without updating the reference docs, examples, and tests together.
