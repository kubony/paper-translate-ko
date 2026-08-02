# 논문 한글 번역 스타일 규칙 (레이아웃 보존)

DAAAM(arXiv 2512.00565) 참조 번역본을 원본과 대조하여 도출한 규칙이다.
목표: **원본 논문의 학술적 레이아웃·정보 구조를 유지하면서, 본문을 읽기 좋은
한국어로 완역**하는 것. 산출물은 HTML → 헤드리스 Chrome print-to-PDF.

## 1. 문서 구조

산출 PDF는 다음 순서를 따른다.

1. **표지 (1페이지 전체)**
   - 좌측에 굵은 세로 바(장식), 원제(영문, 대형 bold) + 하단 밑줄
   - 부제: `한국어 전문 번역`
   - `저자:` 원문 저자 — 소속 / `학회:` / `arXiv:` ID / `원문:` abs URL / `번역 생성일:` YYYY-MM-DD
   - 하단에 작은 안내문: "논문과 유사한 2단 PDF 레이아웃으로 구성했으며, 원문 피겨/표/캡션을 가능한 한 유지했습니다."
2. **서지 + 번역 메모 (본문 첫 페이지 상단, 2단)**
   - 좌측 단: 원문 제목/저자/학회/arXiv·PDF·코드 링크/번역 기준(버전) bullet 목록
   - 우측 단: **번역 메모** — 핵심 용어를 어떻게 옮겼는지 결정 사항 5~7개
     (예: "spatio-temporal memory는 문맥에 따라 '시공간 메모리/기억'으로 번역했다",
     "수식, 모델명, 벤치마크명, 데이터셋명, 표의 수치는 원문 표기를 최대한 유지했다")
3. **초록** → 번호 섹션들 → (감사의 말) → (부록) → **참고문헌 요약**

## 2. 레이아웃

- 본문은 **2단(two-column)**. 원본이 1단(예: ECCV/LNCS)이어도 참조 스타일과의
  일관성을 위해 2단을 기본으로 하되, 사용자가 원본 단 수를 요구하면 따른다.
- 섹션 번호와 계층을 그대로 보존: `1. 서론`, `2. 관련 연구`, `2.1 ...`, `부록 A. ...`
- 큰 섹션 제목(H1/H2)은 단을 가로지르는 전체 폭 + 상하 구분선, 소제목(H3/H4)은 단 내부.
- 페이지 크기 A4, 여백 약 15mm. 폰트: 한글 산세리프(Apple SD Gothic Neo / Noto Sans KR),
  코드·수식은 monospace(DejaVu Sans Mono / Menlo).
- 본문 text-align: justify. 줄간격 1.5~1.6 안팎.

## 3. 번역 문체 (혼합 표기)

- **전문용어는 영문 원형을 유지하고 한글 조사를 붙인다**: "grounding해야",
  "annotation을 붙이고", "frame 단위로". 무리한 한글화(접지, 주석화)를 하지 않는다.
- 확립된 번역어가 있으면 사용하되 첫 등장에서 원어 병기:
  "장면 그래프(scene graph, SG)", "의미적 리프팅(semantic lifting)".
- **절대 번역하지 않는 것**: 모델명, 시스템명, 벤치마크/데이터셋명, 지표명(Top-1 등),
  수치·단위·오차(0.18 ± 0.03s), 하이퍼파라미터(α = 0.5), 인명, 기관명, URL.
- 논문 자체의 시스템명 약어(예: DAAAM)는 항상 원형 유지.
- 학술 관용구는 자연스러운 한국어로: "We propose" → "본 논문은 ...를 제안한다",
  문어체 평서형("~한다", "~이다")으로 통일. 경어체 금지.
- 강조(bold/italic)는 원문 위치를 따라 유지한다.

## 3.1. AI/Robotics 용어집 우선 규칙

AI/robotics/VLA/VLN/physical AI 문서에서는 `references/vla-robotics-translation-glossary.md`를 먼저 읽고, 그 용어집을 일반 기계번역보다 우선 적용한다. 특히 다음 표기를 기본으로 한다.

