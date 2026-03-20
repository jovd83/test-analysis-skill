import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.+)$")
EXAMPLE_RE = re.compile(r"(.+)-(requirement|report)\.md$")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("No YAML frontmatter found at the top of SKILL.md.")
    frontmatter: dict[str, object] = {}
    current_parent: str | None = None
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue

        if raw_line.startswith("  "):
            if current_parent is None:
                raise ValueError(f"Unsupported frontmatter indentation: {raw_line}")
            entry = KEY_VALUE_RE.match(raw_line.strip())
            if not entry:
                raise ValueError(f"Unsupported nested frontmatter line: {raw_line}")
            parent = frontmatter.setdefault(current_parent, {})
            if not isinstance(parent, dict):
                raise ValueError(f"Frontmatter key '{current_parent}' cannot contain nested values.")
            parent[entry.group(1)] = entry.group(2).strip()
            continue

        if raw_line.startswith(" "):
            raise ValueError(f"Unsupported frontmatter indentation: {raw_line}")

        if raw_line.rstrip().endswith(":"):
            current_parent = raw_line.rstrip()[:-1].strip()
            if not current_parent:
                raise ValueError(f"Unsupported frontmatter line: {raw_line}")
            frontmatter[current_parent] = {}
            continue

        current_parent = None
        entry = KEY_VALUE_RE.match(raw_line.strip())
        if not entry:
            raise ValueError(f"Unsupported frontmatter line: {raw_line}")
        frontmatter[entry.group(1)] = entry.group(2).strip()
    body = text[match.end():].strip()
    return frontmatter, body


def validate_skill_md(root: Path, errors: list[str], warnings: list[str]) -> str | None:
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        errors.append("Missing SKILL.md.")
        return None

    lines = skill_path.read_text(encoding="utf-8").splitlines()
    if len(lines) > 500:
        warnings.append(f"SKILL.md is {len(lines)} lines; keep it under 500 lines when possible.")

    try:
        frontmatter, body = parse_frontmatter("\n".join(lines) + "\n")
    except ValueError as exc:
        errors.append(str(exc))
        return None

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not name:
        errors.append("SKILL.md frontmatter is missing 'name'.")
    elif not NAME_RE.match(name):
        errors.append("Skill name must use lowercase letters, digits, and hyphens only.")

    if not description:
        errors.append("SKILL.md frontmatter is missing 'description'.")
    else:
        if len(description) > 1024:
            errors.append("SKILL.md description exceeds 1024 characters.")
        if not description.startswith("Use when"):
            warnings.append("Description should begin with 'Use when' for strong trigger behavior.")

    if name and root.name != name:
        warnings.append(f"Skill directory '{root.name}' does not match SKILL.md name '{name}'.")

    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append("SKILL.md metadata must be a nested mapping when provided.")

    unexpected_keys = sorted(set(frontmatter) - {"name", "description", "metadata"})
    if unexpected_keys:
        warnings.append(f"SKILL.md uses extra frontmatter keys: {', '.join(unexpected_keys)}")

    if not body:
        errors.append("SKILL.md body is empty.")

    return name


def validate_agents_metadata(root: Path, skill_name: str | None, errors: list[str], warnings: list[str]) -> None:
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        errors.append("Missing agents/openai.yaml.")
        return

    text = load_text(path)
    required_snippets = [
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        "policy:",
        "allow_implicit_invocation:",
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"agents/openai.yaml is missing '{snippet}'.")

    if skill_name and f"${skill_name}" not in text:
        warnings.append("agents/openai.yaml default_prompt should mention the skill explicitly.")


def validate_examples(root: Path, errors: list[str], warnings: list[str]) -> None:
    example_dir = root / "examples"
    if not example_dir.exists():
        errors.append("Missing examples directory.")
        return

    groups: dict[str, set[str]] = {}
    for path in example_dir.glob("*.md"):
        match = EXAMPLE_RE.fullmatch(path.name)
        if not match:
            warnings.append(f"Example file '{path.name}' does not follow the '*-requirement.md' or '*-report.md' convention.")
            continue
        groups.setdefault(match.group(1), set()).add(match.group(2))

    if not groups:
        warnings.append("No example pairs found.")
        return

    for name, parts in sorted(groups.items()):
        if {"requirement", "report"} - parts:
            errors.append(f"Example '{name}' is missing a paired requirement or report file.")


def validate_required_paths(root: Path, errors: list[str]) -> None:
    required_paths = [
        ".github/workflows/ci.yml",
        ".gitignore",
        "README.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "memory/requirement-antipatterns.md",
        "references/analysis-framework.md",
        "references/risk-model.md",
        "scripts/calculate_risk.py",
        "scripts/export_report.py",
        "scripts/validate_skill.py",
        "evals/trigger-queries.json",
        "evals/output-quality-checklist.md",
        "tests/test_calculate_risk.py",
        "tests/test_export_report.py",
        "tests/test_validate_skill.py",
    ]
    for relative_path in required_paths:
        if not (root / relative_path).exists():
            errors.append(f"Missing required repository file: {relative_path}")


def validate(root: Path, strict: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    skill_name = validate_skill_md(root, errors, warnings)
    validate_required_paths(root, errors)
    validate_agents_metadata(root, skill_name, errors, warnings)
    validate_examples(root, errors, warnings)

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")

    if errors or (strict and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"SUCCESS: repository checks passed with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else Path.cwd()
    strict = "--strict" in sys.argv[1:]
    sys.exit(validate(root, strict=strict))
