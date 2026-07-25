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

    def assert_formula_remnant_fails(self, formula):
        rep = self.run_check_html(
            f"<html><body><h1>실제 제목</h1><pre>{formula}</pre></body></html>",
            {"figures": [], "tables": [], "display_equations": 1},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(
            any("수식 변환 잔재" in msg for level, msg in rep.items if level == "FAIL")
        )

    def test_korean_screen_reader_subscript_labels_fail_in_formula(self):
        for label in ("아래 첨자", "아래   첨자", "하위\n첨자", "위 첨자"):
            with self.subTest(label=label):
                self.assert_formula_remnant_fails(f"p_IDM(a_t | o_t) {label} t")

    def test_latexml_structure_artifacts_fail_in_formula(self):
        for token in ("Formulae-sequence", "formulae sequence", "leavevmode", "similar-to"):
            with self.subTest(token=token):
                self.assert_formula_remnant_fails(f"p_IDM(a_t | o_t) {token}")

    def test_latexml_accessibility_commands_fail_in_formula(self):
        for token in ("textsubscript", "textrm"):
            with self.subTest(token=token):
                self.assert_formula_remnant_fails(f"p_{{{token}(IDM)}}(a_t | o_t)")

    def test_english_screen_reader_script_labels_fail_in_formula(self):
        for token in ("superscript", "subscript"):
            with self.subTest(token=token):
                self.assert_formula_remnant_fails(f"x_t = y {token} t")

    def test_formula_terms_in_legitimate_explanatory_prose_are_not_flagged(self):
        rep = self.run_check_html(
            """<html><body><h1>실제 제목</h1>
            <p>아래첨자는 변수의 색인을 나타낸다. In English, subscript and
            superscript are ordinary typography terms; textrm is discussed by name.</p>
            </body></html>""",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertFalse(rep.failed)

    def test_compact_korean_term_in_formula_markup_is_not_flagged(self):
        rep = self.run_check_html(
            """<html><body><h1>실제 제목</h1>
            <pre>x_t에서 <span>아래</span><span>첨자</span>는 색인을 나타낸다.</pre>
            </body></html>""",
            {"figures": [], "tables": [], "display_equations": 1},
        )
        self.assertFalse(rep.failed)

    def test_formula_tokens_in_comments_css_and_metadata_are_not_flagged(self):
        rep = self.run_check_html(
            """<html><head><meta name="description" content="textsubscript superscript">
            <style>.subscript::after { content: "leavevmode 아래 첨자"; }</style></head>
            <body><!-- Formulae-sequence textrm similar-to --><h1>실제 제목</h1></body></html>""",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertFalse(rep.failed)

    def test_raw_latex_in_visible_html_is_failure(self):
        rep = self.run_check_html(
            r"<html><body><h1>실제 제목</h1><p>결과는 \frac{x}{y}이다.</p></body></html>",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(any("LaTeX 잔재" in msg for level, msg in rep.items if level == "FAIL"))

    def test_common_visible_latex_commands_are_failures_without_an_allowlist(self):
        for command in (
            r"\sqrt{x}", r"\theta", r"\theta이다", r"\hat{x}", r"\overline{x}", r"\infty", r"\ell",
        ):
            with self.subTest(command=command):
                rep = self.run_check_html(
                    f"<html><body><h1>실제 제목</h1><p>{command}</p></body></html>",
                    {"figures": [], "tables": [], "display_equations": 0},
                )
                self.assertTrue(rep.failed)
                self.assertTrue(
                    any("LaTeX 잔재" in msg for level, msg in rep.items if level == "FAIL")
                )

    def test_visible_dollar_delimited_latex_is_failure(self):
        rep = self.run_check_html(
            "<html><body><h1>실제 제목</h1><p>$$ x = y $$</p></body></html>",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(any("LaTeX 잔재" in msg for level, msg in rep.items if level == "FAIL"))

    def test_raw_latex_in_comments_and_css_is_not_flagged(self):
        rep = self.run_check_html(
            r"""<html><head><style>.math::after { content: "\\frac"; }</style></head>
            <body><!-- $$ \\mathbb{R} --><h1>실제 제목</h1></body></html>""",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertFalse(rep.failed)

    def test_aria_hidden_visible_latex_is_still_failure(self):
        rep = self.run_check_html(
            r'<html><body><h1>실제 제목</h1><span aria-hidden="true">\sqrt{x}</span></body></html>',
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertTrue(rep.failed)
        self.assertTrue(any("LaTeX 잔재" in msg for level, msg in rep.items if level == "FAIL"))

    def test_br_and_block_boundaries_preserve_formula_word_boundaries(self):
        for markup in (
            "<pre>x = y<br>textsubscript<br>IDM</pre>",
            "<pre>x = y<div>textsubscript</div><div>IDM</div></pre>",
        ):
            with self.subTest(markup=markup):
                rep = self.run_check_html(
                    f"<html><body><h1>실제 제목</h1>{markup}</body></html>",
                    {"figures": [], "tables": [], "display_equations": 1},
                )
                self.assertTrue(rep.failed)
                self.assertTrue(
                    any("수식 변환 잔재" in msg for level, msg in rep.items if level == "FAIL")
                )

    def test_visible_extraction_preserves_br_and_block_boundaries(self):
        visible, _ = self.validator._visible_html_text(
            "<p>alpha<br>beta</p><div>gamma</div>"
        )
        self.assertIn("alpha\nbeta", visible)
        self.assertRegex(visible, r"beta\n+gamma")

    def test_inline_spans_do_not_insert_structural_whitespace(self):
        visible, formula = self.validator._visible_html_text(
            "<pre>x_t에서 <span>아래</span><span>첨자</span>는 색인을 나타낸다.</pre>"
        )
        self.assertIn("아래첨자", visible)
        self.assertIn("아래첨자", formula)

    def test_inline_code_terminology_is_not_implicitly_formula_context(self):
        rep = self.run_check_html(
            "<html><body><h1>실제 제목</h1><p><code>textsubscript</code>는 용어다.</p></body></html>",
            {"figures": [], "tables": [], "display_equations": 0},
        )
        self.assertFalse(rep.failed)

    def test_explicit_formula_contexts_still_detect_artifacts(self):
        for markup in (
            "<pre>x = textsubscript IDM</pre>",
            "<math>x = textsubscript IDM</math>",
            '<span role="math">x = textsubscript IDM</span>',
            '<code class="equation">x = textsubscript IDM</code>',
        ):
            with self.subTest(markup=markup):
                rep = self.run_check_html(
                    f"<html><body><h1>실제 제목</h1>{markup}</body></html>",
                    {"figures": [], "tables": [], "display_equations": int(markup.startswith("<pre"))},
                )
                self.assertTrue(rep.failed)
                self.assertTrue(
                    any("수식 변환 잔재" in msg for level, msg in rep.items if level == "FAIL")
                )

    def test_pdf_formula_context_retains_neighboring_wrapped_line(self):
        selected = self.validator._pdf_formula_text("p_IDM(a_t | o_t) =\ntextsubscript IDM")
        self.assertIn("textsubscript IDM", selected)

    def test_pdf_formula_context_excludes_neighboring_explanatory_sentence(self):
        for explanation in (
            "The word subscript is an ordinary typography term.",
            "The subscript t denotes the timestep",
        ):
            with self.subTest(explanation=explanation):
                selected = self.validator._pdf_formula_text(
                    f"p_IDM(a_t | o_t) = 0.5\n{explanation}"
                )
                self.assertNotIn(explanation, selected)

    def test_pdf_formula_line_with_single_script_term_is_not_artifact(self):
        text = "The subscript t in x_t denotes the timestep."
        self.assertEqual(self.validator._pdf_formula_remnant_hits(text), [])

    def test_pdf_weak_script_terms_do_not_accumulate_across_document(self):
        text = (
            "The subscript t in x_t denotes the timestep.\n"
            "The subscript k in z_k denotes the rollout step."
        )
        self.assertEqual(self.validator._pdf_formula_remnant_hits(text), [])

    def _write_pdf(self, path, text):
        doc = self.validator.fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), text)
        doc.save(path)
        doc.close()

    def test_generated_pdf_formula_artifact_regression(self):
        with tempfile.TemporaryDirectory() as td:
            orig = Path(td) / "original.pdf"
            final = Path(td) / "final.pdf"
            self._write_pdf(orig, "Original paper body")
            self._write_pdf(final, "p_IDM(a_t | o_t) = textsubscript IDM")
            rep = self.validator.Report()
            self.validator.check_final_pdf(rep, str(final), str(orig))
        self.assertTrue(rep.failed)
        self.assertTrue(
            any("수식 변환 잔재" in msg for level, msg in rep.items if level == "FAIL")
        )

    def test_generated_pdf_formula_artifact_on_wrapped_neighbor_line(self):
        with tempfile.TemporaryDirectory() as td:
            orig = Path(td) / "original.pdf"
            final = Path(td) / "final.pdf"
            self._write_pdf(orig, "Original paper body")
            self._write_pdf(final, "p_IDM(a_t | o_t) =\ntextsubscript IDM")
            rep = self.validator.Report()
            self.validator.check_final_pdf(rep, str(final), str(orig))
        self.assertTrue(rep.failed)
        self.assertTrue(
            any("수식 변환 잔재" in msg for level, msg in rep.items if level == "FAIL")
        )

    def test_generated_pdf_explanatory_term_is_not_formula_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            orig = Path(td) / "original.pdf"
            final = Path(td) / "final.pdf"
            self._write_pdf(orig, "Original paper body")
            self._write_pdf(final, "The word subscript is an ordinary typography term.")
            rep = self.validator.Report()
            self.validator.check_final_pdf(rep, str(final), str(orig))
        self.assertFalse(rep.failed)


if __name__ == "__main__":
    unittest.main()