- `frontier model` → **프론티어 모델**. 절대 "개척 모델"로 번역하지 않는다.
- `Physical AI` → **피지컬 AI**.
- `Vision-Language-Action`, `VLA` → 첫 등장: **Vision-Language-Action(VLA, 비전-언어-액션)**, 이후 **VLA**.
- `foundation model` → **파운데이션 모델**. 문맥상 필요한 경우 "foundation model식"처럼 혼합 표기한다.
- `robot foundation model` → **로봇 파운데이션 모델**.
- `generalist policy` → **generalist policy** 또는 **범용 로봇 policy**. "범형"은 출처가 그렇게 쓰는 경우가 아니면 피한다.
- `embodiment` → **embodiment** 또는 **로봇 몸체/몸체 형태**. "실체"로 번역하지 않는다.
- `embodied reasoning` → **embodied reasoning(체화 추론)** 또는 **embodied reasoning**.
- `direct control`, `code control`, `programmatic control`, `high-level control`, `low-level control` → 각각 **direct control**, **code control**, **programmatic control**, **high-level control**, **low-level control**을 유지하고 필요하면 괄호 안에 직역 설명을 붙인다.
- `policy`, `pretrained policy`, `gait policy`, `controller` → **policy**, **pretrained policy**, **gait policy**, **controller**를 유지한다.
- `action`, `action chunking`, `flow matching`, `diffusion policy`, `diffusion transformer` → **action**, **action chunking**, **flow matching**, **diffusion policy**, **diffusion transformer**를 유지한다.
- `open-world generalization`, `cross-embodiment`, `motion transfer`, `test-time compute`, `latent reasoning` → **open-world generalization**, **cross-embodiment**, **motion transfer**, **test-time compute**, **latent reasoning**을 유지하거나 첫 등장에 한국어 설명을 병기한다.

## 4. 수식

- 디스플레이 수식은 **monospace 코드블록**으로 ASCII/유니코드 근사 표기한다.
  LaTeX 렌더링을 시도하지 않는다(의존성 최소화, 참조 스타일과 일치).
  - 예: `K* = min_{S ⊆ F^w} |S|`, `q_ij = α · q_ij^pos + (1 - α) · q_ij^size`
  - 아래첨자는 `_`, 위첨자는 `^`, 집합·논리 기호는 유니코드(∈, ⊆, Σ, ∀) 사용.
- 인라인 수식·기호도 monospace로: `o_j^w ∈ O`, `v_ij ∈ {0,1}`.
- 수식 번호가 본문에서 참조되면 "식 (1)" 형태로 유지한다.
- PDF accessibility text나 LaTeXML 추출 결과를 그대로 붙여 넣지 않는다. 하나의 수식이
  시각 표기·접근성 낭독·LaTeX 문자열로 2~3회 중복된 경우, 모두 제거하고 사람이 읽을 수
  있는 ASCII/유니코드 수식 **한 벌만** 남긴다.
- 조건부확률, 목적함수, 복잡한 action-space 계산처럼 수식만으로 의미가 불분명하면
  수식 바로 아래에 템플릿의 `.explain-card`를 사용해 **수식 읽는 법**을 덧붙인다.
  - 각 기호가 무엇인지 정의한다.
  - 조건부 막대 `|` 오른쪽에 어떤 정보가 주어지는지 평문으로 설명한다.
  - 시계열 모델이면 과거·현재·미래 중 어떤 관찰을 사용할 수 있는지 밝힌다.
  - 예: `p_IDM(a_t | o_t, o_{t+1})` → “현재 화면과 다음 화면이 주어졌을 때,
    그 사이에 수행된 action이 `a_t`일 확률”.
- 여러 모델이 함께 학습되는 절차는 산문만 이어 쓰지 말고 짧은 흐름을 병기한다.
  예: `BC rollout → IDM 훈련 데이터 → IDM label 개선 → BC 개선`.

`work`와 `published work`는 문맥상 연구를 뜻하면 각각 **"연구"**, **"발표된 연구"**로
옮긴다. "작업", "출판된 작업"으로 기계적으로 옮기지 않는다. `to the best of our
knowledge` 같은 한정 표현은 "우리가 아는 한"처럼 보존하고, 근거 없이 "최초"라는 주장으로
강화하지 않는다.

- `previous/related work` → "기존/관련 연구"
- `no published work` → "발표된 연구는 없다" 또는 "연구가 발표된 바 없다"
- 특정 논문 한 편이라는 근거가 없으면 `work`를 임의로 "논문"으로 좁히지 않는다.

### 논문 내부 참조와 삽입구문

