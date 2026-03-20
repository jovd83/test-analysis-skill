from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import export_report


class ExportReportTests(unittest.TestCase):
    def test_markdown_to_html_renders_table(self) -> None:
        markdown = "# Report\n\n| A | B |\n| --- | --- |\n| 1 | 2 |"
        html = export_report.markdown_to_html(markdown)
        self.assertIn("<h1>Report</h1>", html)
        self.assertIn("<table>", html)
        self.assertIn("<td>2</td>", html)

    def test_export_html_writes_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "report.md"
            output = Path(temp_dir) / "report.html"
            source.write_text("# Demo\n\nA short report.", encoding="utf-8")
            export_report.export_html(str(source), str(output))
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("<title>Demo</title>", rendered)
            self.assertIn("<main>", rendered)


if __name__ == "__main__":
    unittest.main()
