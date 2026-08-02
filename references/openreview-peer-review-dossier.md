# OpenReview 공개 심사 기록을 학술 PDF dossier로 만드는 절차

## Trigger와 범위 구분

사용자가 논문 자체가 아니라 “리뷰를 모아 보고 싶다”, “심사 기록을 논문 완역본처럼 PDF로 달라”고 하면 기존 논문 번역본을 재전달하지 않는다. 이 작업은 **peer-review dossier**다.

최소 inventory:

1. submission/current venue
2. official reviews
3. author comments/rebuttals
4. meta-review
5. decision note가 있으면 decision; 없으면 별도 note가 없다고 밝히고 submission venue와 독립 source로만 outcome을 교차 검증

## 1. 공개 thread 복구

1. forum ID와 submission title/number를 확정한다.
2. 일반 forum/API가 challenge-gated면 CAPTCHA·인증 우회를 하지 않는다.
3. 공개 `https://api2.openreview.net/notes/search`가 응답하면 다음 query를 넓혀가며 수집한다.
   - 정확한 논문 제목과 고유 phrase
   - reviewer alias/signature
   - 이미 확보한 reply의 고유 title/phrase
4. 결과는 검색어 일치만으로 채택하지 않고 `note.id == forum_id` 또는 `note.forum == forum_id`를 강제한다.
5. `replyto`, signature, invitation/type, note ID를 이용해 submission→review→response→meta-review closure를 구성한다.
6. Wayback, conference stats/review datasets, 공개 mirror는 note 원문의 대체재가 아니라 score/outcome의 독립 corroboration으로 사용한다.
7. current public note들의 exact structured JSON과 사람이 읽는 verbatim inventory를 모두 보존한다. 복구하지 못한 note나 decision을 추정 생성하지 않는다.

완전성 문구는 증거 수준에 맞춘다. 직접 `forum=` 열거가 막혔고 search closure로 복구했다면 “수학적으로 완전”이라고 쓰지 말고, reviewer 전원·reply chain·meta-review·독립 source 일치에 근거해 “공개 thread를 사실상 완전 복구”했다고 한계를 함께 적는다.

## 2. 요청 해석과 문서 정보 구조

### `완역` 계약

사용자가 “리뷰를 한글 논문 완역본처럼”, “리뷰 원문을 모두 한글로”, “전문 번역”이라고
하면 기본값은 **한국어 분석을 덧붙이는 것**이 아니라 아래 전체 source text의 완역이다.

- official review의 모든 문자열 field(summary, strengths, weaknesses, questions 등)
- author comment/rebuttal의 title과 comment 전문
- meta-review의 summary, reviewer concerns, reviewer scores 등 모든 문자열 field
- decision note가 있으면 decision 전문

Submission note는 review가 아니므로 사용자가 thread 전체 번역을 요구하지 않는 한 서지
metadata에만 사용한다. exact English source는 JSON/verbatim inventory로 별도 보존하되, 사용자가
bilingual 판본을 요청하지 않았다면 delivered PDF에 영문 원문 부록을 넣어 분량을 대신하지
않는다. **한국어 요약 + 영문 원문 Appendix는 완역이 아니다.**

한국어 A4 2단 완역 dossier의 권장 순서:

1. 별도 표지: 제목, forum/submission, outcome, 완역 note 구성, 작성자, 생성일
2. 완역 범위·번역 원칙·review rating/confidence 표
3. note inventory 표
4. official review 한국어 전문
5. author comments/rebuttals 한국어 전문
6. meta-review/decision 한국어 전문
7. 수집 경로, cross-check, 접근·완전성 한계

분석·비평을 추가할 경우 `번역문 아님`으로 시각적으로 분리한다. 완역 본문에는 source가 직접
말한 내용만 둔다. 각 note에 ID, type, created time, reply target, signature, version, license,
stable OpenReview link를 둔다.

### Field-level 완전성·충실도 gate

1. source-of-truth JSON에서 번역 대상 note ID와 모든 string field key의 inventory를 만든다.
2. 번역 JSON은 `note id → translations → original field key` 구조로 저장한다.
3. source와 번역의 note ID set 및 field key set이 exact equality인지 assert한다.
4. field마다 Markdown table row, fenced-code marker, URL, 숫자·metric을 대조한다. 한국어 어순을
   위해 paragraph 사이 blank line을 추가할 수는 있지만 원문 명제나 rhetorical boundary를
   합치거나 생략하지 않는다.
5. 독립 fidelity pass로 누락, 의미 반전, 주체/비교기준 변경, 주장 과강화·약화, VLA/VLN 용어
   위반을 교정한다. 번역 agent와 감사 agent를 가능하면 분리한다.