`Sec.`는 `Section`의 약어다. `Sec. 4.4` 전체를 하나의 참조 단위로 복원하여 **"4.4절"**로
옮긴다. `Sec.`의 마침표를 문장 종결점으로 오인해 번호나 뒤따르는 명사구를 분리하지 않는다.

쉼표로 둘러싸인 삽입구문이 있으면 이를 잠시 제거해 주절과 병렬 항목을 먼저 확인한 뒤,
원래 수식 대상에 다시 연결한다. 긴 삽입구문은 별도 문장으로 나눌 수 있지만, "이 가운데"처럼
대상을 명시하여 의미 관계를 보존한다.

- 잘못된 예: `presented in Sec. 4.4, diamond mining` → "Sec에 제시된다. 4.4, 다이아몬드 채굴"
- 권장 예: `presented in Sec. 4.4` → "4.4절에 제시된"
- `full, unmodified action space`처럼 병렬 수식어가 있으면 둘 다 `action space`를 수식하도록
  "수정하지 않은 전체 행동 공간"처럼 옮긴다.
- `which includes ...`는 관계절의 실제 선행사를 확인한다. 필요하면 "이 행동 공간에는 …도
  포함된다"처럼 문장을 나누되, 포함 관계를 바꾸지 않는다.

### 게임·강화학습 문맥

- `action space` → **행동 공간**
- 게임 UI의 `inventory` → **인벤토리**, not "재고"
- `drag-and-drop inventory management` → **드래그 앤 드롭 방식의 인벤토리 관리**
- `out-of-distribution` → **학습 분포 밖(out-of-distribution)**. 데이터의 공개·배포 여부로
  옮기지 않는다.
- `visual domain shift` → **시각적 domain shift** 또는 **시각적 도메인 차이**. "시각적
  영역의 영향력 있는 변화"처럼 단어별로 번역하지 않는다.
- `different distribution of play` → **플레이 양상이 다르다** 또는 **플레이 행동 분포가
  다르다**. 비교 대상이 생략되어 있으면 앞 문장에서 복원한다.
- `craft a crafting table` → **제작대를 만들다**. "제작대를 제작하다"처럼 동족 목적어를
  기계적으로 반복하지 않는다.
- `go past this in the technology tree` → **기술 트리의 다음 단계로 나아가다**.
- `narrower datasets` → **범위가 더 좁은 데이터셋**. 영어 어순의 "더 좁은 데이터셋"을
  그대로 쓰지 않는다.
- 데이터 분류명 `clean` / `unclean`은 **clean / unclean**처럼 대립을 보존한다. 번역어를
  쓰더라도 서로 다른 이름이어야 하며, "A를 깨끗함, 그 밖의 모든 데이터를 깨끗함"처럼
  양쪽 범주에 같은 label을 부여하지 않는다.

### 의미 슬롯 기반 3단계 번역·검토

복합문은 한 번에 한국어로 치환하지 말고 다음 세 단계를 반드시 거친다.

1. **원문 구조 복원:** 주절, 양보·대조·인과절, 삽입구문, 관계절의 선행사를 분리한다.
2. **의미 슬롯 대조:** 누가/무엇이, 어떤 조건에서, 무엇과 비교해, 무엇이 증가·감소했는지,
   저자가 관찰한 사실과 예상·가설을 표로 대조한다. `loss 증가`와 `실제 성능 하락 없음`처럼
   반대 방향의 결과는 서로 다른 문장으로 분리한다.
3. **한국어 독립 검토:** 원문을 가린 채 번역문만 읽고 대상·비교 기준·논리 관계를 설명할 수
   있는지 확인한다. 설명할 수 없으면 원문 구조를 다시 확인하고 번역한다.

특히 다음 패턴은 교정 없이 통과시키지 않는다.

- "예측할 수 있다고 예상할 수 있다"처럼 양태가 중복된 문장
- loss/metric이 무엇에 대해 증가·감소하는지 비교 기준이 빠진 문장
- `while`, `however`, `but`의 기대와 관찰 결과를 한 한국어 문장에 억지로 묶은 문장
- 영어 관계절의 선행사가 한국어에서 다른 명사로 이동한 문장
- 문장이 "~함에 따라" 같은 연결어로 끝나 후속 명제가 누락된 경우
- 원문에서 model objective 설명과 optimizer·learning rate·batch size·step 수가 별도 문단이면 번역에서도 문단을 보존한다. 개념적 결론 뒤에 AdamW 같은 hyperparameter를 한 문단으로 이어 붙이지 말고, 필요하면 **`학습 설정.`** label을 둔 별도 문단으로 분리한다.

