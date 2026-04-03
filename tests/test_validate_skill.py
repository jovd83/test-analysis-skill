from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate_skill


class ValidateSkillTests(unittest.TestCase):
    def test_parse_frontmatter(self) -> None:
        frontmatter, body = validate_skill.parse_frontmatter(
            "---\nname: demo-skill\ndescription: Use when checking a demo.\n---\n# Demo\n"
        )
        self.assertEqual(frontmatter["name"], "demo-skill")
        self.assertEqual(frontmatter["description"], "Use when checking a demo.")
        self.assertEqual(body, "# Demo")

    def test_validate_examples_detects_missing_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            examples = root / "examples"
            examples.mkdir()
            (examples / "demo-requirement.md").write_text("# Demo", encoding="utf-8")
            errors: list[str] = []
            warnings: list[str] = []
            validate_skill.validate_examples(root, errors, warnings)
            self.assertTrue(errors)
            self.assertFalse(warnings)

    def test_validate_required_paths_does_not_require_contributing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            required_paths = [
                ".github/workflows/ci.yml",
                ".gitignore",
                "README.md",
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
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")

            errors: list[str] = []
            validate_skill.validate_required_paths(root, errors)
            self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main()
