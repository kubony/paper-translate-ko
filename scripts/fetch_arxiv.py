#!/usr/bin/env python3
"""arXiv 논문 PDF와 메타데이터를 내려받는다.

사용법:
    python3 fetch_arxiv.py <arxiv_id> <outdir>

동작:
    - https://arxiv.org/pdf/<id> 에서 PDF를 받아 <outdir>/<id>.pdf 로 저장한다.
    - https://export.arxiv.org/api/query?id_list=<id> 에서 Atom 응답을 파싱해
      제목/저자/초록/comment/발표정보(journal_ref, primary_category, 링크)를
      <outdir>/metadata.json 으로 저장한다.

표준 라이브러리만 사용한다 (urllib, xml, json, re). pymupdf 불필요.
"""
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"

UA = "Mozilla/5.0 (paper-translate-ko fetch_arxiv)"


def _norm_id(raw: str) -> str:
    """URL/버전 접미사가 붙은 입력을 순수 arXiv id로 정규화한다."""
    raw = raw.strip()
    # arxiv.org/abs/2512.00565v1 또는 arxiv.org/pdf/2512.00565 형태 처리
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", raw)
    if m:
        return m.group(1) + (m.group(2) or "")
    # old-style id (예: math/0603522)
    m = re.search(r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", raw)
    if m:
        return m.group(1) + (m.group(2) or "")
    return raw


def _get(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return data if binary else data.decode("utf-8", "replace")


def download_pdf(arxiv_id: str, outdir: str) -> str:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    pdf_path = os.path.join(outdir, f"{arxiv_id}.pdf")
    print(f"[fetch] PDF 다운로드: {url}")
    data = _get(url, binary=True)
    if not data[:5] == b"%PDF-":
        raise RuntimeError(f"PDF가 아닌 응답을 받았다 (앞 20바이트: {data[:20]!r})")
    with open(pdf_path, "wb") as f:
        f.write(data)
    print(f"[fetch] 저장 완료: {pdf_path} ({len(data):,} bytes)")
    return pdf_path


def fetch_metadata(arxiv_id: str, outdir: str) -> dict:
    # 버전 접미사는 API 조회 시 제거 (id_list는 버전 없는 id를 권장)
    base_id = re.sub(r"v\d+$", "", arxiv_id)
    url = f"https://export.arxiv.org/api/query?id_list={base_id}"
    print(f"[fetch] 메타데이터 조회: {url}")
    xml_text = _get(url)
    root = ET.fromstring(xml_text)
    entry = root.find(f"{ATOM}entry")
    if entry is None:
        raise RuntimeError("메타데이터 entry를 찾지 못했다")

    def _text(tag):
        el = entry.find(tag)
        return re.sub(r"\s+", " ", el.text).strip() if el is not None and el.text else ""

    authors = []
    for a in entry.findall(f"{ATOM}author"):
        name = a.find(f"{ATOM}name")
        aff = a.find(f"{ARXIV}affiliation")
        authors.append({
            "name": name.text.strip() if name is not None and name.text else "",
            "affiliation": aff.text.strip() if aff is not None and aff.text else "",
        })

    links = {}
    for l in entry.findall(f"{ATOM}link"):
        rel = l.get("rel", "")
        title = l.get("title", "")
        href = l.get("href", "")
        if title == "pdf" or rel == "alternate" or rel == "related":
            key = title or rel
            links[key] = href

    comment_el = entry.find(f"{ARXIV}comment")
    journal_el = entry.find(f"{ARXIV}journal_ref")
    primary_el = entry.find(f"{ARXIV}primary_category")

    categories = [c.get("term") for c in entry.findall(f"{ATOM}category")]

    meta = {
        "arxiv_id": arxiv_id,
        "title": _text(f"{ATOM}title"),
        "authors": authors,
        "abstract": _text(f"{ATOM}summary"),
        "comment": (re.sub(r"\s+", " ", comment_el.text).strip()
                    if comment_el is not None and comment_el.text else ""),
        "journal_ref": (journal_el.text.strip()
                        if journal_el is not None and journal_el.text else ""),
        "primary_category": (primary_el.get("term") if primary_el is not None else ""),
        "categories": categories,
        "published": _text(f"{ATOM}published"),
        "updated": _text(f"{ATOM}updated"),
        "abs_url": f"https://arxiv.org/abs/{base_id}",
        "pdf_url": f"https://arxiv.org/pdf/{base_id}",
        "links": links,
    }
    meta_path = os.path.join(outdir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"[fetch] 메타데이터 저장: {meta_path}")
    print(f"[fetch] 제목: {meta['title']}")
    print(f"[fetch] 저자: {', '.join(a['name'] for a in authors)}")
    return meta


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 1
    arxiv_id = _norm_id(argv[1])
    outdir = argv[2]
    os.makedirs(outdir, exist_ok=True)
    download_pdf(arxiv_id, outdir)
    fetch_metadata(arxiv_id, outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
