import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FetchArxivTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fetch = load_script("fetch_arxiv")

    def test_norm_id_new_style_url_and_version(self):
        self.assertEqual(
            self.fetch._norm_id("https://arxiv.org/abs/2512.00565v2"),
            "2512.00565v2",
        )
        self.assertEqual(
            self.fetch._norm_id("https://arxiv.org/pdf/2512.00565"),
            "2512.00565",
        )

    def test_download_pdf_uses_original_pdf_contract(self):
        with tempfile.TemporaryDirectory() as td:
            calls = []

            def fake_get(url, binary=False):
                calls.append((url, binary))
                return b"%PDF-1.4\n%fake\n"

            old_get = self.fetch._get
            try:
                self.fetch._get = fake_get
                out = self.fetch.download_pdf("2512.00565", td)
            finally:
                self.fetch._get = old_get

            self.assertEqual(Path(out).name, "original.pdf")
            self.assertTrue(Path(out).exists())
            self.assertEqual(calls, [("https://arxiv.org/pdf/2512.00565", True)])


class RenderPdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render = load_script("render_pdf")

    def test_chrome_bin_override(self):
        old = os.environ.get("CHROME_BIN")
        os.environ["CHROME_BIN"] = "/bin/sh"
        try:
            self.assertEqual(self.render.find_chrome(), "/bin/sh")
        finally:
            if old is None:
                os.environ.pop("CHROME_BIN", None)
            else:
                os.environ["CHROME_BIN"] = old


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_script("validate_output")

    def run_check_html(self, html, manifest):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            html_path = work / "translation.html"
            html_path.write_text(html, encoding="utf-8")
            rep = self.validator.Report()
            self.validator.check_html(rep, str(html_path), str(work), str(work / "original.pdf"), manifest)
            return rep

    def test_placeholder_is_failure(self):
        rep = self.run_check_html(
            "<html><body><h1>Original English Paper Title</h1></body></html>",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(any("placeholder" in msg for level, msg in rep.items if level == "FAIL"))

    def test_display_equation_count_is_enforced(self):
        rep = self.run_check_html(
            "<html><body><h1>실제 제목</h1><pre>x = y</pre></body></html>",
            {"figures": [], "tables": [], "display_equations": 2},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(any("수식 누락" in msg for level, msg in rep.items if level == "FAIL"))

    def test_clean_html_contract_passes(self):
        rep = self.run_check_html(
            "<html><body><h1>실제 제목</h1><pre>x = y</pre></body></html>",
            {"figures": [], "tables": [], "display_equations": 1},
        )
        self.assertFalse(rep.failed)


if __name__ == "__main__":
    unittest.main()
