#!/usr/bin/env python3
"""웹 아티클/프로젝트 페이지의 영상·이미지 자산을 수집해 작업 폴더에 보관한다.

사용법:
    python3 fetch_web_assets.py --out <작업폴더>/assets <page_url> [<page_url> ...]
        [--max-mib N] [--include-images] [--no-thumbnails] [--dry-run]

동작:
    1. 헤드리스 Chrome으로 각 페이지를 렌더해 DOM을 얻는다(JS로 주입되는
       <video>/<source>도 잡기 위함). Chrome이 없으면 정적 HTML로 폴백한다.
    2. DOM과 원본 HTML에서 mp4/webm/mov/m3u8(및 --include-images 시 이미지)
       URL을 추출하고 base URL로 절대화한다.
    3. 각 자산을 내려받아 `videos/`(또는 `images/`)에 저장하고, ffmpeg로
       썸네일 첫 프레임을, ffprobe로 길이·해상도를 기록한다.
    4. `videos.json` 매니페스트와 사람이 읽는 `ASSETS.md`를 쓴다.
       매니페스트의 `local` 경로는 번역 HTML에서 그대로 링크할 수 있도록
       작업 폴더 기준 상대경로다.

표준 라이브러리 + 외부 실행파일(chrome/ffmpeg/ffprobe/yt-dlp)만 쓴다. pymupdf 불필요.
ffmpeg/ffprobe/yt-dlp가 없으면 해당 단계만 건너뛰고 나머지는 진행한다.
"""
import argparse
import hashlib
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

UA = "Mozilla/5.0 (paper-translate-ko fetch_web_assets)"

VIDEO_EXTS = ("mp4", "webm", "mov", "m4v", "m3u8")
# 애니메이션 GIF는 기술 블로그에서 데모 영상 대용으로 쓰인다 — 영상과 같이 취급한다.
MOTION_EXTS = VIDEO_EXTS + ("gif",)
IMAGE_EXTS = ("png", "jpg", "jpeg", "webp", "svg")

CHROME_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

STREAM_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")


# ---- 유틸 ---------------------------------------------------------------
def find_chrome() -> str | None:
    """Chrome/Chromium 실행 경로를 찾는다. CHROME_BIN 환경변수가 우선."""
    env = os.environ.get("CHROME_BIN")
    if env:
        return env if os.path.exists(env) or shutil.which(env) else None
    for cand in CHROME_CANDIDATES:
        if os.path.isabs(cand):
            if os.path.exists(cand):
                return cand
        elif shutil.which(cand):
            return cand
    return None


def slugify(url: str, fallback: str = "asset") -> str:
    """URL을 파일명으로 쓸 수 있는 slug로 바꾼다. 충돌 방지용 해시 접미사를 붙인다."""
    path = urllib.parse.urlsplit(url).path
    stem = Path(urllib.parse.unquote(path)).stem or fallback
    stem = re.sub(r"[^0-9A-Za-z가-힣._-]+", "-", stem).strip("-._") or fallback
    stem = stem[:60]
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:6]
    return f"{stem}-{digest}"


def _strip_tags(fragment: str) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", fragment)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = _html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def context_for(html: str, url: str, window: int = 1500, limit: int = 220) -> str:
    """자산 URL 직전의 본문 텍스트를 캡션 후보로 뽑는다."""
    idx = html.find(url)
    if idx < 0:
        return ""
    text = _strip_tags(html[max(0, idx - window):idx])
    return text[-limit:].strip()


