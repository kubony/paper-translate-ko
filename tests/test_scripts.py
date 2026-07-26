import importlib.util
import json
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


class SplitPdfForDeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.splitter = load_script("split_pdf_for_delivery")

    def test_split_covers_every_page_with_size_limit(self):
        fitz = self.splitter.fitz
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / "paper.pdf"
            source = fitz.open()
            for page_no in range(6):
                page = source.new_page()
                page.insert_text((72, 72), f"page {page_no + 1} " + ("content " * 500))
            source.save(source_path)
            source.close()

            check = fitz.open(source_path)
            try:
                one_page_size = len(self.splitter.render_range(check, 0, 0))
            finally:
                check.close()
            limit = one_page_size + 200
            results = self.splitter.split_pdf(source_path, root / "parts", limit)

            self.assertGreater(len(results), 1)
            covered = []
            for path, start, end, size in results:
                self.assertLessEqual(size, limit)
                self.assertTrue(path.exists())
                covered.extend(range(start, end + 1))
            self.assertEqual(covered, list(range(1, 7)))

    def test_rejects_limit_smaller_than_one_page(self):
        fitz = self.splitter.fitz
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path = root / "paper.pdf"
            source = fitz.open()
            source.new_page().insert_text((72, 72), "single page")
            source.save(source_path)
            source.close()
            with self.assertRaises(ValueError):
                self.splitter.split_pdf(source_path, root / "parts", 1)


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

    def test_high_confidence_machine_translation_residue_is_failure(self):
        phrases = (
            "손실은 훈련을 통해 건강하게 감소한다",
            "시각적 영역의 영향력 있는 변화가 있다",
            "시각적 영역의\n영향력 있는 변화가 있다",
            "평가 성능 저하를 예측할 수 있다고 예상할 수 있었다",
            "제작대를 제작할 수 있었다",
            "기술 트리에서는 이를 지나칠 수 없었다",
            "두 개의 더 좁은 데이터 세트로 fine-tuning한다",
            '데이터를 "깨끗함"이라고 부르고, 다른 모든 데이터는 "깨끗함"이라고 부른다',
            '데이터를 "clean"이라고 부르고,\n다른 모든 데이터는 "clean"이라고 부른다',
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                rep = self.run_check_html(
                    f"<html><body><h1>실제 제목</h1><p>{phrase}</p></body></html>",
                    {"figures": [], "tables": [], "display_equations": 0},
                )
                self.assertTrue(rep.failed)
                self.assertTrue(
                    any("기계번역 잔재" in msg for level, msg in rep.items if level == "FAIL")
                )

    def test_natural_academic_equivalents_are_not_flagged(self):
        rep = self.run_check_html(
            """<html><body><h1>실제 제목</h1>
            <p>loss는 안정적으로 감소한다. 데이터가 학습 분포 밖에 놓였을 수 있다.
            제작대를 만들었지만 기술 트리의 다음 단계로 나아가지는 못했다.
            범위가 더 좁은 두 데이터셋으로 fine-tuning한다.</p></body></html>""",
            {"figures": [], "tables": [], "display_equations": 0},
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


class FolderNameAndMediaAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_script("validate_output")

    def test_id_only_folder_name_fails(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "2410.01273"
            work.mkdir()
            rep = self.validator.Report()
            self.validator.check_folder_name(rep, str(work))
        self.assertTrue(rep.failed)

    def test_folder_name_with_title_slug_passes(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "2410.01273_CANVAS-Commonsense-Aware-Navigation"
            work.mkdir()
            rep = self.validator.Report()
            self.validator.check_folder_name(rep, str(work))
        self.assertFalse(rep.failed)

    def _media_workdir(self, td, html_body, local="assets/videos/demo.mp4", write_file=True):
        work = Path(td) / "2026-07-17_Sunday_ACT-2-Preview"
        (work / "assets" / "videos").mkdir(parents=True)
        if write_file:
            (work / local).write_bytes(b"\x00fake mp4 bytes")
        (work / "assets" / "videos.json").write_text(
            json.dumps({
                "fetched_on": "2026-07-17",
                "pages": [{"url": "https://example.com/blog"}],
                "assets": [{
                    "kind": "video",
                    "url": "https://example.com/demo.mp4",
                    "local": local,
                    "bytes": 14,
                }],
            }, ensure_ascii=False),
            encoding="utf-8",
        )
        html_path = work / "translation.html"
        html_path.write_text(html_body, encoding="utf-8")
        return work, html_path

    def test_unlinked_stored_video_fails(self):
        with tempfile.TemporaryDirectory() as td:
            work, html_path = self._media_workdir(td, "<html><body><p>본문만 있다.</p></body></html>")
            rep = self.validator.Report()
            self.validator.check_media_assets(rep, str(work), str(html_path))
        self.assertTrue(rep.failed)
        self.assertTrue(any("링크되어 있지 않다" in msg for level, msg in rep.items if level == "FAIL"))

    def test_linked_stored_video_passes(self):
        with tempfile.TemporaryDirectory() as td:
            work, html_path = self._media_workdir(
                td,
                '<html><body><a href="assets/videos/demo.mp4">레포 사본</a></body></html>',
            )
            rep = self.validator.Report()
            self.validator.check_media_assets(rep, str(work), str(html_path))
        self.assertFalse(rep.failed)

    def test_missing_asset_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            work, html_path = self._media_workdir(
                td,
                '<html><body><a href="assets/videos/demo.mp4">레포 사본</a></body></html>',
                write_file=False,
            )
            rep = self.validator.Report()
            self.validator.check_media_assets(rep, str(work), str(html_path))
        self.assertTrue(rep.failed)

    def test_no_manifest_means_no_media_check(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "2410.01273_Some-Title"
            work.mkdir()
            rep = self.validator.Report()
            self.validator.check_media_assets(rep, str(work), str(work / "translation.html"))
        self.assertEqual(rep.items, [])


class FetchWebAssetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fwa = load_script("fetch_web_assets")

    def test_extract_media_urls_handles_srcset_and_relative_paths(self):
        html = (
            '<video src="/media/demo.mp4" poster="/media/demo.jpg"></video>'
            '<img srcset="https://cdn.example.com/a-720x270.gif?w=450&amp;q=90 450w, '
            'https://cdn.example.com/a-720x270.gif?w=900&amp;q=90 900w">'
        )
        urls = self.fwa.extract_media_urls(html, "https://site.example/blog/post", self.fwa.MOTION_EXTS)
        self.assertIn("https://site.example/media/demo.mp4", urls)
        self.assertTrue(any(u.startswith("https://cdn.example.com/a-720x270.gif") for u in urls))
        self.assertFalse(any(u.endswith(".jpg") for u in urls))

    def test_extract_media_urls_unescapes_json_encoded_slashes(self):
        html = r'{"video":"https:\/\/cdn.example.com\/clip.mp4"}'
        urls = self.fwa.extract_media_urls(html, "https://site.example/", self.fwa.VIDEO_EXTS)
        self.assertEqual(urls, ["https://cdn.example.com/clip.mp4"])

    def test_extract_stream_pages_skips_channel_links(self):
        html = (
            '<a href="https://www.youtube.com/@SundayRobotics">channel</a>'
            '<a href="https://youtu.be/d7I1wj0Gkik">demo</a>'
            '<iframe src="https://www.youtube.com/embed/a2HZyURUE_o"></iframe>'
        )
        hits = self.fwa.extract_stream_pages(html)
        self.assertIn("https://youtu.be/d7I1wj0Gkik", hits)
        self.assertIn("https://www.youtube.com/embed/a2HZyURUE_o", hits)
        self.assertFalse(any("@SundayRobotics" in u for u in hits))

    def test_slugify_is_filesystem_safe_and_unique_per_url(self):
        a = self.fwa.slugify("https://cdn.example.com/a b/데모 영상.mp4")
        b = self.fwa.slugify("https://cdn.example.com/other/데모 영상.mp4")
        self.assertNotIn(" ", a)
        self.assertNotEqual(a, b)
        self.assertTrue(a.startswith("데모-영상-"))

    def test_context_for_returns_preceding_visible_text(self):
        html = "<p>애호박을 절단하는 데모다.</p><video src='https://x.example/clip.mp4'></video>"
        context = self.fwa.context_for(html, "https://x.example/clip.mp4")
        self.assertIn("애호박", context)

    def test_write_manifest_and_assets_md(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "assets"
            out.mkdir()
            entries = [{
                "kind": "video",
                "url": "https://x.example/clip.mp4",
                "local": "assets/videos/clip.mp4",
                "bytes": 2 * 1024 * 1024,
                "duration_s": 12.0,
                "context": "애호박 절단 데모",
            }]
            manifest = self.fwa.write_manifest(out, [{"url": "https://x.example/post"}], entries)
            assets_md = self.fwa.write_assets_md(out, [{"url": "https://x.example/post"}], entries)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            md = assets_md.read_text(encoding="utf-8")
        self.assertEqual(data["assets"][0]["local"], "assets/videos/clip.mp4")
        self.assertIn("https://x.example/clip.mp4", md)
        self.assertIn("애호박 절단 데모", md)


class SourceResidueTests(unittest.TestCase):
    """번역 원문을 LaTeX 소스·마크다운·DOM에서 뽑았을 때의 잔재 검사.

    실제 산출물 15편 재검토에서 기존 검사가 통과시킨 실패들을 회귀 고정한다.
    """

    @classmethod
    def setUpClass(cls):
        cls.v = load_script("validate_output")

    def residue(self, text):
        rep = self.v.Report()
        self.v.check_source_residue(rep, text, "테스트")
        return rep

    def fails(self, rep):
        return [msg for level, msg in rep.items if level == "FAIL"]

    def warns(self, rep):
        return [msg for level, msg in rep.items if level == "WARN"]

    def test_clean_korean_body_passes_every_check(self):
        rep = self.residue(
            "그림 1. 시스템 개요.\n표 1. 정량 비교.\n"
            "본 논문은 그림 1과 표 1에서 제안 기법의 성능을 보인다.\n"
        )
        self.assertFalse(rep.failed, msg=f"오탐: {self.fails(rep)}")

    def test_backslash_stripped_latex_macro_is_failure(self):
        # CostNav 회귀: `\noindent`가 `noindent`로 남아 LATEX_REMNANT를 빠져나갔다.
        rep = self.residue("noindent비용 인식 로봇공학.기존 연구에서는 toprule midrule 를 쓴다.")
        self.assertTrue(any("LaTeX 매크로 잔재" in m for m in self.fails(rep)))

    def test_ordinary_korean_text_is_not_bare_latex(self):
        rep = self.residue("이 절은 표 형식과 항목 나열을 설명한다. quadruped robot을 다룬다.")
        self.assertFalse(any("LaTeX 매크로 잔재" in m for m in self.fails(rep)))

    def test_ref_label_exposure_is_failure(self):
        rep = self.residue("자세한 내용은 부록 sec:cost_parameters와 표 tab:baselines에 있다.")
        self.assertTrue(any("label 참조 노출" in m for m in self.fails(rep)))

    def test_markdown_table_separator_is_failure(self):
        # SC3-Eval 회귀: 표가 조판되지 않고 마크다운 원문으로 인쇄됐다.
        rep = self.residue("| 방법 | 점수 |\n|---|---:|\n| Ctrl-World | 0.878 |")
        self.assertTrue(any("마크다운 표" in m for m in self.fails(rep)))

    def test_caption_with_source_filename_is_failure(self):
        # SC3-Eval 회귀: 캡션이 번역되지 않고 원본 파일명 그대로였다.
        rep = self.residue("원문 피겨. teaser_v6.png\n그림 2. corr_v3.png")
        self.assertTrue(any("캡션에 원본 파일명" in m for m in self.fails(rep)))

    def test_template_null_residue_over_limit_is_failure(self):
        # PI_website 회귀: 값 없는 항목이 걸러지지 않아 113건이 인쇄됐다.
        rep = self.residue("동영상 1 - 원본 URL: 없음(null)\n" * 4)
        self.assertTrue(any("템플릿 자리표시 잔재" in m for m in self.fails(rep)))

    def test_template_null_residue_under_limit_is_warning_only(self):
        rep = self.residue("동영상 1 - 원본 URL: 없음(null)")
        self.assertFalse(rep.failed)
        self.assertTrue(any("템플릿 자리표시 잔재" in m for m in self.warns(rep)))

    def test_duplicated_caption_is_failure(self):
        # HABIT 회귀: 번역 캡션과 원문 캡션이 겹쳐 인쇄됐다.
        rep = self.residue("그림 1. 그림 1: HABIT는 60가지 작업을 다룬다.")
        self.assertTrue(any("캡션 중복 인쇄" in m for m in self.fails(rep)))

    def test_duplicated_section_number_is_failure(self):
        rep = self.residue("1. 1 소개\n2.1 2.1 태스크 설계\n")
        self.assertTrue(any("섹션 번호 중복" in m for m in self.fails(rep)))

    def test_repeated_table_numbers_are_not_section_numbers(self):
        # 표의 반복 수치(`53.3 53.3 8`)를 섹션 번호 중복으로 오탐하지 않는다.
        rep = self.residue("성능 비교는 다음과 같다.\n53.3 53.3 8\n12.5 12.5 4\n")
        self.assertFalse(any("섹션 번호 중복" in m for m in self.fails(rep)))

    def test_missing_table_captions_are_failure(self):
        # KOFFVQA 회귀: 본문이 표 1~3을 참조하나 `표 N.` 캡션이 하나도 없었다.
        rep = self.residue(
            "정렬된 평가 결과는 표 1에 제공된다. 표 2와 표 3은 부록에 있다.\n"
            "그림 1. 카테고리 분포.\n그림 2. 범주별 예시.\n"
        )
        self.assertTrue(any("캡션이 하나도 없다" in m for m in self.fails(rep)))

    def test_panel_sublabel_captions_satisfy_base_number_reference(self):
        # act2 회귀: 캡션이 `그림 3a/3b/3c`로 쪼개져도 `그림 3` 참조는 충족된 것이다.
        rep = self.residue(
            "그림 1. 개요.\n그림 3a. 좌측 패널.\n그림 3b. 중앙 패널.\n"
            "그림 3에서 보듯 성능이 향상된다.\n"
        )
        self.assertFalse(rep.failed, msg=f"오탐: {self.fails(rep)}")

    def test_untranslated_english_prose_is_warning(self):
        # LLM_Novel 회귀: 원문 영어 문단이 통째로 남았다.
        rep = self.residue(
            "본문은 한국어로 이어진다.\n\n"
            "While the original experiment from Bai et al. used a points system for\n"
            "successful job assignments to incentivize the participants, these incentives\n"
            "are not necessary for the models that we have evaluated in this work here.\n"
        )
        self.assertTrue(any("영어 블록" in m for m in self.warns(rep)))

    def test_english_table_header_is_not_flagged_as_prose(self):
        # 표 헤더·저자 명단은 한글이 없어도 정상이므로 걸리지 않아야 한다.
        rep = self.residue(
            "표 1. 비교.\n표 2. 결과.\n"
            "Method Params VLA Pt Spatial Object Goal Total Octo Model Team 93M Yes 78.9 85.2\n"
            "Bo Ai Ali Amin Ashwin Balakrishna Greg Balke Kevin Black George Cheng Danny Driess\n"
        )
        self.assertFalse(any("영어 블록" in m for m in self.warns(rep)))

    def test_english_after_bibliography_heading_is_ignored(self):
        rep = self.residue(
            "본문이다.\n참고문헌\n"
            "Brohan et al. that this is the reference title of the paper which we cite for\n"
            "the purposes of this work and these results are from the original authors here.\n"
        )
        self.assertFalse(any("영어 블록" in m for m in self.warns(rep)))


if __name__ == "__main__":
    unittest.main()
