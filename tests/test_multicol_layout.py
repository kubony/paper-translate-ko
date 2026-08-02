import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_multicol_layout.py"


def run_preflight(html: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "translation.html"
        path.write_text(html, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path)],
            check=False,
            capture_output=True,
            text=True,
        )


class MulticolLayoutTests(unittest.TestCase):
    def test_wide_table_heading_with_explicit_selectors_passes(self):
        result = run_preflight(
            """
            <style>
            h3.section { column-span: all; }
            table.wide { column-span: all; }
            </style>
            <h3 class="section">표 4. Local planner ablation</h3>
            <table class="wide"><tr><td>value</td></tr></table>
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_h3_span_reproduces_dualvln_failure(self):
        result = run_preflight(
            """
            <style>
            h2.section { column-span: all; }
            table.wide { column-span: all; }
            </style>
            <h3 class="section">표 4. Local planner ablation</h3>
            <table class="wide"><tr><td>value</td></tr></table>
            """
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("h3.section", result.stderr)

    def test_class_only_selectors_cover_multiple_element_types(self):
        result = run_preflight(
            """
            <style>
            .section { column-span: all; }
            .wide { column-span: all; }
            .fig-wide { column-span: all; }
            </style>
            <h2 class="section">Results</h2>
            <h3 class="section">Table title</h3>
            <table class="wide"></table>
            <figure class="fig-wide"></figure>
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
