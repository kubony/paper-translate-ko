# CogACT arXiv 2411.19650 한국어 전문 번역

## 산출물

- 한국어 전문 HTML: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/translation.html`
- 구조·완전성 manifest: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/manifest.json`
- 원문 PDF: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/original.pdf`
- 주 LaTeX: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/source/main.tex`
- 섹션 LaTeX: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/source/sec/`
- 참고문헌 원본: `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2411.19650_CogACT-Synergizing-Cognition-and-Action/source/main.bbl`

## 번역 범위

`source/main.tex`와 `source/sec/*.tex` 7개, 총 8개 TeX 파일 911줄을 확인하고 `original.pdf` 20쪽의 구조와 대조했다. 다음을 포함한다.

- 초록 전체
- 본문 1–5장 전체(서론, 관련 연구, 방법, 실험, 결론)
- Supplementary Material A–C 전체
- figure 13개와 모든 caption
- table 13개를 HTML table로 재구성하고 모든 수치 및 원문의 굵게/밑줄 강조 보존
- display equation 6개(본문 5개와 supplement의 `C = K × std` 관계식)
- 참고문헌 79개 원문 제목 보존 목록

## 형식 및 용어

- `/home/inkeun/tools/paper-translate-ko/assets/template.html`을 기준으로 A4 인쇄용 2단 layout을 직접 구성했다.
- 문어체 평서형 `~한다`를 사용했다.
- VLA, policy, action, cognition token, cognition feature, Diffusion Action Transformer(DiT), embodiment, action chunk 등 핵심 전문용어는 영문 혼합 표기를 유지했다.
- 특히 linguistic token과 visual token에 **추가 learnable cognition token 하나**를 붙여 causal attention으로 처리하고, 그 cognition token에 대응하는 **output hidden feature(cognition feature)가 뒤 action module의 condition**이 된다는 원문 의미를 명시적으로 보존했다.
- 수식은 `<pre class="equation">`의 ASCII/Unicode 근사 표기이다.
- 그림은 원문 페이지 통캡처가 아니라 `source/figures/`의 개별 figure asset을 상대경로로 참조한다.

## 검증 결과

HTML parser와 파일 검사를 통해 다음을 확인했다.

| 항목 | 확인값 |
|---|---:|
| original.pdf 페이지 | 20 |
| 확인한 TeX 파일 | 8 |
| 확인한 TeX 줄 | 911 |
| HTML figure / img | 13 / 13 |
| HTML table | 13 |
| HTML display equation | 6 |
| 참고문헌 | 79 |
| HTML UTF-8 크기 | 55,461 bytes |

브라우저에서 `translation.html`을 열면 상대경로 자산과 함께 볼 수 있다. PDF figure asset은 브라우저의 PDF 이미지 표시 지원에 따라 inline 렌더링되며, 원본 개별 asset 경로 자체는 그대로 보존된다.