def extract_media_urls(html: str, base_url: str, exts: tuple[str, ...]) -> list[str]:
    """HTML/DOM 문자열에서 주어진 확장자의 미디어 URL을 순서대로 중복 없이 뽑는다.

    <video src>, <source src>, poster=, og:video, 본문/스크립트에 하드코딩된
    절대·상대 URL을 모두 대상으로 한다.
    """
    text = _html.unescape(html.replace("\\/", "/"))
    candidates: list[str] = []

    # 1) 속성값 — 상대경로와 srcset(쉼표로 구분된 "url 450w" 목록)까지 포함한다.
    attr_re = r"""(?i)\b(?:src|srcset|href|poster|content|data-src|data-video|data-poster)\s*=\s*["']([^"']+)["']"""
    for value in re.findall(attr_re, text):
        for part in value.split(","):
            token = part.strip().split()[0] if part.strip() else ""
            if token:
                candidates.append(token)

    # 2) 스크립트/JSON에 하드코딩된 절대 URL. 인용부호로 끝나지 않는 경우가 많아
    #    (srcset 항목, 마크다운 링크 등) 토큰 단위로 훑는다.
    candidates += re.findall(r"""(?i)https?://[^\s"'<>()\[\]\\]+""", text)

    found: list[str] = []
    seen: set[str] = set()
    for raw in candidates:
        candidate = raw.strip().rstrip(".,;)>\"'")
        if not candidate:
            continue
        if candidate.startswith("//"):
            candidate = urllib.parse.urlsplit(base_url).scheme + ":" + candidate
        absolute = urllib.parse.urljoin(base_url, candidate)
        if not absolute.lower().startswith(("http://", "https://")):
            continue
        ext = Path(urllib.parse.urlsplit(absolute).path).suffix.lower().lstrip(".")
        if ext not in exts:
            continue
        if absolute in seen:
            continue
        seen.add(absolute)
        found.append(absolute)
    return found


def _stream_id(url: str) -> str:
    """YouTube/Vimeo URL에서 영상 id를 뽑는다(중복 제거용)."""
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc.lower()
    if host.endswith("youtu.be"):
        return parts.path.strip("/")
    if host.endswith("youtube.com"):
        if parts.path.startswith("/embed/"):
            return parts.path.split("/embed/", 1)[1].strip("/")
        return urllib.parse.parse_qs(parts.query).get("v", [""])[0]
    return parts.path.strip("/")


def extract_stream_pages(html: str) -> list[str]:
    """YouTube/Vimeo 단일 영상 URL을 뽑는다(yt-dlp로 내려받는 대상).

    채널·계정·플레이리스트 링크(`/@handle`, `/channel/`, `/c/`, `/user/`)는
    영상이 아니므로 제외한다.
    """
    hits: list[str] = []
    seen: set[str] = set()
    seen_ids: set[str] = set()
    non_video = ("/@", "/channel/", "/c/", "/user/", "/results")
    for raw in re.findall(r"""(?i)["'(](https?://[^"'\s)]+)["')]""", html):
        url = raw.replace("\\/", "/").rstrip("\\,.")
        parts = urllib.parse.urlsplit(url)
        host = parts.netloc.lower()
        if not any(host.endswith(h) for h in STREAM_HOSTS):
            continue
        if any(marker in parts.path for marker in non_video):
            continue
        if host.endswith("youtube.com") and parts.path not in ("/watch", "/embed") and not parts.path.startswith("/embed/"):
            continue
        if url in seen:
            continue
        video_id = _stream_id(url)
        if video_id and video_id in seen_ids:
            continue  # 같은 영상의 다른 URL 형태 — 한 번만 받는다
        seen.add(url)
        if video_id:
            seen_ids.add(video_id)
        hits.append(url)
    return hits


