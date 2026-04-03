# Changelog

All notable changes to the `test-analysis-skill` repository are documented in this file.

The format follows Keep a Changelog with lightweight `Added`, `Changed`, and `Fixed` sections.

## [Unreleased]

### Added
- `## Gotchas` section to `SKILL.md` for better LLM instruction.
- Version, license, and 'Buy Me a Coffee' badges to `README.md`.

## [1.0.0] - 2026-03-18

### Added
- `agents/openai.yaml` metadata for UI-facing skill discovery.
- Repository-level validation and unit tests.
- Trigger-evaluation prompts and an output-quality checklist.
- Paired requirement and report examples with consistent naming.
- Explicit memory model documentation and a curated anti-pattern catalog.

### Changed
- Rewrote `SKILL.md` to tighten trigger language, guardrails, workflow, output contract, and memory behavior.
- Replaced the legacy reference docs with a clearer analysis framework and risk model.
- Upgraded helper scripts for stronger validation, deterministic risk scoring, and dependency-free HTML export.
- Rebuilt the README and contribution guidance for GitHub readiness and maintainability.

### Fixed
- Removed conflicting scoring guidance between the skill text, examples, and scripts.
- Eliminated encoding noise and inconsistent terminology across the repository.
- Clarified that memory updates are deliberate and auditable instead of implicitly self-modifying.

## [0.1.0] - 2026-03-17

### Added
- Initial public release of the `test-analysis-skill`.
- Core capabilities for Testability Analysis, Static Testing of Analysis, Risk Assessment, and Gap Analysis.
- Included structured scoring models (`Testability Score`, `Static Review Quality Score`, `Residual Risk Score`, `Completeness Score`).
- Defined matrix visualization patterns.