## 5. 피겨(그림)

- 원본 PDF에서 그림 영역을 **이미지로 추출**(scripts/extract_figures.py)하여 재삽입한다.
  그림을 다시 그리거나 생략하지 않는다.
- 그림 아래에 짧은 캡션: `그림 N. <한 줄 요약>.` (예: `그림 2. 시스템 개요.`)
- 캡션이 길면(2문장 이상) 별도 전체 폭 섹션 `그림 N. <제목> 캡션 번역`을 만들어
  캡션 전문을 2단으로 완역한다. 티저 그림(Figure 1)은 항상 이 방식을 쓴다.
- 그림 번호는 원본을 따른다(`그림 A.1` 등). 본문 참조("Fig. 2")는 "그림 2"로.
- 원본이 표와 그림을 한 캡션으로 묶어도("Table 1 and Figure 2: ...") 산출물에서는
  **표 캡션과 그림 캡션을 분리**해 각자 단다. 혼합 캡션은 번호 혼동을 만든다.
- 세로로 매우 긴 다패널 그림(A.1 같은 4패널 세로 배치)은 페이지 경계에서 잘리기 쉽다.
  템플릿의 `max-height` 제한을 활용하거나, 패널을 (a)(b)/(c)(d)로 나눠 각각 crop해
  두 개의 그림으로 삽입한다. 그림이 잘린 채 다음 페이지로 넘어가면 안 된다.

## 6. 표

- 표는 이미지가 아니라 **HTML 표로 재구성**한다. 수치는 원본 그대로(반올림 금지),
  최고 성능 bold 강조와 **2위 성능 underline 강조**(템플릿 `.ul` 클래스)도 그대로 재현한다.
- **6열 이상이거나 셀 텍스트가 긴 표는 반드시 `class="wide"`**로 단 전체 폭에 배치한다.
  좁은 단에 넣으면 셀 겹침·세로 토큰 덤프로 붕괴한다.
- 표 제목은 섹션형 헤더로: `표 N. <내용 요약>` (원본 캡션 요약 번역).
- **`table.wide`의 제목도 반드시 같은 전체 폭 formatting context에 둔다.** 예를 들어 `h3.section`을 쓰면 CSS에 `.doc-title, h2.section, h3.section { column-span: all; }`처럼 H3까지 명시한다. `class="section"`만 붙이고 selector를 `h2.section`으로 한정하면 Chrome의 multicol print에서 제목 마지막 단어가 반대쪽 column으로 찢어질 수 있다.
- 전체 contact sheet뿐 아니라 wide table이 있는 page를 120–150 dpi로 별도 확대해 제목이 한 덩어리로 유지되는지 확인한다.
- 헤더 행은 회색 배경, 셀 좌우 정렬은 원본을 따른다. 열 이름(Method, Top-1 등)은 원형 유지.

## 7. 인용과 참고문헌

- 본문 인라인 인용 번호 `[12, 34]`는 **제거**하고 문장을 자연스럽게 다듬는다.
  구체적 시스템을 지칭하면 이름으로 풀어쓴다("Khronos의 접근을 따른다").
- 문서 끝에 `참고문헌 요약` 섹션: "아래는 원문 참고문헌 N개의 핵심 목록이다.
  원문과의 대조를 위해 citation key와 제목은 주로 원문을 유지했다." 안내 후,
  `저자 et al. (연도), 제목.` 형태의 번호 목록(2단, 원문 제목 유지).

## 8. 완전성 기준

- 초록부터 결론·부록까지 **모든 본문 문단을 완역**한다. 요약·생략 금지
  (참고문헌만 요약 허용).
- 모든 그림·표가 산출물에 존재해야 한다.
- 페이지 수는 원본과 비슷한 수준(±30%)이 정상 범위다.
- **원문 페이지를 통째로 캡처한 이미지를 삽입하지 않는다.** `figures/pages/page-NN.png`는
  그림 좌표 계산용 보조자료일 뿐이다 — 산출물에는 개별 추출한 `fig-*.png`만 넣는다.
- **"원문 p.N 번역" 식 페이지 단위 텍스트 덤프로 구성하지 않는다.** 산출물은 원문
  페이지가 아니라 섹션 구조를 따르는 2단 본문이어야 한다.
