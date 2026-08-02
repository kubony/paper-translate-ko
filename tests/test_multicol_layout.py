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

    def test_active_column_rule_with_spanning_content_fails(self):
        result = run_preflight(
            """
            <style>
            .paper-body { column-count: 2; column-rule: .35pt solid #ddd; }
            h2.section { column-span: all; }
            </style>
            <main class="paper-body"><h2 class="section">Review</h2></main>
            """
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("active column-rule", result.stderr)

    def test_column_rule_none_with_spanning_content_passes(self):
        result = run_preflight(
            """
            <style>
            .paper-body { column-count: 2; column-rule: none; }
            h2.section { column-span: all; }
            </style>
            <main class="paper-body"><h2 class="section">Review</h2></main>
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_fixed_offset_cover_separator_fails(self):
        result = run_preflight(
            """
            <style>
            .cover::after {
              content: ""; position: absolute; top: 77mm;
              left: 15mm; right: 11mm; height: 2px; background: navy;
            }
            </style>
            <section class="cover"><h1>Wrapped title</h1></section>
            """
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("flow-independent cover separator", result.stderr)

    def test_flow_anchored_cover_separator_passes(self):
        result = run_preflight(
            """
            <style>
            .cover h1 { padding-bottom: 5mm; border-bottom: 2px solid navy; }
            </style>
            <section class="cover"><h1>Wrapped title</h1></section>
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
