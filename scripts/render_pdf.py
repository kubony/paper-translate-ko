#!/usr/bin/env python3
"""HTML을 헤드리스 Chrome으로 print-to-PDF 렌더한다.

사용법:
    python3 render_pdf.py <input.html> <output.pdf>

표준 라이브러리만 사용한다 (pymupdf 불필요). 종료코드/산출물/대략적 페이지 수를 보고한다.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

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


def find_chrome() -> str | None:
    """Return a Chrome/Chromium executable path.

    Users can override auto-detection with CHROME_BIN.  Otherwise try common
    Linux command names and the macOS app bundle path.
    """
    env = os.environ.get("CHROME_BIN")
    if env:
        return env if os.path.exists(env) or shutil.which(env) else None
    for cand in CHROME_CANDIDATES:
        if os.path.isabs(cand):
            if os.path.exists(cand):
                return cand
        else:
            found = shutil.which(cand)
            if found:
                return found
    return None


def _count_pages(pdf_bytes: bytes) -> int:
    """PDF 바이트에서 페이지 수를 대략 센다 (/Type /Page 개수)."""
    # /Type/Page 는 세되 /Type/Pages(트리 노드)는 제외
    n = len(re.findall(rb"/Type\s*/Page(?![s])", pdf_bytes))
    if n == 0:
        # 일부 생성기는 /Count 로만 표기 — 폴백
        m = re.findall(rb"/Count\s+(\d+)", pdf_bytes)
        if m:
            n = max(int(x) for x in m)
    return n


def render(html_path: str, pdf_path: str) -> int:
    html_abs = os.path.abspath(html_path)
    pdf_abs = os.path.abspath(pdf_path)
    if not os.path.exists(html_abs):
        print(f"[render] 입력 HTML 없음: {html_abs}")
        return 1
    chrome = find_chrome()
    if not chrome:
        print("[render] Chrome/Chromium 실행 파일을 찾지 못했다.")
        print("[render] CHROME_BIN=/path/to/chrome 로 지정하거나 google-chrome/chromium을 설치하라.")
        return 1

    os.makedirs(os.path.dirname(pdf_abs) or ".", exist_ok=True)
    if os.path.exists(pdf_abs):
        os.remove(pdf_abs)

    file_url = "file://" + html_abs

    # 참고: 일부 macOS Chrome 빌드는 print-to-pdf 파일을 쓴 뒤에도 프로세스가
    # 스스로 종료되지 않는다. 따라서 Popen으로 띄우고 파일이 생겨 크기가
    # 안정될 때까지 폴링한 다음 프로세스를 강제 종료한다.
    base = [
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
    ]
    # 구버전 폴백 (--headless=new / --no-pdf-header-footer 미지원 시)
    fallback = [
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-margins",
    ]

    for attempt, flags in enumerate((base, fallback), start=1):
        user_data = tempfile.mkdtemp(prefix="chrome-render-")
        cmd = [chrome, *flags, f"--user-data-dir={user_data}",
               f"--print-to-pdf={pdf_abs}", file_url]
        print(f"[render] 시도 {attempt}: {' '.join(flags[:2])} ...")
        if os.path.exists(pdf_abs):
            os.remove(pdf_abs)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 파일이 생기고 크기가 2회 연속 동일해질 때까지 최대 ~60초 폴링
        last = -1
        stable = 0
        ok = False
        for _ in range(300):  # 300 * 0.2s = 60s
            if proc.poll() is not None and not os.path.exists(pdf_abs):
                break  # 프로세스가 파일 없이 종료 -> 실패
            if os.path.exists(pdf_abs):
                sz = os.path.getsize(pdf_abs)
                if sz > 0 and sz == last:
                    stable += 1
                    if stable >= 2:
                        ok = True
                        break
                else:
                    stable = 0
                last = sz
            time.sleep(0.2)

        # 프로세스 정리 (스스로 종료 안 하는 빌드 대비)
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

        if ok and os.path.getsize(pdf_abs) > 0:
            size = os.path.getsize(pdf_abs)
            with open(pdf_abs, "rb") as f:
                pages = _count_pages(f.read())
            print(f"[render] 성공: {pdf_abs}")
            print(f"[render] 크기: {size:,} bytes, 페이지 수(추정): {pages}")
            return 0
        print(f"[render] 시도 {attempt} 실패")
        err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
        if err.strip():
            print("[render] stderr:", err.strip()[:500])

    print("[render] 모든 시도 실패 — PDF 생성 안 됨")
    return 1


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 1
    return render(argv[1], argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