6. code block 밖에서 `ASCII 문자가 길고 한글이 거의 없는 line`을 찾아 미번역 English prose를
   검사한다. 논문명·참고문헌 원제·모델명·code는 허용하되, 허용 line을 명시적으로 기록한다.
7. 최종 PDF의 note ID, translated section title, 마지막 meta-review/decision marker를 extracted
   text에서 확인한다.

## 3. OpenReview Markdown 정규화

OpenReview response는 Markdown이 list 안에 들여쓰기되어 있어 Python-Markdown에서 표·fenced code·heading이 raw text로 인쇄될 수 있다.

렌더링 사본에만 다음 정규화를 적용하고 exact JSON은 절대 수정하지 않는다.

- 들여쓰기된 pipe-table run을 root로 lift하고 앞뒤 blank line을 추가한다.
- list 안의 fenced code block은 fence와 내용의 공통 들여쓰기를 제거한다.
- `1. ### Heading`은 `### 1. Heading`, `- ### Heading`은 `#### Heading`처럼 semantic heading으로 바꾼다.
- 정규화 후 HTML에서 `<table>`·`<pre>`·heading 개수가 예상대로 증가했는지 assert한다.
- PDF에 raw `| --- |`, `###`, literal backticks가 남지 않았는지 확대 QA한다.

이 변환은 display-only다. 원문 verbatim 보존 주장은 exact JSON/Markdown inventory에 대해 한다.

## 3.1. 선택된 OpenReview note의 문자열 field만 JSON으로 완역

사용자가 note ID 목록과 `comment`, `title` 같은 field를 지정해 JSON 산출물을 요구하면 dossier PDF 전체를 만들지 말고 **field-level translation artifact**로 처리한다.

1. source JSON을 parser로 읽어 지정 ID를 exact match하고, 사용자가 준 순서를 유지한다. 큰 `value`가 한 줄에 있어 파일 읽기 도구가 `[truncated]`로 표시해도 그 조각을 완전한 원문으로 오인하지 않는다. 가능하면 JSON parser로 값을 추출하고, 이미 생성된 dossier HTML의 `exact original` appendix는 문단 구조를 읽는 보조 view로만 사용한다. source-of-truth는 JSON이다.
2. 결과 schema는 요청한 최소 형태를 그대로 지킨다. 기본 예시는 다음과 같다.

```json
{
  "notes": [
    {
      "id": "<note-id>",
      "translations": {
        "comment": "<한국어 완역>",
        "title": "<한국어 완역>"
      }
    }
  ]
}
```

원본 metadata, `forumContent`, 저자명, URL 등을 사용자가 요구하지 않았으면 복사하지 않는다. ID는 번역하지 않는다.
3. Markdown의 heading/list/table/fenced code/강조/문단 경계를 보존한다. prompt나 code fence 안의 자연어 문장은 번역하되 placeholder, 숫자, 좌표, action sequence, model·benchmark·metric명, 변수와 code token은 유지한다. 논문 제목이 참고문헌에 들어 있으면 일반 번역 규칙에 따라 원문 제목을 유지한다.
4. 긴 문자열 안의 ASCII 큰따옴표는 JSON escape(`\"`)를 정확히 쓰거나 의미가 같다면 curly quote(`“…”`)로 바꾼다. 파일 작성 직후 JSON lint를 통과해야 하며, 실패하면 먼저 보고된 line/column 부근의 embedded quote와 backslash를 검사한다.
5. 완료 assertion: 요청한 note 수, ID의 exact order, note별 요청 field 수, 빈 번역 0, 예상 밖 key 0을 확인한다. 최종 보고는 절대경로와 `N개 note / M개 field`만 간결하게 제시해 downstream 조립을 방해하지 않는다.

## 4. 2단 Chromium 조판

- `.paper-body { column-count:2; column-gap:...; column-rule:none }`
- wide table, major section heading, note metadata strip, source caveat는 `column-span:all`로 둔다.
- 모든 wide table의 heading도 동일한 spanning context에 둔다.
- `break-inside:avoid`를 긴 note 전체에 주지 않는다. note는 여러 page/column에 흐를 수 있어야 한다.
- code는 `white-space:pre-wrap`, `overflow-wrap:anywhere`, 작은 monospace font로 둔다.
- **spanning 요소가 하나라도 있으면 `column-rule`을 그리지 않는다.** Chromium print는
  `column-span:all` 앞뒤에서 세로 rule을 분절하고, 그 조각이 heading·note metadata box를
  관통하거나 page 중간에 고립된 수직선으로 나타날 수 있다. 열 구분은 충분한 `column-gap`만
  사용한다.
