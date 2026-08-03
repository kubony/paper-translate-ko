# 본문 인용·참고문헌 조판 규칙

## 목적

번역 fragment 또는 LaTeX source의 raw BibTeX key(`team2024chameleon`, `chen2025blip3`)를 독자에게 노출하지 않는다. 2단 학술 PDF에서는 원문 bibliography style과 번호를 보존한 압축 숫자형 인용을 사용한다.

## 표준 출력

- 본문: `[12]`, `[12, 57]`, `[12–14, 21]`
- 연속 번호 3개 이상만 en dash(`–`)로 압축한다. 두 개는 `[12, 13]`으로 쓴다.
- citation 전체에 `white-space: nowrap`을 적용해 줄 중간에서 괄호가 찢어지지 않게 한다.
- 숫자는 참고문헌 `<li id="ref-N">`에 연결한다. PDF 내부 링크가 유지되는지 확인한다.
- raw BibTeX key, 세미콜론 key 묶음, `\\cite{...}`는 최종 HTML/PDF에 남기지 않는다.

## 원문 번호 확정

1. source에 `.bbl`이 있으면 `\\bibitem{key}` 순서를 canonical order로 사용한다.
2. `.bbl`이 없으면 `main.tex`의 `\\bibliographystyle{...}`을 확인한다.
3. TeX 전체 컴파일이 font/package 누락으로 실패해도 포기하지 않는다. active section에서 citation key를 수집한 최소 `.aux`를 만든 뒤 `bibtex`만 실행하여 `.bbl`을 생성한다.
4. `.bbl`의 `\\bibitem` 순서를 `citation_map.json`으로 저장한다. 번호를 BibTeX 파일의 물리적 entry 순서로 추측하지 않는다.
5. 번역 fragment의 대괄호 문자열은 내부 token이 **모두 citation_map의 key일 때만** 인용으로 치환한다. `[dev]`, `[High]`, `[0,1]` 같은 일반 텍스트·수식 범위를 오인하지 않는다.

## 참고문헌 목록

- 실제 본문에서 인용한 entry만 싣는다. source `refs.bib`에 존재하지만 active paper에서 인용하지 않은 entry를 개수 채우기용으로 붙이지 않는다.
- 원문 번호 순서로 `<ol>`을 만든다.
- 각 항목은 `첫 저자 et al. (연도). 원문 제목.`을 기본으로 한다. 모델명·논문 제목은 원문 표기를 유지한다.
- 항목마다 `break-inside: avoid`를 적용하고 2단에서 7–7.5pt 정도의 보조 본문 크기를 쓴다.

## 필수 assertion

- citation map 번호는 1부터 연속이고 중복이 없다.
- 모든 본문 citation key가 map에 존재한다.
- 모든 map key가 BibTeX metadata를 가진다.
- 최종 DOM의 `.references li` 개수와 citation map 크기가 같다.
- 모든 `.citation a[href^="#ref-"]` 대상이 실제로 존재한다.
- 알려진 raw BibTeX key가 최종 visible text에 남지 않는다. 모델명과 key가 우연히 같은 경우는 citation bracket 문맥으로 판별한다.
- 교정 후 validator를 다시 실행하고, 인용이 밀집된 본문 페이지와 참고문헌 시작·중간·마지막 페이지를 확대 시각 QA한다.

## 금지 패턴

- `[team2024chameleon; chen2025blip3]`처럼 key를 그대로 인쇄
- citation을 일괄 삭제해 문장의 근거 연결을 제거
- `refs.bib` 파일 순서를 원문 번호라고 가정
- 숫자형 인용을 validator 경고로 간주하여 다시 제거
- 참고문헌 목록에 title만 나열하고 저자·연도를 생략
