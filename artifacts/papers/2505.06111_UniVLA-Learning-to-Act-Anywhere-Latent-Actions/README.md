# UniVLA (arXiv:2505.06111) 한국어 전문 번역

**원제**: *UniVLA: Learning to Act Anywhere with Task-centric Latent Actions*  
**저자**: Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, Hongyang Li  
**소속**: The University of Hong Kong · OpenDriveLab · AgiBot  
**출처**: arXiv:2505.06111, 18페이지 · **번역 생성일**: 2026-07-27  
**코드**: https://github.com/OpenDriveLab/UniVLA

## 산출물

| 파일 | 설명 |
|---|---|
| `translation.html` | 초록부터 본문, 결론, 한계, 감사의 말, 부록, 참고문헌까지 옮긴 2단 한국어 HTML |
| `manifest.json` | 원문/산출물 구조 카운트, 자산 매핑, 완결성 점검 |
| `README.md` | 본 문서 |
| `figures/assets/*.png` | `source/figures/*.pdf`를 브라우저용 개별 PNG로 변환한 12개 그림 |

## 번역·재구성 기준

- `source/paper_submission_main.tex` **절대경로**: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2505.06111_UniVLA-Learning-to-Act-Anywhere-Latent-Actions/source/paper_submission_main.tex`
- `original.pdf` **절대경로**: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2505.06111_UniVLA-Learning-to-Act-Anywhere-Latent-Actions/original.pdf`
- TeX 1,444행과 PDF 18쪽을 대조했다. 문체는 문어체 평서형(`~한다`)이다.
- VLA, policy, action, latent action, task-centric, embodiment, cross-embodiment 등 핵심 기술 용어는 영문 혼합 표기를 유지한다.
- 원문 그림은 페이지 통캡처가 아니라 `source/figures/`의 개별 PDF 자산을 150dpi PNG로 변환하여 상대경로로 삽입했다.
- 표는 전부 HTML `<table>`로 재구성하여 수치와 굵게/밑줄 강조를 보존했다.
- 디스플레이 수식은 `<pre class="equation">`의 ASCII/Unicode 표현 한 벌로 넣었다.
- 본문 citation 번호는 제거했으나, 참고문헌 99개는 저자·연도·원문 제목 목록으로 보존했다.

## 구조 및 검증 카운트

| 항목 | 원문/산출물 수 |
|---|---:|
| PDF 페이지 | 18 |
| 본문 번호 섹션 | 6 |
| 부록 상위 구획 | 3 |
| 그림 | 12 |
| 표 | 11 |
| 디스플레이 수식 | 4 |
| 참고문헌 | 99 |

원문 LaTeX에서 그림 caption과 table caption을 합친 총 caption 수는 23개이며, 산출물에는 그림 12개와 HTML 표 11개로 모두 대응한다. 이미지 상대경로 12개는 모두 실제 파일 존재를 확인했다.

## 여는 법

```bash
cd /home/inkeun/tools/paper-translate-ko/artifacts/papers/2505.06111_UniVLA-Learning-to-Act-Anywhere-Latent-Actions
xdg-open translation.html
```

브라우저 인쇄에서 A4 2단 레이아웃으로 PDF 저장할 수 있다. `translation.html`과 `figures/assets/`의 상대적 위치를 함께 유지해야 그림이 표시된다.