- **표지 장식선을 `position:absolute; top:77mm`처럼 물리 좌표에 고정하지 않는다.** 제목이
  줄바꿈되거나 font가 대체되면 선이 글자를 관통한다. 제목 요소 자체의
  `padding-bottom + border-bottom`처럼 document flow에 anchor한다.
- major section `h2`와 첫 note title이 연속할 때 양쪽 모두 border를 그리지 않는다. 예:
  `h2 + .note > h3.note-title { border-top:0; padding-top:0; }`. 같은 위치의 구분선은 한 요소만
  소유하게 해 이중·삼중 horizontal rule을 막는다.
- **fixed header/footer를 multicol body에 쓰지 않는다.** Chrome print에서 footer가 page 상단/본문 중간에 반복되어 제목과 겹칠 수 있다. canonical renderer의 print header/footer 비활성화를 사용하고, 꼭 필요한 running header는 검증된 page-margin 방식이 있을 때만 넣는다.

`check_multicol_layout.py`로 wide selector뿐 아니라 active `column-rule`과 fixed-offset cover
separator 회귀도 검사하고 canonical `render_pdf.py`로 출력한다.

## 5. 필수 QA gate

기계 QA:

- PDF 모든 page가 A4인가
- blank page와 out-of-bounds text block이 0인가
- inventory의 모든 unique note ID가 PDF extracted text에 존재하는가
- venue/outcome, meta-review signature, 마지막 response title 등 핵심 marker가 존재하는가
- `file:///`, browser challenge 문구, `[truncated]`, raw Markdown table/heading이 없는가
- 링크 annotation 수가 0이 아닌가
- page별 text character count로 비정상적으로 빈 page를 찾는다

시각 QA:

1. 전체 page를 140–180 dpi로 rasterize해 6–8장씩 contact sheet로 본다. 100 dpi 안팎의 축소본은
   0.35–1 pt의 잘못된 separator를 놓칠 수 있으므로 thin-line QA에는 사용하지 않는다.
2. 모든 wide table page, code/pseudocode page, 첫 page, 마지막 page를 개별 확대한다.
3. 모든 `column-span:all` heading·metadata strip의 위/아래를 확대해 center gutter에 고립된
   수직선 조각이 없는지 확인한다. separator는 텍스트·박스·제목을 관통하지 않아야 한다.
4. 표지는 제목 줄 수가 달라도 장식선이 제목의 마지막 baseline 아래에 있는지 확인한다.
5. 표 header/수치 가독성, column 경계, heading split, clipping/overlap, 마지막 문장 완결을 확인한다.
6. 가능하면 Android/iOS 기본 PDF viewer 또는 그와 유사한 실제 viewer 배율에서도 표지와
   spanning-heavy page를 확인한다. browser screenshot과 rasterized PDF 둘 중 하나만 통과한 것은
   완료가 아니다.
7. Chrome/Skia PDF의 한글이 다수의 embedded Type 3 subset font로 기록되면 PyMuPDF·Poppler에서는
   정상이어도 Discord/일부 모바일 preview가 뒤쪽 page를 백지로 표시할 수 있다. 실제 PDF의
   page별 text/drawing count와 독립 renderer 결과가 정상인데 viewer에서만 blank라면 콘텐츠를
   삭제하지 않는다. Ghostscript `pdfwrite -dNoOutputFonts -dPreserveAnnots=true`로 글자를 vector
   outline으로 바꾼 별도 `*_VIEWER_COMPAT.pdf`를 만들고, 원본은 검색·선택 가능한 canonical
   artifact로 보존한다. 호환본은 page 수, annotation 수, 전 page raster, 특히 신고된 마지막 page를
   다시 검사한다. 글자를 outline으로만 변환하면 텍스트 선택이 사라지므로, canonical PDF의
   `rawdict` line text와 좌표를 가져와 실제 사용 glyph만 subset한 CJK CID font로 invisible
   text layer(`render_mode=3`)를 겹친 **selectable compatibility copy**를 우선 전달한다. 완료
   조건은 page별 정규화 text length ratio 99% 이상, 마지막 page의 고유 한국어/영문 phrase
   search hit, annotation 보존, outline-only 호환본과 전 page raster pixel equality다. full CJK
   font를 그대로 embed해 첨부 한도를 낭비하지 말고 문서 glyph subset을 사용한다.
8. raw Markdown 표, fixed footer 겹침, separator 관통/분절이 하나라도 발견되면
   수정→재렌더→**전 페이지** 기계/시각 QA를 처음부터 반복한다.

최종 보고에는 page 수, byte size, SHA-256, note count/type breakdown, blank/oob 결과와 QA PASS를 적고 PDF 자체를 첨부한다. 의미 있는 복구·검증 작업은 작성자 이름과 함께 Outline `Sessions`에도 기록한다.