def decode_js_text(value: str) -> str:
    r"""JSON/JS 문자열 이스케이프(\uXXXX, \n, \t)를 사람이 읽는 문자로 되돌린다.

    RSC payload에서 뽑은 제목에는 `\u003cP0/ \u003e ALOHA folding a towel`처럼
    이스케이프된 마크업이 섞인다. 디코드한 뒤 남는 태그는 제거한다.
    """
    try:
        value = json.loads(f'"{value}"')
    except json.JSONDecodeError:
        value = value.replace("\\n", " ").replace("\\t", " ")
    value = re.sub(r"<[^>]*>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_titles(html: str, base_url: str) -> dict[str, str]:
    """영상 URL에 붙은 원문 제목을 뽑는다.

    Next.js/React 사이트는 RSC payload에 `{"url":"....mp4","title":"Cutting a zucchini"}`
    형태로 캡션을 싣는 경우가 많다. 이 제목이 있으면 캡션을 추측하지 않아도 된다.
    payload가 JS 문자열 안에 들어가면 따옴표가 `\"`로 이스케이프되므로 먼저 푼다.
    """
    text = _html.unescape(html.replace("\\/", "/").replace('\\"', '"'))
    titles: dict[str, str] = {}
    # 캡션이 담기는 키는 사이트마다 다르다(title / description / caption / alt).
    caption_keys = "title|description|caption|alt|label"
    url_keys = "url|src|asset|video|videoUrl|source"
    pairs = [
        rf'"(?:{url_keys})"\s*:\s*"([^"]+?)"\s*,\s*"(?:{caption_keys})"\s*:\s*"([^"]*?)"',
    ]
    reversed_pairs = [
        rf'"(?:{caption_keys})"\s*:\s*"([^"]*?)"\s*,\s*"(?:{url_keys})"\s*:\s*"([^"]+?)"',
    ]
    found: list[tuple[str, str]] = []
    for pat in pairs:
        found += re.findall(pat, text)
    for pat in reversed_pairs:
        found += [(u, t) for t, u in re.findall(pat, text)]
    # <video title="..."> / aria-label
    for attrs in re.findall(r"(?is)<video\b([^>]*)>", text):
        src = re.search(r"""src\s*=\s*["']([^"']+)["']""", attrs)
        label = re.search(r"""(?:title|aria-label)\s*=\s*["']([^"']+)["']""", attrs)
        if src and label:
            found.append((src.group(1), label.group(1)))

    for url, title in found:
        title = decode_js_text(title)
        if not title:
            continue
        absolute = urllib.parse.urljoin(base_url, url.strip())
        titles.setdefault(absolute, title)
    return titles


def portable_text_caption(html: str, asset_url: str, window: int = 1600) -> str:
    """Sanity portable text로 실린 캡션을 뽑는다.

    Sanity(anthropic.com 등)는 `"asset":{"_ref":"image-<hash>-480x360-gif"}` 뒤에
    `"caption":[{...,"children":[{"text":"..."}]}]` 블록을 둔다. 자산 참조 뒤쪽
    구간에서 caption 블록의 text 조각을 이어 붙인다.
    """
    text = _html.unescape(html.replace("\\/", "/").replace('\\"', '"'))
    stem = Path(urllib.parse.urlsplit(asset_url).path).stem
    if not stem:
        return ""
    # 같은 자산이 여러 번(썸네일 srcset 등) 등장하므로, caption 블록이 뒤따르는
    # 첫 번째 참조를 쓴다.
    start = 0
    while True:
        idx = text.find(stem, start)
        if idx < 0:
            return ""
        start = idx + len(stem)
        tail = text[idx: idx + window]
        cap = tail.find('"caption"')
        if cap < 0:
            continue
        pieces = re.findall(r'"text"\s*:\s*"([^"]*)"', tail[cap: cap + window])
        caption = " ".join(piece.strip() for piece in pieces if piece.strip()).strip()
        if caption:
            return caption


# ---- 페이지 로드 ---------------------------------------------------------
def fetch_static(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="replace")


def render_dom(url: str, timeout: int = 45, virtual_time_ms: int = 12000) -> str:
    """헤드리스 Chrome으로 렌더된 DOM을 얻는다. 실패하면 빈 문자열.

    render_pdf.py와 같은 이유로 Popen을 쓴다 — 일부 macOS Chrome 빌드는 DOM을
    stdout에 쓴 뒤에도 스스로 종료하지 않는다. timeout이 지나면 강제 종료하고
    그때까지 버퍼에 담긴 DOM을 사용한다.
    """
    chrome = find_chrome()
    if not chrome:
        return ""
    user_data = tempfile.mkdtemp(prefix="chrome-assets-")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={user_data}",
        f"--virtual-time-budget={virtual_time_ms}",
        "--dump-dom",
        url,
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except OSError:
        shutil.rmtree(user_data, ignore_errors=True)
        return ""
    try:
        out, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
    finally:
        shutil.rmtree(user_data, ignore_errors=True)
    return (out or b"").decode("utf-8", errors="replace")


def page_sources(url: str) -> tuple[str, str]:
    """(dom, static_html)을 반환한다. 둘 다에서 자산을 찾아 합친다."""
    dom = render_dom(url)
    try:
        static = fetch_static(url)
    except (urllib.error.URLError, OSError, TimeoutError):
        static = ""
    return dom, static


# ---- 다운로드/프로브 -----------------------------------------------------
def head_size(url: str, timeout: int = 30) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.headers.get("Content-Length") or 0)
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return 0


def download(url: str, dest: Path, timeout: int = 600) -> int:
    """URL을 dest로 스트리밍 저장하고 바이트 수를 돌려준다."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    total = 0
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as fh:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)
            total += len(chunk)
    return total


def download_stream(url: str, dest_stem: Path, timeout: int = 900) -> Path | None:
    """m3u8/YouTube/Vimeo는 yt-dlp에 위임한다. 실패하면 None."""
    if not shutil.which("yt-dlp"):
        return None
    dest_stem.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp", "--quiet", "--no-warnings", "--no-playlist",
        "-f", "mp4/best", "-o", f"{dest_stem}.%(ext)s", url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    hits = sorted(dest_stem.parent.glob(f"{dest_stem.name}.*"))
    return hits[0] if hits else None


def stream_title(url: str, timeout: int = 120) -> str:
    """YouTube/Vimeo 영상의 원문 제목을 얻는다. 캡션 근거가 된다."""
    if not shutil.which("yt-dlp"):
        return ""
    cmd = ["yt-dlp", "--quiet", "--no-warnings", "--skip-download", "--print", "title", url]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout.decode("utf-8", errors="replace").strip().splitlines()[0] if proc.stdout.strip() else ""


def probe(path: Path) -> dict:
    """ffprobe로 길이·해상도를 얻는다. 없으면 빈 dict."""
    if not shutil.which("ffprobe"):
        return {}
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
        data = json.loads(proc.stdout.decode("utf-8", errors="replace") or "{}")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return {}
    info: dict = {}
    duration = (data.get("format") or {}).get("duration")
    if duration:
        info["duration_s"] = round(float(duration), 2)
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            info["width"] = stream.get("width")
            info["height"] = stream.get("height")
            break
    return info


def make_thumbnail(video: Path, out: Path, at_seconds: float = 1.0) -> bool:
    """영상 첫 프레임을 JPEG 썸네일로 뽑는다."""
    if not shutil.which("ffmpeg"):
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-ss", str(at_seconds), "-i", str(video),
        "-frames:v", "1", "-vf", "scale=640:-2", str(out),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return False
    if proc.returncode != 0 or not out.exists():
        # 짧은 영상은 1초 지점이 없을 수 있다 — 0초로 재시도.
        cmd[cmd.index("-ss") + 1] = "0"
        try:
            subprocess.run(cmd, capture_output=True, timeout=180)
        except (OSError, subprocess.TimeoutExpired):
            return False
    return out.exists() and out.stat().st_size > 0


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ---- 매니페스트 ----------------------------------------------------------
def write_manifest(out_dir: Path, pages: list[dict], entries: list[dict]) -> Path:
    path = out_dir / "videos.json"
    payload = {
        "fetched_on": date.today().isoformat(),
        "pages": pages,
        "assets": entries,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_assets_md(out_dir: Path, pages: list[dict], entries: list[dict]) -> Path:
    """번역문에서 참조할 사람이 읽는 자산 목록을 쓴다."""
    lines = ["# 원문 미디어 자산", ""]
    lines.append(f"수집일: {date.today().isoformat()}")
    lines.append("")
    lines.append("출처 페이지:")
    for page in pages:
        lines.append(f"- {page['url']}")
    lines.append("")
    videos = [e for e in entries if e["kind"] in ("video", "animation")]
    images = [e for e in entries if e["kind"] == "image"]
    for title, group in (("영상·애니메이션", videos), ("이미지", images)):
        if not group:
            continue
        lines.append(f"## {title} ({len(group)}개)")
        lines.append("")
        lines.append("| # | 파일 | 원문 제목 | 길이/크기 | 원본 URL |")
        lines.append("|---|------|-----------|-----------|----------|")
        for i, entry in enumerate(group, 1):
            local = entry.get("local") or "(미보관)"
            size_mb = entry.get("bytes", 0) / 1024 / 1024
            meta = []
            if entry.get("duration_s"):
                meta.append(f"{entry['duration_s']:.0f}s")
            if entry.get("bytes"):
                meta.append(f"{size_mb:.1f}MB")
            label = (entry.get("title") or entry.get("context") or "").replace("|", "/")[:80]
            lines.append(
                f"| {i} | `{local}` | {label or '-'} | {' · '.join(meta) or '-'} | {entry['url']} |"
            )
        lines.append("")
    path = out_dir / "ASSETS.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# ---- 메인 ---------------------------------------------------------------
def collect(
    urls: list[str],
    out_dir: Path,
    max_bytes: int = 0,
    include_images: bool = False,
    thumbnails: bool = True,
    dry_run: bool = False,
) -> tuple[list[dict], list[dict]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pages: list[dict] = []
    entries: list[dict] = []
    seen: set[str] = set()

    for page_url in urls:
        dom, static = page_sources(page_url)
        combined = dom + "\n" + static
        video_urls = extract_media_urls(combined, page_url, MOTION_EXTS)
        video_urls += [u for u in extract_stream_pages(combined) if u not in video_urls]
        image_urls = extract_media_urls(combined, page_url, IMAGE_EXTS) if include_images else []
        titles = extract_titles(combined, page_url)
        pages.append({
            "url": page_url,
            "rendered_with_chrome": bool(dom),
            "videos_found": len(video_urls),
            "images_found": len(image_urls),
        })
        print(f"[page] {page_url} — 영상 {len(video_urls)}개, 이미지 {len(image_urls)}개"
              f"{'' if dom else ' (Chrome 렌더 실패, 정적 HTML만 사용)'}")

        for group_kind, media_urls in (("video", video_urls), ("image", image_urls)):
            for url in media_urls:
                if url in seen:
                    continue
                seen.add(url)
                kind = group_kind
                if group_kind == "video" and url.lower().split("?")[0].endswith(".gif"):
                    kind = "animation"
                entry = {
                    "kind": kind,
                    "url": url,
                    "page": page_url,
                    "context": context_for(combined, url),
                }
                title = titles.get(url) or portable_text_caption(combined, url)
                if title:
                    entry["title"] = title
                size = head_size(url)
                if size:
                    entry["bytes"] = size
                if dry_run:
                    entries.append(entry)
                    print(f"  [dry] {kind} {size / 1024 / 1024:.1f}MB {url}")
                    continue
                if max_bytes and size and size > max_bytes:
                    entry["skipped"] = f"{size} bytes > 상한 {max_bytes} bytes"
                    entries.append(entry)
                    print(f"  [skip] {size / 1024 / 1024:.1f}MB 상한 초과 — {url}")
                    continue

                sub = "videos" if group_kind == "video" else "images"
                slug = slugify(url)
                is_stream = url.lower().split("?")[0].endswith(".m3u8") or any(
                    urllib.parse.urlsplit(url).netloc.lower().endswith(h) for h in STREAM_HOSTS
                )
                try:
                    if is_stream:
                        got = download_stream(url, out_dir / sub / slug)
                        if got is None:
                            entry["skipped"] = "yt-dlp 없음 또는 다운로드 실패"
                            entries.append(entry)
                            print(f"  [skip] 스트림 다운로드 실패 — {url}")
                            continue
                        dest = got
                        if not entry.get("title"):
                            found_title = stream_title(url)
                            if found_title:
                                entry["title"] = found_title
                    else:
                        ext = Path(urllib.parse.urlsplit(url).path).suffix or (
                            ".mp4" if kind == "video" else ".bin"
                        )
                        dest = out_dir / sub / f"{slug}{ext}"
                        entry["bytes"] = download(url, dest)
                except (urllib.error.URLError, OSError, TimeoutError) as exc:
                    entry["skipped"] = f"다운로드 실패: {exc}"
                    entries.append(entry)
                    print(f"  [fail] {url} — {exc}")
                    continue

                entry["bytes"] = dest.stat().st_size
                entry["local"] = str(dest.relative_to(out_dir.parent))
                entry["sha256"] = sha256_of(dest)
                if group_kind == "video":
                    entry.update(probe(dest))
                    if thumbnails:
                        thumb = out_dir / sub / "thumbs" / f"{slug}.jpg"
                        if make_thumbnail(dest, thumb):
                            entry["thumbnail"] = str(thumb.relative_to(out_dir.parent))
                entries.append(entry)
                print(f"  [ok] {entry['bytes'] / 1024 / 1024:.1f}MB → {entry['local']}")

    return pages, entries


def refresh_manifest(urls: list[str], out_dir: Path) -> int:
    """이미 내려받은 자산의 title/context만 페이지에서 다시 읽어 갱신한다."""
    path = out_dir / "videos.json"
    if not path.exists():
        print(f"[오류] videos.json 없음: {path}")
        return 2
    data = json.loads(path.read_text(encoding="utf-8"))
    titles: dict[str, str] = {}
    contexts: dict[str, str] = {}
    for page_url in urls:
        dom, static = page_sources(page_url)
        combined = dom + "\n" + static
        titles.update(extract_titles(combined, page_url))
        for asset in data.get("assets", []):
            if asset["url"] not in titles:
                caption = portable_text_caption(combined, asset["url"])
                if caption:
                    titles[asset["url"]] = caption
            if asset["url"] not in contexts:
                ctx = context_for(combined, asset["url"])
                if ctx:
                    contexts[asset["url"]] = ctx
    updated = 0
    for asset in data.get("assets", []):
        if titles.get(asset["url"]):
            asset["title"] = titles[asset["url"]]
            updated += 1
        if contexts.get(asset["url"]):
            asset["context"] = contexts[asset["url"]]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_assets_md(out_dir, data.get("pages", []), data.get("assets", []))
    print(f"제목 갱신 {updated}/{len(data.get('assets', []))}개 — {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="웹 아티클의 영상·이미지 자산을 수집해 작업 폴더에 보관한다.",
    )
    parser.add_argument("urls", nargs="+", help="수집할 페이지 URL (여러 개 가능)")
    parser.add_argument("--out", required=True, help="자산 저장 폴더 (예: <작업폴더>/assets)")
    parser.add_argument("--max-mib", type=float, default=0,
                        help="파일당 상한(MiB). 0이면 무제한(기본).")
    parser.add_argument("--include-images", action="store_true", help="이미지도 함께 수집")
    parser.add_argument("--no-thumbnails", action="store_true", help="영상 썸네일 생성 생략")
    parser.add_argument("--dry-run", action="store_true", help="다운로드 없이 목록만 조사")
    parser.add_argument("--refresh-titles", action="store_true",
                        help="다운로드 없이 기존 videos.json의 원문 제목/맥락만 갱신")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    if args.refresh_titles:
        return refresh_manifest(args.urls, out_dir)
    pages, entries = collect(
        args.urls,
        out_dir,
        max_bytes=int(args.max_mib * 1024 * 1024),
        include_images=args.include_images,
        thumbnails=not args.no_thumbnails,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        total = sum(e.get("bytes", 0) for e in entries)
        print(f"\n[dry-run] 자산 {len(entries)}개, 합계 약 {total / 1024 / 1024:.1f}MB")
        return 0

    manifest = write_manifest(out_dir, pages, entries)
    assets_md = write_assets_md(out_dir, pages, entries)
    stored = [e for e in entries if e.get("local")]
    total = sum(e.get("bytes", 0) for e in stored)
    print(f"\n보관 {len(stored)}/{len(entries)}개, 합계 {total / 1024 / 1024:.1f}MB")
    print(f"매니페스트: {manifest}")
    print(f"자산 목록: {assets_md}")
    print("번역 HTML에는 videos.json의 local 경로와 url을 함께 링크하라.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
