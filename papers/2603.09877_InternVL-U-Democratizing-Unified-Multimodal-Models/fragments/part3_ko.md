# InternVL-U — 실험·결론·부록 한국어 번역 조각

> 번역 범위: `main.tex`의 활성 순서에 따른 `sections/5.experiment.tex`, `sections/6.conclusion.tex`, `sections/appendix.tex` 및 이 파일들이 직접 `\input`하는 표 파일. 벤치마크·모델·지표명과 수치는 원문 표기를 유지한다.

<!-- source:sections/5.experiment.tex:1 -->
## 실험

<!-- source:sections/5.experiment.tex:4 -->
### 실험 설정

<!-- source:sections/5.experiment.tex:6 -->
InternVL-U는 InternVL3.5-2B에 구현되어 있으며, 비주얼 이해 앵코더와 멀티모달 컨텍스트 백스본을 초기화하기 위해 무게를 사용한다. 텍스트 토케니저와 대화 형식은 동일한다. 이미지 생성을 위해, 우리는 Qwen-Image와 동일한 VAE를 사용한다.

<!-- source:sections/5.experiment.tex:7 -->
시각 생성 헤드 는 1.7B 매개 변수를 포함하여 무작위로 초기화 된다. InternVL-U의 매개 변수의 총 수는 4B 이다. 상세한 구성은 테이블 §tab:model_config에서 표시된다.

<!-- source:sections/5.experiment.tex:8 -->
이전 작업에 따라 우리는 이미지 및 텍스트 조건 모두에 대한 분류자 없는 가이드 (CFG) 를 채택했습니다. 훈련 중에 텍스트에서 이미지 생성 데이터에 대한 조건은 10%의 확률로 떨어집니다. 이미지 편집 데이터에 대한 경우, 멀티모달 조건 ( 텍스트와 이미지를 포함한) 은 5%의 확률로 떨어집니다. 그리고 이미지 입력을 유지하면서 텍스트만 떨어뜨리는 5%의 확률도 있다.

<!-- source:sections/5.experiment.tex:9 -->
추론 과정에서 Flow-DPM-Solver는 20개의 추론 단계로 채택된다. 전체 조건과 텍스트 조건만을 떨어뜨리는 CFG 스칼은 각각 3.5 및 1.5로 설정된다.

<!-- source:sections/5.experiment.tex:10 -->
§sys_prompt는 다양한 설정에서 사용되는 시스템 및 사용자 명령어를 설명하고 있으며, 이 설정의 임베디션은 시각 생성 헤드에 입력되면 단축된다.

<!-- source:sections/5.experiment.tex:11 -->
각 단계의 상세한 교육 설정은 §tab:train_config에서 표시된다. 우리는 VLMEvalkit을 사용하여 다형적 이해와 추론 기준을 평가한다. 이미지 생성 및 편집 작업에 대한 평가에 대해서는 또한 오픈 소스인 GenEditEvalKit$^†$라는 자체 개발 된 평가 도구 킷을 사용한다.

<!-- source:sections/5.experiment.tex:21 -->
< < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <

<!-- source:sections/5.experiment.tex:22 -->
당신은 서생·만상(书生·万象)이며 영어 이름은 InternVL이다. 상하이 인공지능연구소, 칭화대학교 및 여러 협력 기관이 공동 개발한 멀티모달 대규모 언어 모델이다. 이미지 속 객체와 배경의 색상, 모양, 크기, 질감, 수량, 문자 내용 및 공간적 위치 관계 등을 상세히 기술하여 이미지를 포괄적으로 설명한다: <|im_end|>

<!-- source:sections/5.experiment.tex:25 -->
< < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < < <

<!-- source:sections/5.experiment.tex:26 -->
당신은 서생·만상(书生·万象)이며 영어 이름은 InternVL이다. 상하이 인공지능연구소, 칭화대학교 및 여러 협력 기관이 공동 개발한 멀티모달 대규모 언어 모델이다. 입력 이미지의 핵심 특징(색상, 모양, 크기, 질감, 객체, 배경 등)을 설명한 다음, 사용자의 텍스트 지시가 이미지를 어떻게 변경하거나 수정해야 하는지 설명하여 사용자 요구를 충족하는 새 이미지를 생성하고 원본 입력과의 일관성을 적절히 유지한다: <|im_end|>

<!-- source:sections/5.experiment.tex:29 -->
< 줌im_start 줌>user \\

<!-- source:sections/5.experiment.tex:30 -->
여기 무작위 이미지입니다: <img_uncond>

<!-- source:sections/5.experiment.tex:33 -->
< 줌im_start 줌>user \\

<!-- source:sections/5.experiment.tex:34 -->
참조 이미지를 기반으로 이미지를 생성한다.<

<!-- source:sections/5.experiment.tex:37-38 -->
**그림 설명.** ** 시스템 명령어 및 사용자 명령어, 다양한 작업에 대한 훈련 중 채택된**, <img_uncond>는 이미지 생성에 대한 학습 가능한 특수 토큰이다.

<!-- source:sections/5.experiment.tex:42 -->
### 멀티모달 이해 및 추론

<!-- source:sections/5.experiment.tex:44 -->
다중모달적 이해와 추론 능력을 평가하기 위해 우리는 MME-P, SEED, ChartQA, OCRBench, MMMU, MathVerse, LogicVista 등 7개의 널리 인정되는 MLLM 벤치마크를 통해 InternVL-U를 평가한다.

<!-- source:sections/5.experiment.tex:45 -->
§tab:exp_und_reason에서 보여지는 바와 같이, InternVL-U는 다모달 이해와 추론 기준에 대한 강력한 성능을 입증하고 있으며, MME-P (1607.5) 및 OCRBench (83.9) 같은 핵심 매트릭스에서 Janus-Pro 및 Ovis-U1와 같은 비교형 UMM를 크게 뛰어넘습니다. 주목할 만한 점은, 컴팩트 구조 (2B+1.7B) 와는 비교할 수 있는 추론 능력을 제공하며, 특히 MMMU (54.7와 55.3) 에서 이해와 발전 사이의 우수한 균형을 달성하는 동시에 이해의 기본 라인들의 강력한 시각적 언어 이해도를 효과적으로 유지한다는 것을 나타낸 결과이다.

<!-- source:sections/5.experiment.tex:50 -->
### 텍스트-이미지 생성

<!-- source:sections/5.experiment.tex:52 -->
텍스트에서 이미지로 생성할 수 있는 능력을 종합적으로 평가하기 위해 우리는 일반 평가에 대해 GenEval, DPG-Bench, TIIF, OneIG, 텍스트 렌더링 품질에 대해 LongText, CVTG-2k, 지식 집중적인 생성에 대해 WISE, GenExam를 채택한다.

<!-- source:sections/5.experiment.tex:54 -->
#### 일반 이미지 생성

<!-- source:sections/5.experiment.tex:56 -->
**GenEval**. GenEval은 객체 공상 속성, 위치, 수, 색 등의 구성 성질을 평가하는 객체 중심의 프레임워크이다. §tab:exp_geneval에서, InternVL-U는 기존의 BAGEL와 같은 통일 모델 중 절반 또는 심지어는 적은 매개 변수 수를 가진 최고 전체 점수를 (0.85) 달성한다. 또한 대부분의 전문 생성 모델을 뛰어넘습니다.

<!-- source:sections/5.experiment.tex:59 -->
DPG 벤치

<!-- source:sections/5.experiment.tex:60 -->
§tab:exp_dpgbench에서는 텍스트-진상 모델의 복잡한 의미적 조율 기능을 평가하기 위해 여러 객체를 설명하는 밀집한 명령어를 제공하는 DPG-Bench의 결과를 보여준다. §tab:exp_dpgbench에서는 우리의 모델은 다른 통일된 모델보다 특히 *Global* 및 *Entity* 차원에서 더 강력한 성능을 보여준다.

<!-- source:sections/5.experiment.tex:66 -->
**TIIF**.TIIF는 복잡한 지침을 따르는 능력을 체계적으로 평가하는 것을 목표로 한다. §tab:exp_tiif_short,tab:exp_tiif_long에서 보여지는 바와 같이, 우리의 InternVL-U는 통일된 모델들 사이에서 특히 고급 지침을 따르는 데 강력한 성능을 달성한다. 통일된 모델과 생성 모델 사이에 여전히 눈에 띄는 차이점이 있다.

<!-- source:sections/5.experiment.tex:71 -->
**OneIG-Bench**. §tab:exp_oneigbench,tab:exp_oneigbench_zh 에서, 우리는 OneIG-Bench에서 우리의 InternVL-U를 평가한다. 이는 주체 요소 조율, 텍스트 렌더링 정확성, 추론으로 생성된 콘텐츠, 스타일링 및 다양성을 통해 세밀한 평가로 설계되었습니다.

<!-- source:sections/5.experiment.tex:77 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:78 -->
양적 측정치 이외의 실질적인 강점을 더 잘 설명하기 위해 우리는 추가적인 질적 비교를 제공한다.

<!-- source:sections/5.experiment.tex:79 -->
그림 §fig:general-t2i-vis에서 보여지는 바와 같이, InternVL-U는 일반적인 이미지 생성에서 특히 복잡한 텍스처와 뉘앙스 된 조명 효과를 렌더링하는 데 탁월한 시각적 충실성을 보여 주며 각 명령의 목적을 정확하게 캡처한다.

<!-- source:sections/5.experiment.tex:85-85 -->
**그림 설명.** ** 일반 이미지 생성의 시각화.** 다른 오픈소스 모델과 비교하면 InternVL-U는 복잡한 텍스처와 뉘앙스 된 조명 효과를 렌더링하는 데 탁월한 충실성을 보여 각 명령어의 정확한 의도를 캡처한다.

<!-- source:sections/5.experiment.tex:91 -->
#### 텍스트 중심 이미지 생성

<!-- source:sections/5.experiment.tex:93 -->
**CVTG-2k**. §tab:exp_cvtg에서는 복잡한 시각 텍스트 생성을 위해 고안된 CVTG-2k에 대한 결과를 제공한다. InternVL-U는 통일된 모델 중 최첨단 성능을 달성하며 평균 단어 정확도는 0.623이다.

<!-- source:sections/5.experiment.tex:96 -->
**LongText-Bench**. LongText-Bench는 이미지에 더 긴 텍스트를 렌더링 할 수있는 능력을 평가한다. §tab:exp_longtext에서 보여짐에 따라, InternVL-U는 영어에서 0.738 점수와 중국어로 0.860 점수를 가진 강력한 다국어 텍스트 생성을 보여준다. 이러한 결과는 이전 통일된 모델을 큰 소외로 우월한다. 이 결과는 우리의 모델이 읽기 쉬운 텍스트를 렌더링하는 통일된 모델의 이전 결함을 효과적으로 해결한다는 것을 보여준다.

<!-- source:sections/5.experiment.tex:101 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:102 -->
그림 §fig:text-generation-vis에서 보여지는 바와 같이 InternVL-U는 중국어와 영어 문자뿐만 아니라 더 높은 가독성과 유물 적은 수학적 상징을 렌더링하는 데 탁월한 능력을 보여준다. BAGEL 및 Ovis-U1와 비교하면 오픈소스 통일된 멀티모달 기본 라인과 비교하면 더 나은 텍스트 렌더링 품질을 달성하고 20B 대규모 모델 Qwen-Image 및 폐쇄적인 모델 Nano-Banana-Pro와 경쟁력을 유지하고 있다.

<!-- source:sections/5.experiment.tex:107-107 -->
**그림 설명.** ** 텍스트 중심의 이미지 생성의 시각화.*** 결과물들은 우리의 InternVL-U가 중국어, 영어 및 수치 공식의 상징을 렌더링하는 데 탁월한 능력을 가지고 있음을 보여준다. 오픈소스 통일된 멀티모달 모델 BAGEL 및 Ovis-U1과 비교하면 더 나은 렌더링 능력과 Qwen Image와 비교 가능한 성능을 가지고 있다.

<!-- source:sections/5.experiment.tex:113 -->
#### 지식 기반 이미지 생성

<!-- source:sections/5.experiment.tex:114 -->
**WISE**. WISE는 모델들이 텍스트에서 이미지로의 생성에 세계 지식을 통합할 수 있는지 여부를 평가한다. §tab:exp_wise에서 보여짐에 따르면, CoT와 InternVL-U는 상당한 성능 향상을 (전반 점수 0.46에서 0.58) 이룬다. BAGEL 및 UniWorld-V1와 같은 다른 통일된 기준선을 뛰어넘는 것으로, 문화 상식, 공간-시간 추론 및 자연 과학 분야에서 높은 능력을 제안한다.

<!-- source:sections/5.experiment.tex:116 -->
**GenExam**. GenExam는 시험 스타일 지침을 통해 학문적 지식으로 추론을 이해하는 텍스트에서 이미지에 대한 모델의 능력을 평가한다. §tab:exp_genexam에서, 우리의 모델은 물리학, 화학 및 생물학에 관한 통합 모델 중 가장 높은 점수를 달성한다. CoT로 강화된 InternVL-U는 3.7B 파라미터만 가지고 22.9의 전체 점수를 달성한다. 이것은 과학 중심의 이미지 이해와 생성, 추론 및 생성의 통합 능력에 대한 InternVL-U를 검증한다.

<!-- source:sections/5.experiment.tex:118 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:119 -->
그림 §fig:Knowledge-informed-t2i-vis에서 보여지는 바와 같이, 모델이 세계 지식을 이해하는 것을 필요로 하는 명령어들을 위해, InternVL-U는 더 강력한 지식 기반 렌더링을 제공하며 복잡한 명령어에 시각적으로 충실한 결과를 생산하고 명시적인 지식 통합 없이 기초 라인을 크게 뛰어넘습니다.

<!-- source:sections/5.experiment.tex:125-125 -->
**그림 설명.** ** 지식 정보 기반 이미지 생성의 시각화.** InternVL-U는 정확한 지식 렌더링에 뛰어난 능력을 나타낸다. 영역 지식을 효과적으로 통합함으로써, 우리의 모델은 복잡한 명령에 시각적으로 충실한 결과를 생산하고, 특정 세계 지식을 갖지 않는 기본선을 크게 뛰어넘습니다.

<!-- source:sections/5.experiment.tex:130 -->
### 이미지 편집

<!-- source:sections/5.experiment.tex:132 -->
이미지 편집을 위해 ImgEdit , GEdit-Bench , RISEBench의 기존 벤치마크를 사용한다. 또한 텍스트 편집의 광범위한 응용 시나리오를 고려하여 우리는 가상 및 실제 시나리오에서 텍스트 편집을 수행하는 모델의 정확성을 평가하기 위해 텍스트 중심의 이미지 편집 벤치마크인 TextEdit을 추가로 구축했습니다.

<!-- source:sections/5.experiment.tex:134 -->
#### 일반 이미지 편집

<!-- source:sections/5.experiment.tex:141 -->
**ImagEdit**

<!-- source:sections/5.experiment.tex:142 -->
ImgEdit은 단일 및 다중 회전 편집 작업의 다양한 범위를 다루고 있다.

<!-- source:sections/5.experiment.tex:143 -->
InternVL-U는 통일된 모델들 사이에서 경쟁력 있는 편집 능력을 입증하고 있으며, CoT 모델들은 전체 점수를 3.82으로 달성한다.

<!-- source:sections/5.experiment.tex:145 -->
**GEdit-Bench**. GEdit-Bench는 실제 편집 요구 사항 모두 있는 명령어를 포함합니다

<!-- source:sections/5.experiment.tex:146 -->
그리고 높은 다양성. §tab:exp_gedit에서, InternVL-U는 평균 6.66의 점수를 달성하고 BAGEL (6.52) 및 Ovis-U1 (6.42) 같은 기본선을 뛰어넘습니다. 특히, CoT 전략을 적용하면 성능이 더욱 향상되어 점수를 6.88으로 높인다. Qwen-Image-Edit 같은 전문 편집 모델은 여전히 특정 매트릭에서 선두를 차지하지만, InternVL-U의 성능은 다양한 편집 작업에 대한 통일된 아키텍처의 실행 가능성을 확인한다. 특히 명시적인 추론 단계와 함께 증강하면.

<!-- source:sections/5.experiment.tex:148 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:149 -->
그림 §fig:general-edit-vis에서 보여지는 바와 같이, InternVL-U는 원본 이미지의 조명 및 구조적 세부 사항을 보존하면서 현실적인 텍스처와 스타일을 생산하는 데 탁월하며, 다른 오픈 소스 모델과 비교하여 광범위한 시나리오에서 더 자연스럽고 일관된 편집을 초래한다.

<!-- source:sections/5.experiment.tex:154-154 -->
**그림 설명.** ** 일반 이미지 편집의 시각화.** InternVL-U는 다른 오픈소스 모델과 비교하여 다양한 작업에서 우수한 성능을 보여 주는 원본 이미지의 조명 및 구조적 세부 사항에 높은 충실성을 유지하면서 현실적인 텍스처와 스타일을 생성하는 데 탁월한다.

<!-- source:sections/5.experiment.tex:158 -->
#### 텍스트 중심 이미지 편집

<!-- source:sections/5.experiment.tex:161 -->
** 텍스트 편집**. 텍스트 편집 기능을 엄격하게 평가하기 위해 ** 텍스트 편집** 매트플라시 홀더0를 소개한다. 다양한 편집 시나리오와 고품질 편집 이미지 기반 진실을 특징으로하는 2,148 개의 샘플을 포함하는 신기준표 ( 참조 섹션 §sec:textedit 참조 참조 참조) 참조 표시 구조에 대한 자세한 내용은. §tab:exp_textedit_mllm,tab:exp_textedit_rule에서 나타난 바와 같이, InternVL-U는 이러한 기준표에서 뛰어난 성능을 보여, 나노 바나노 프로와 일치하는 F1 점수를 0.71으로 달성하고, U-U1 (0.35) 와 같은 통일된 평균을 크게 우월한다. 이 장점은 더 많은 BA-U1 (0.35) 과 같은 국제 정보통상 기반 평가에서 확인된다.

<!-- source:sections/5.experiment.tex:166 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:167 -->
§fig:text-bench-vis에서 보여지는 바와 같이, 우리는 제안된 벤치마크인 InternVL-U인 TextEdit에서 대표적인 최고 수준의 오픈소스 및 상업 모델의 성능을 시각화하여, 다양한 텍스트 편집 시나리오에서 강력한 결과를 달성한다. 특히, InternVL-U는 시각적 미술과 텍스트 정확성을 유지하면서 이미지에 대체되는 텍스트를 정확하게 위치화하고 표적 텍스트로 대체할 수 있다. 이러한 결과는 현재의 최신 기술 상황을 명확하게 보여주고 기존 텍스트 편집 기능의 상위 한계를 효과적으로 표시하고, 우리의 성능 벤치마크가 텍스트 중심의 이미지 편집의 경계를 어떻게 지각하는지를 강조한다.

<!-- source:sections/5.experiment.tex:172-173 -->
**그림 설명.** ** 텍스트 중심의 이미지 편집의 시각화**. InternVL-U는 보다 정확하고 충실한 텍스트 편집 기능을 보여 주면서 목표 편집 영역 이외의 텍스트 및 시각적 콘텐츠에 대한 강력한 일관성을 유지한다.

<!-- source:sections/5.experiment.tex:177 -->
#### 추론 기반 이미지 편집

<!-- source:sections/5.experiment.tex:180 -->
- ! !

<!-- source:sections/5.experiment.tex:181 -->
우리는 RISEBench 벤치마크에 대한 논리적 추출을 요구하는 복잡한 편집 명령어를 처리하는 모델의 능력을 추가로 평가했습니다. §tab:exp_rise에서 상세히 설명한 바와 같이, CoT 전략의 도입은 인수성 향상으로 주목할만한 성능을 가져오고, 3.6에서 9.4까지 인턴VL-U의 전체 점수를 높여줍니다. 이 향상은 오픈 소스 통일 기본 라인 (예를 들어, BAGEL 6.1) 과 Q-Image-Edit (8.9) 같은 전문 생성 모델 (전문) 을 뛰어넘을 수 있다. 특히, CoT는 명령어 추론 (IR) 과 외관 일관성 (AC) 을 크게 향상시켜 복잡하고 논리 의존적인 편집 작업을 정확하게 수행하는 데 명시적인 추론이 필수적임을 입증한다.

<!-- source:sections/5.experiment.tex:185 -->
** 질적 결과**

<!-- source:sections/5.experiment.tex:186 -->
§fig:reasoning-informed-edit-vis에서 보여준 바와 같이, InternVL-U는 여러 단계의 추론과 엄격한 논리적 제약을 필요로 하는 복잡한 편집 명령어를 이전 방법보다 더 신뢰할 수 있게 처리한다. 시간 계산 (예를 들어, 달력 날짜를 업데이트), 공간 및 문화 이해 (예를 들어, 이미지가 주어진 맥락에 적합한 시를 검색) 및 정확한 알고리즘 규칙 (예를 들어, 바이너리 검색 트리 삽입) 를 포함하여 다양한 제약을 정확하게 해석하고 실행할 수 있다.

<!-- source:sections/5.experiment.tex:192-192 -->
**그림 설명.** ** 추론에 기반한 이미지 편집의 시각화.** InternVL-U는 복잡한 명령어들을 처리하는 데 있어서 최첨단 모델을 능가한다. 여러 단계 추론을 필요로 한다. 결과는 우리의 모델의 뛰어난 능력을 입증하고, 달력 날짜를 업데이트하는 시간 계산, 시 배치에 대한 공간적 및 문화적 이해, 그리고 바이너리 검색 트리 삽입에 대한 정확한 알고리즘 규칙 등을 아우르는 다양한 논리적 제약을 정확하게 해석하고 실행한다.

<!-- source:sections/5.experiment.tex:199-199 -->
**그림 설명.** ** 좀 더 특별한 이미지 편집 예제들의 시각화.** InternVL-U는 복잡한 편집 작업에서 고급 공간적 추론과 정확한 제어력을 보여준다. 결과는 그래프 속성을 정확하게 식별하는 모델의 우수한 능력을 강조한다 (예를 들어 노드 정도), 적절한 표현으로 유머 중심의 콘텐츠를 생성하고, 좌표 벡터에 기반한 정확한 3D 기하학적 변환을 수행하며, 전문 영역에서 광범위한 적용성을 보여준다.

<!-- source:sections/5.experiment.tex:203 -->
### 추가 정성 결과

<!-- source:sections/5.experiment.tex:204 -->
그림 §fig:special-edit-vis에서 보여준 바와 같이, 우리는 표준 편집을 넘어서는 특수한 기능들을 보여주는 전문 편집 예제를 제시하고, 컴퓨터 과학 지식, 유머 중심의 콘텐츠 제작, 수학 관련 편집 등 비정상적인 요구사항을 강력하게 처리할 수 있도록 해줍니다.

<!-- source:tables/config-model.tex:3 -->
**표.** \textbf{InternVL-U 아키텍처의 상세한 구성.

<!-- source:tables/config-model.tex:1-18 -->
```text
\centering **Configuration** | **Visual Und. Encoder** | **Context Backbone** | **Visual Gen. Head**
# Layers             | 24      | 28     | 20
# Num Heads (Q / KV) | 16 / 16 | 16 / 8 | 12 / 12
Head Size             | 64      | 128    | 128
Intermediate Size     | 4,096   | 6,144  | 6,144
Patch / Scale Factor  | 14      | -      | 2
# Parameters         | 0.3B    | 2B     | 1.7B
```

<!-- source:tables/config-train.tex:3 -->
**표.** ** 다른 훈련 단계에 대한 하이퍼파라미터**

<!-- source:tables/config-train.tex:1-33 -->
```text
\centering } **Hyperparameters** | **Stage 1** | **Stage 2** | **Stage 3**
\multicolumn{4}{l}{*학습 가능 모듈*}
Backbone | \textcolor{red}{$\times$} | \textcolor{red}{$\times$} | \textcolor{green}{\checkmark}
Visual gen. head | \textcolor{green}{\checkmark} | \textcolor{green}{\checkmark} | \textcolor{green}{\checkmark}
Learning rate | 3e-04 | 1e-04 | 1e-05
LR scheduler | Constant | Cosine | Cosine
Weight decay | 0.0 | 0.0 | 0.01
Gradient norm clip | 0.2 | 0.2 | 1
Optimizer | \multicolumn{3}{c}{AdamW ($\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$)}
Warm-up steps | 1000
Training steps | 250,000 | 60,000 | 20,000
Batch size | 2048 | 1024 | 1024
Gen. resolution (min, max) | (512, 512) | (512, 1024) | (512, 1024)
Und. resolution (min, max) | (448, 448)
Diffusion timestep shift | 3.0
Data / tasks | T2I + IT2I | T2I + IT2I | T2I + IT2I + Und
Data ratio | 4:1 | 3:4 | 1:1:2
Loss weight (NTP:VP) | 0:1 | 0:1 | 1:20
```

<!-- source:tables/final/understand_reason_v2.tex:3 -->
**표.** **인터VL-U와 다중모달 이해와 추론 기준에 대한 기본 모델의 비교.** *는 우리의 평가 스크립트를 기반으로 한 결과를 나타낸다. ``A + B''의 통일 모델의 크기는 이해 (A) 및 세대 (B) 매개 변수를 별도로 나타낸다. } \resizebox{\textwidth}{!}{% 自动缩放以适应页面宽度

<!-- source:tables/final/understand_reason_v2.tex:1-33 -->
```text
\centering } \multirow{2}{*}{**Model**} | \multirow{2}{*}{**#Params**} | \multicolumn{4}{c|}{**Understanding**} | \multicolumn{3}{c}{**Reasoning**}
& | **MME-P ** | **SEED ** | **ChartQA ** | **OCRBench ** | **MMMU ** | **MathVerse ** | **LogicVista **
\multicolumn{9}{l}{*MLLMs w/o Generator*}
LLaVA-1.5V  | 7B | 1510.7 | 65.8 | 17.8 | 31.8 | 35.7 | 7.6 | --
Qwen2.5-VL  | 3B | 1574.9 | 73.7 | 84.0 | 79.7 | 53.1 | 31.2 | 40.3
InternVL3.5  | 2B | 1552.1 | 75.3 | 80.7 | 83.6 | 59.0 | 53.4 | 47.7
\multicolumn{9}{l}{*UMMs w/ Generator*}
JanusFlow  | 1.3B | 1333.1 | 70.5 | 42.4 | 53.2 | 29.3 | -- | --
Janus-Pro  | 1.5B | 1444.0 | 68.3 | 23.4 | 48.7 | 36.3 | -- | --
Show-o2  | 1.5B | 1450.9 | 65.6 | 40.0 | 24.5 | 37.1 | -- | --
TUNA  | 1.5B | 1461.5 | 69.3 | 82.1 | 71.9 | 39.1 | -- | --
MetaQuery-L  | 3B+1B | 1574.3 | 73.8 | -- | -- | 53.1 | -- | --
Ovis-U1  | 2.4B+1.2B | 1508.0* | 75.5* | 76.4* | 88.3 | 51.1 | 30.6* | 32.4*
Emu3  | 8B | -- | 68.2 | -- | 68.7 | 31.6 | -- | --
BAGEL  | 7B+7B | 1687.0 | 78.5 | 78.5 | 73.3 | 55.3 | 48.1* | 44.3*
InternVL-U | 2B+1.7B | 1607.5 | 75.2 | 76.6 | 83.9 | 54.7 | 45.6 | 40.3
```

<!-- source:tables/final/geneval.tex:3 -->
**표.** **GenEval에서 일반 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A (A) 및 B (B) 의 차원별 이해를 나타낸다. } \resizebox{\textwidth}{!}{% 自动缩放以适应页面宽度

<!-- source:tables/final/geneval.tex:1-32 -->
```text
\centering } **Model** | **#Params** | **Single Object** | **Two Object** | **Counting** | **Colors** | **Position** | **Color Attribution** | **Overall**
\multicolumn{9}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 0.98 | 0.81 | 0.74 | 0.79 | 0.22 | 0.45 | 0.66
SD3-Medium  | 2B | 0.99 | 0.94 | 0.72 | 0.89 | 0.33 | 0.60 | 0.74
Seedream 3.0  | - | 0.99 | 0.96 | 0.91 | 0.93 | 0.47 | 0.80 | 0.84
GPT Image 1 [High]  | - | 0.99 | 0.92 | 0.85 | 0.92 | 0.75 | 0.61 | 0.84
Z-Image  | 6B | 1.00 | 0.94 | 0.78 | 0.93 | 0.62 | 0.77 | 0.84
Qwen-Image | 20B | 0.99 | 0.92 | 0.89 | 0.88 | 0.76 | 0.77 | 0.87
\multicolumn{9}{l}{*통합 모델*}
Show-o2  | 7B | 1.00 | 0.87 | 0.58 | 0.92 | 0.52 | 0.62 | 0.76
Janus-Pro  | 7B | 0.99 | 0.89 | 0.59 | 0.90 | 0.79 | 0.66 | 0.80
UniWorld-V1  | 7B+13B | 0.99 | 0.93 | 0.79 | 0.89 | 0.49 | 0.70 | 0.80
OmniGen2  | 3B+4B | 1.00 | 0.95 | 0.64 | 0.88 | 0.55 | 0.76 | 0.80
BAGEL  | 7B+7B | 0.99 | 0.94 | 0.81 | 0.88 | 0.64 | 0.63 | 0.82
InternVL-U | 2B+1.7B | 0.99 | 0.94 | 0.74 | 0.91 | 0.77 | 0.74 | 0.85
```

<!-- source:tables/final/dpgbench.tex:3 -->
**표.** **DPG-Bench에서 일반적인 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A (A) 및 생성 (B) 매개 변수를 분리하여 이해한다는 것을 나타낸다. } \resizebox{0.85\textwidth}{!}{% 自动缩放以适应页面宽度

<!-- source:tables/final/dpgbench.tex:1-33 -->
```text
\centering } **Model** | **#Params** | **Global** | **Entity** | **Attribute** | **Relation** | **Other** | **Overall**
\multicolumn{8}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 82.10 | 89.50 | 88.80 | 91.10 | 89.40 | 84.00
SD3-Medium  | 2B | 87.90 | 91.01 | 88.83 | 80.70 | 88.68 | 84.08
GPT Image 1 [High]  | - | 88.89 | 88.94 | 89.84 | 92.63 | 90.96 | 85.15
Nano Banana Pro  | - | 91.00 | 92.85 | 91.56 | 92.39 | 89.93 | 87.16
Z-Image  | 6B | 93.39 | 91.22 | 93.16 | 92.22 | 91.52 | 88.14
Qwen-Image  | 20B | 91.32 | 91.56 | 92.02 | 94.31 | 92.73 | 88.32
Seedream 4.5  | - | 89.24 | 94.30 | 92.14 | 92.23 | 93.83 | 88.63
\multicolumn{8}{l}{*통합 모델*}
UniWorld-V1  | 7B+13B | 83.64 | 88.39 | 88.44 | 89.27 | 87.22 | 81.38
OmniGen2  | 3B+4B | 88.81 | 88.83 | 90.18 | 89.37 | 90.27 | 83.57
Ovis-U1  | 2.4B+1.2B | 82.37 | 90.08 | 88.68 | 93.35 | 85.20 | 83.72
Janus-Pro  | 7B | 86.90 | 88.90 | 89.40 | 89.32 | 89.48 | 84.19
BAGEL  | 7B+7B | 88.94 | 90.37 | 91.29 | 90.82 | 88.67 | 85.07
InternVL-U | 2B+1.7B | 90.39 | 90.78 | 90.68 | 90.29 | 88.77 | 85.18
```

<!-- source:tables/final/tiif-short.tex:3 -->
**표.** **TIIF (Short Prompts) 에서 일반 텍스트-영상 생성 능력 평가.** ``A + B'의 통일 모델의 크기는 A) 과 B) 의 생성 (B) 의 매개 변수를 구분하여 이해한다. 요약: **Attr**=Attribute, **Rel**=Relation, **A+R**=Attribute+Relation, **A+Re**=Attribute+Reasoning, **R+Re**=Relation+Reasoning, **RW**=Real World.}{\textwidth}{% \begin{tabular}{% \ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

<!-- source:tables/final/tiif-short.tex:1-36 -->
```text
\centering \multirow{2}{*}{**Model**} | \multirow{2}{*}{**#Params**} | \multicolumn{4}{c|}{**Basic Following**} | \multicolumn{6}{c|}{**Advanced Following**} | \multicolumn{1}{c|}{**Designer**} | \multirow{2}{*}{**Overall**}
& | **Avg** | **Attr** | **Rel** | **Reas** | **Avg** | **A+R** | **A+Re** | **R+Re** | **Style** | **Text** | **RW** &
\multicolumn{14}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 83.1 | 87.1 | 87.3 | 75.0 | 65.8 | 67.1 | 73.8 | 69.1 | 66.7 | 43.8 | 70.7 | 71.1
Z-Image  | 6B | 78.4 | 79.5 | 80.5 | 75.1 | 72.9 | 72.9 | 67.0 | 73.9 | 90.0 | 94.8 | 88.1 | 80.2
Seedream 3.0  | - | 87.1 | 90.5 | 89.6 | 80.9 | 79.2 | 79.8 | 77.2 | 75.6 | 100.0 | 97.2 | 83.2 | 86.0
Qwen-Image  | 20B | 86.2 | 90.5 | 88.2 | 79.8 | 79.3 | 79.2 | 78.9 | 75.6 | 100.0 | 92.8 | 90.3 | 86.1
\multicolumn{14}{l}{*통합 모델*}
Show-o  | 1.3B | 73.1 | 74.8 | 78.8 | 65.6 | 53.7 | 61.0 | 68.6 | 66.5 | 63.3 | 3.8 | 55.0 | 59.7
Janus-Pro  | 7B | 79.3 | 79.3 | 78.3 | 80.3 | 59.7 | 66.1 | 70.5 | 67.2 | 60.0 | 28.8 | 65.8 | 65.5
Ovis-U1  | 2.4B+1.2B | 77.8 | 83.5 | 80.1 | 69.9 | 67.4 | 71.8 | 66.8 | 69.0 | 83.3 | 8.1 | 67.2 | 66.7
BAGEL  | 7B+7B | 81.8 | 82.5 | 83.0 | 79.9 | 70.2 | 74.4 | 67.4 | 72.0 | 86.7 | 29.4 | 68.3 | 71.5
Lumina-DiMOO  | 8B | 84.9 | 87.0 | 87.6 | 79.8 | 72.8 | 74.8 | 76.8 | 69.8 | 70.0 | 51.1 | 75.0 | 74.7
InternVL-U | 2B+1.7B | 82.3 | 86.0 | 84.1 | 76.7 | 73.5 | 75.3 | 70.4 | 75.5 | 93.3 | 47.5 | 65.3 | 74.9
```

<!-- source:tables/final/tiif-long.tex:3 -->
**표.** **TIIF (장시간 명령어) 에서 일반적인 텍스트-영상 생성 능력 평가.** ``A + B'의 통일 모델의 크기는 이해 (A) 와 생성 (B) 매개 변수를 별도로 나타낸다. 요약: **Attr**=Attribute, **Rel**=Relation, **Reas**=Reasoning, **A+R**=Attribute+Relation, **A+Re**=Attribute+Reasoning, **R+Re**=Relation+Reasoning, **RW**=Real World.}

<!-- source:tables/final/tiif-long.tex:1-35 -->
```text
\centering \multirow{2}{*}{**Model**} | \multirow{2}{*}{**#Params**} | \multicolumn{4}{c|}{**Basic Following**} | \multicolumn{6}{c|}{**Advanced Following**} | \multicolumn{1}{c|}{**Designer**} | \multirow{2}{*}{**Overall**}
& | **Avg** | **Attr** | **Rel** | **Reas** | **Avg** | **A+R** | **A+Re** | **R+Re** | **Style** | **Text** | **RW** &
\multicolumn{14}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 78.7 | 83.2 | 80.4 | 72.4 | 68.5 | 73.7 | 73.3 | 71.6 | 66.7 | 52.8 | 71.5 | 71.8
Z-Image  | 6B | 82.8 | 86.5 | 79.9 | 81.9 | 77.0 | 77.6 | 73.8 | 75.6 | 93.3 | 93.2 | 85.5 | 83.0
Seedream 3.0  | - | 84.9 | 90.1 | 85.9 | 78.9 | 80.6 | 81.8 | 78.9 | 78.6 | 93.3 | 87.8 | 83.6 | 84.3
Qwen-Image  | 20B | 87.2 | 91.5 | 90.8 | 79.4 | 80.9 | 79.8 | 81.7 | 78.6 | 100.0 | 89.1 | 91.4 | 86.8
\multicolumn{14}{l}{*통합 모델*}
Show-o  | 1.3B | 75.8 | 79.8 | 78.3 | 69.3 | 50.4 | 56.8 | 69.0 | 56.2 | 66.7 | 2.8 | 50.9 | 58.9
Janus-Pro  | 7B | 78.3 | 82.3 | 73.3 | 79.1 | 58.8 | 56.2 | 70.8 | 60.0 | 70.0 | 33.8 | 60.3 | 65.0
Ovis-U1  | 2.4B+1.2B | 79.4 | 81.5 | 81.4 | 75.2 | 67.8 | 68.3 | 73.8 | 65.9 | 86.7 | 12.7 | 68.7 | 68.2
Lumina-DiMOO  | 8B | 78.0 | 81.5 | 79.8 | 72.6 | 68.5 | 74.1 | 69.1 | 66.4 | 63.3 | 40.7 | 72.0 | 68.8
BAGEL  | 7B+7B | 80.1 | 83.5 | 79.9 | 76.8 | 72.2 | 75.0 | 70.1 | 74.9 | 83.3 | 33.9 | 67.9 | 71.7
InternVL-U | 2B+1.7B | 81.5 | 81.5 | 82.2 | 80.9 | 72.7 | 76.2 | 67.6 | 75.8 | 83.3 | 50.7 | 66.8 | 73.9
```

<!-- source:tables/final/oneig.tex:3 -->
**표.** **OneIG-EN에서 일반적인 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A (A) 및 세대 (B) 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{0.9\textwidth}{!}{%自动缩放以应页宽度 \begin适应图表度}{lccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

<!-- source:tables/final/oneig.tex:1-32 -->
```text
\centering **Model** | **#Params** | **Alignment** | **Text** | **Reasoning** | **Style** | **Diversity** | **Overall**
\multicolumn{8}{l}{*생성 모델*}
SDXL  | 2.6B | 0.69 | 0.03 | 0.24 | 0.33 | 0.30 | 0.32
FLUX.1 [dev]  | 12B | 0.79 | 0.52 | 0.25 | 0.37 | 0.24 | 0.43
Qwen-Image  | 20B | 0.88 | 0.89 | 0.31 | 0.42 | 0.18 | 0.54
Z-Image  | 6B | 0.88 | 0.99 | 0.28 | 0.39 | 0.19 | 0.55
Seedream 4.5  | - | 0.89 | 1.00 | 0.35 | 0.43 | 0.21 | 0.58
Nano Banana Pro  | - | 0.89 | 0.94 | 0.33 | 0.48 | 0.25 | 0.58
\multicolumn{8}{l}{*통합 모델*}
Janus-Pro  | 7B | 0.55 | 0.00 | 0.14 | 0.28 | 0.37 | 0.27
Show-o2  | 7B | 0.82 | 0.00 | 0.23 | 0.32 | 0.18 | 0.31
Ovis-U1  | 2.4B+1.2B | 0.81 | 0.03 | 0.22 | 0.45 | 0.18 | 0.34
BAGEL  | 7B+7B | 0.77 | 0.24 | 0.17 | 0.37 | 0.25 | 0.36
Lumina-DiMOO  | 8B | 0.82 | 0.55 | 0.28 | 0.40 | 0.23 | 0.46
OmniGen2  | 3B+4B | 0.80 | 0.68 | 0.27 | 0.38 | 0.24 | 0.47
InternVL-U | 2B+1.7B | 0.82 | 0.74 | 0.27 | 0.40 | 0.25 | 0.50
```

<!-- source:tables/final/oneig-zh.tex:3 -->
**표.** **OneIG-ZH에서 일반적인 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A) 과 B) 과의 생성 (B) 의 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{0.9\textwidth}{!}{% 自动缩放以适应页面宽度 \begin{tabular}{lccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

<!-- source:tables/final/oneig-zh.tex:1-33 -->
```text
\centering **Model** | **#Params** | **Alignment** | **Text** | **Reasoning** | **Style** | **Diversity** | **Overall**
\multicolumn{8}{l}{*생성 모델*}
Qwen-Image  | 20B | 0.83 | 0.96 | 0.27 | 0.41 | 0.21 | 0.53
Z-Image  | 6B | 0.79 | 0.99 | 0.27 | 0.39 | 0.24 | 0.54
Seedream 4.5  | - | 0.83 | 0.99 | 0.30 | 0.43 | 0.21 | 0.55
Nano Banana Pro  | - | 0.84 | 0.98 | 0.31 | 0.46 | 0.24 | 0.57
\multicolumn{8}{l}{*통합 모델*}
Janus-Pro  | 7B | 0.32 | 0.15 | 0.10 | 0.26 | 0.36 | 0.24
BLIP-3o  | 8B | 0.61 | 0.09 | 0.21 | 0.37 | 0.23 | 0.30
Lumina-DiMOO  | 8B | 0.68 | 0.15 | 0.23 | 0.37 | 0.24 | 0.33
Ovis-U1  | 2.4B+1.2B | 0.72 | 0.15 | 0.21 | 0.43 | 0.20 | 0.34
BAGEL  | 7B+7B | 0.67 | 0.37 | 0.19 | 0.36 | 0.27 | 0.37
InternVL-U | 2B+1.7B | 0.75 | 0.90 | 0.23 | 0.37 | 0.26 | 0.50
```

<!-- source:tables/final/cvtg.tex:3 -->
**표.** **CVTG-2k에서 텍스트 중심의 텍스트-영상 생성 능력 평가.** ``A + B'의 통일 모델의 크기는 A (A) 및 생성 (B) 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{0.95\textwidth}{!}{% 自动缩放以适应页面宽度 \begin{tabular}{lcccccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lcclcclccl}{lccl}{lcclccl}{lcclccl}{lcc

<!-- source:tables/final/cvtg.tex:1-34 -->
```text
\centering \multirow{2}{*}{**Model**} | \multirow{2}{*}{**#Params**} | \multirow{2}{*}{**NED**} | \multirow{2}{*}{**CLIPScore**} | \multicolumn{5}{c}{**Word Accuracy**}
& | & | **2 regions** | **3 regions** | **4 regions** | **5 regions** | **average**
\multicolumn{9}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 0.688 | 0.740 | 0.609 | 0.553 | 0.466 | 0.432 | 0.497
Nano Banana Pro  | - | 0.875 | 0.737 | 0.737 | 0.775 | 0.786 | 0.793 | 0.779
Qwen-Image  | 20B | 0.912 | 0.802 | 0.837 | 0.836 | 0.831 | 0.816 | 0.829
Z-Image  | 6B | 0.937 | 0.797 | 0.901 | 0.872 | 0.865 | 0.851 | 0.867
Seedream 4.5  | - | 0.948 | 0.807 | 0.878 | 0.895 | 0.908 | 0.901 | 0.899
\multicolumn{9}{l}{*통합 모델*}
Ovis-U1  | 2.4B+1.2B | 0.477 | 0.725 | 0.133 | 0.109 | 0.091 | 0.065 | 0.093
BAGEL  | 7B+7B | 0.657 | 0.779 | 0.498 | 0.391 | 0.332 | 0.291 | 0.356
Lumina-DiMOO  | 8B | 0.805 | 0.831 | 0.723 | 0.646 | 0.571 | 0.505 | 0.590
InternVL-U | 2B+1.7B | 0.804 | 0.816 | 0.729 | 0.660 | 0.618 | 0.549 | 0.623
```

<!-- source:tables/final/longtext.tex:3 -->
**표.** **LongText-Bench에서 텍스트 중심의 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A (A) 및 생성 (B) 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{0.75\textwidth}{!}{% 自动缩放以适应页面宽度 \begin{tabular}{lccc}{lccc}

<!-- source:tables/final/longtext.tex:1-34 -->
```text
\centering **Model** | **#Params** | **LongText-Bench-EN** | **LongText-Bench-ZH**
\multicolumn{4}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 0.607 | 0.005
Z-Image  | 6B | 0.943 | 0.946
Qwen-Image  | 20B | 0.943 | 0.946
Nano Banana Pro  | - | 0.981 | 0.949
Seedream 4.5  | - | 0.989 | 0.987
\multicolumn{4}{l}{*통합 모델*}
Janus-Pro  | 7B | 0.019 | 0.006
BLIP-3o  | 8B | 0.021 | 0.018
Ovis-U1  | 2.4B+1.2B | 0.030 | 0.051
BAGEL  | 7B+7B | 0.373 | 0.310
Lumina-DiMOO  | 8B | 0.437 | 0.047
OmniGen2  | 3B+4B | 0.561 | 0.059
InternVL-U | 2B+1.7B | 0.738 | 0.860
```

<!-- source:tables/final/wise.tex:3 -->
**표.** **WISE에서 지식에 기반한 텍스트-영상 생성 능력 평가.** ``A + B''의 통일 모델의 크기는 A (A) 및 생성 (B) 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{\textwidth}{!}{%自动缩放以应页宽度 \begin适度 \tabularity}{lcccccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lcccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}{lccc}lcclccl}{c}lcclcclccl}{c}{c

<!-- source:tables/final/wise.tex:1-31 -->
```text
\centering **Model** | **#Params** | **Cultural** | **Time** | **Space** | **Biology** | **Physics** | **Chemistry** | **Overall**
\multicolumn{9}{l}{*생성 모델*}
SD3-Medium  | 2B | 0.43 | 0.50 | 0.52 | 0.41 | 0.53 | 0.33 | 0.45
FLUX.1 [dev]  | 12B | 0.48 | 0.58 | 0.62 | 0.42 | 0.51 | 0.35 | 0.50
Qwen-Image  | 20B | 0.63 | 0.62 | 0.76 | 0.60 | 0.72 | 0.39 | 0.63
\multicolumn{9}{l}{*통합 모델*}
Janus-Pro  | 7B | 0.30 | 0.37 | 0.49 | 0.36 | 0.42 | 0.26 | 0.35
Lumina-DiMOO  | 8B | 0.35 | 0.43 | 0.59 | 0.31 | 0.49 | 0.34 | 0.40
Ovis-U1  | 2.4B+1.2B | 0.36 | 0.46 | 0.64 | 0.35 | 0.52 | 0.28 | 0.42
BAGEL  | 7B+7B | 0.44 | 0.52 | 0.65 | 0.42 | 0.62 | 0.41 | 0.49
UniWorld-V1  | 7B+13B | 0.53 | 0.55 | 0.73 | 0.45 | 0.59 | 0.41 | 0.55
InternVL-U | 2B+1.7B | 0.37 | 0.51 | 0.68 | 0.39 | 0.62 | 0.39 | 0.46
InternVL-U (w/ CoT) | 2B+1.7B | 0.55 | 0.57 | 0.74 | 0.51 | 0.72 | 0.46 | 0.58
```

<!-- source:tables/final/genexam.tex:3 -->
**표.** ** 지식에 기반한 텍스트-진상 생성 능력 평가 (Relaxed Scores) ** ``A + B''의 통일 모델의 크기는 분리된 이해 (A) 및 생성 (B) 매개 변수를 나타낸다. 약자: ** 수학**=수학, ** 물리**=물리학, ** 화학**=화학, ** 생물**= 생물학, ** 지질학, ** 컴퓨터 과학, ** 공학, ** 경제**= 경제학, ** 역사**= 역사.

<!-- source:tables/final/genexam.tex:1-38 -->
```text
\centering }  **Model** | **#Params** | **Math** | **Phy** | **Chem** | **Bio** | **Geo** | **Comp** | **Eng** | **Econ** | **Music** | **Hist** | **Overall**
\multicolumn{13}{l}{*생성 모델*}
FLUX.1 [dev]  | 12B | 12.2 | 14.4 | 12.5 | 22.8 | 36.4 | 11.0 | 14.0 | 9.2 | 21.3 | 21.7 | 17.6
HunyuanImage-3.0  | - | 17.0 | 17.2 | 18.8 | 18.7 | 30.4 | 15.5 | 16.9 | 11.7 | 23.9 | 20.4 | 19.1
Qwen-Image  | 20B | 18.9 | 26.3 | 15.3 | 32.1 | 49.6 | 18.9 | 32.0 | 20.3 | 23.4 | 38.6 | 27.5
Seedream 4.5  | - | 44.7 | 63.4 | 48.9 | 75.8 | 67.6 | 57.9 | 69.7 | 67.3 | 38.0 | 55.0 | 58.8
GPT-Image-1.5  | - | 65.8 | 85.4 | 78.1 | 91.9 | 92.5 | 75.8 | 86.4 | 85.5 | 70.8 | 90.9 | 82.3
Nano Banana Pro  | - | 86.3 | 95.1 | 88.7 | 95.9 | 96.5 | 91.7 | 95.1 | 97.2 | 91.0 | 99.9 | 93.7
\multicolumn{13}{l}{*통합 모델*}
BLIP-3o  | 8B | 6.4 | 5.5 | 4.7 | 7.0 | 16.7 | 3.6 | 8.4 | 2.5 | 6.0 | 11.2 | 7.2
Janus-Pro  | 7B | 13.7 | 8.8 | 8.2 | 7.2 | 18.8 | 3.9 | 10.5 | 4.2 | 14.5 | 6.6 | 9.6
Ovis-U1  | 2.4B+1.2B | 12.2 | 10.8 | 6.6 | 10.0 | 25.4 | 6.1 | 8.8 | 5.4 | 13.2 | 15.1 | 11.4
BAGEL  | 7B+7B | 14.7 | 10.6 | 7.9 | 10.8 | 24.5 | 6.8 | 10.2 | 5.3 | 13.7 | 14.4 | 11.9
Show-o2  | 7B | 10.8 | 11.9 | 4.8 | 12.8 | 33.3 | 4.7 | 11.8 | 7.0 | 8.8 | 14.5 | 12.0
InternVL-U | 2B+1.7B | 21.5 | 22.2 | 19.3 | 20.0 | 31.2 | 9.9 | 19.6 | 21.5 | 17.8 | 24.9 | 20.8
InternVL-U (w/ CoT) | 2B+1.7B | 25.6 | 24.2 | 23.5 | 23.6 | 35.6 | 12.0 | 21.4 | 24.4 | 18.4 | 20.3 | 22.9
```

<!-- source:tables/final/imgedit.tex:3 -->
**표.** **ImgEdit에서 일반 이미지 편집 능력 평가.** ``A + B''의 통일 모델의 크기는 (A) 및 (B) 세대 매개 변수를 분리하여 이해한다는 것을 나타낸다.} \resizebox{\textwidth}{!}{% 自动缩放以适应页面宽度 \begin{tabular}{lccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

<!-- source:tables/final/imgedit.tex:1-34 -->
```text
\centering **Model** | **#Params** | **Add** | **Adjust** | **Extract** | **Replace** | **Remove** | **Background** | **Style** | **Hybrid** | **Action** | **Overall**
\multicolumn{12}{l}{*생성 모델*}
FLUX.1 Kontext  | 12B | 4.25 | 4.15 | 2.35 | 4.56 | 3.57 | 4.26 | 4.57 | 3.68 | 4.63 | 4.00
GPT-Image-1 [High]  | - | 4.61 | 4.33 | 2.90 | 4.35 | 3.66 | 4.57 | 4.93 | 3.96 | 4.89 | 4.20
Qwen-Image-Edit  | 20B | 4.38 | 4.16 | 3.43 | 4.66 | 4.14 | 4.38 | 4.81 | 3.82 | 4.69 | 4.27
Z-Image-Edit  | 6B | 4.40 | 4.14 | 4.30 | 4.57 | 4.13 | 4.14 | 4.85 | 3.63 | 4.50 | 4.30
\multicolumn{12}{l}{*통합 모델*}
Lumina-DiMOO  | 8B | 3.41 | 2.38 | 1.90 | 3.26 | 2.21 | 2.11 | 4.19 | 2.26 | 3.17 | 2.77
BAGEL  | 7B+7B | 3.56 | 3.31 | 1.70 | 3.30 | 2.62 | 3.24 | 4.49 | 2.38 | 4.17 | 3.20
UniWorld-V1  | 20B | 3.82 | 3.64 | 2.27 | 3.47 | 3.24 | 2.99 | 4.21 | 2.96 | 2.74 | 3.26
OmniGen2  | 3B+4B | 3.57 | 3.06 | 1.77 | 3.74 | 3.20 | 3.57 | 4.81 | 2.52 | 4.68 | 3.44
Ovis-U1  | 2.4B+1.2B | 3.99 | 3.73 | 2.66 | 4.38 | 4.15 | 4.05 | 4.86 | 3.43 | 4.68 | 3.97
InternVL-U | 2B+1.7B | 4.13 | 3.40 | 2.27 | 4.13 | 3.39 | 3.84 | 4.77 | 3.03 | 4.05 | 3.67
InternVL-U (w/ CoT) | 2B+1.7B | 4.24 | 3.80 | 2.58 | 4.36 | 3.51 | 3.92 | 4.69 | 3.00 | 4.31 | 3.82
```

<!-- source:tables/final/gedit.tex:3 -->
**표.** ** GEdit-Bench에서 일반 이미지 편집 능력 평가 .** ``A + B''의 통일 모델의 크기는 별도의 이해 (A) 및 생성 (B) 매개 변수를 나타낸다. 약자: **BC**= 배경 변경, **CA**= 색상 변경, **MM**=물질 변경, **MC**= 운동 변경, **PB**= 초상화 보아웃, **ST**= 스타일 전송, **SA**= 주체 추가, **SR**= 주체 제거, **SRp**= 주체 교체, **TM**= 텍스트 변경, **TT**= 음향 전송. } \resizebox{\textwidth}{!}{% 自动缩放以适应宽页面

<!-- source:tables/final/gedit.tex:1-31 -->
```text
\centering } **Models** | **#Params** | **BC** | **CA** | **MM** | **MC** | **PB** | **ST** | **SA** | **SR** | **SRp** | **TM** | **TT** | **Avg/G_O**
\multicolumn{14}{l}{*생성 모델*}
GPT Image 1  | - | 6.96 | 6.85 | 7.10 | 5.41 | 6.74 | 7.44 | 7.51 | 8.73 | 8.55 | 8.45 | 8.69 | 7.49
Qwen-Image-Edit  | 20B | 8.23 | 8.30 | 7.33 | 8.05 | 7.49 | 6.74 | 8.57 | 8.09 | 8.29 | 8.48 | 8.50 | 8.01
\multicolumn{14}{l}{*통합 모델*}
Lumina-DiMOO  | 8B | 3.43 | 4.27 | 3.08 | 2.77 | 4.74 | 5.19 | 4.44 | 3.80 | 4.38 | 2.68 | 4.20 | 3.91
Ovis-U1  | 2.4B+1.2B | 7.49 | 6.88 | 6.21 | 4.79 | 5.98 | 6.46 | 7.49 | 7.25 | 7.27 | 4.48 | 6.31 | 6.42
BAGEL  | 7B+7B | 7.32 | 6.91 | 6.38 | 4.75 | 4.57 | 6.15 | 7.90 | 7.16 | 7.02 | 7.32 | 6.22 | 6.52
InternVL-U | 2B+1.7B | 7.08 | 7.05 | 6.38 | 7.02 | 6.03 | 6.27 | 7.13 | 6.55 | 6.33 | 6.59 | 6.85 | 6.66
InternVL-U (w/ CoT) | 2B+1.7B | 7.05 | 7.87 | 6.50 | 6.99 | 5.77 | 6.10 | 7.33 | 7.16 | 7.12 | 7.36 | 6.46 | 6.88
```

<!-- source:tables/final/textedit-rule.tex:4 -->
**표.** ** 텍스트 중심의 이미지 편집의 평가 (Classic Metrics) 에 대한 텍스트 편집.** ``A + B'의 통일 모델의 크기는 (A) 이해와 (B) 생성 매개 변수를 별도로 나타낸다. ``Real'는 실제 세계 장면에서 나오는 이미지를 의미하며, ``Virtual'는 가상 장면에서 나오는 이미지를 의미한다. 약자: **OA**=OCR 정확성, **OP**=OCR 정확성, **OR**=OCR 회수, **F1**=OCR F1-Score, **NED**=ROI-Aware NED, **CLIP**=CLIPScore, **AES**=아스테틱 스코어. 자세한 평가 항목에 대한 자세한 측정 문서를 참조하십시오.

<!-- source:tables/final/textedit-rule.tex:1-45 -->
```text
\centering \multirow{2}{*}{**Models**} | \multirow{2}{*}{**# Params**} | \multicolumn{7}{c|}{**Real**} | \multicolumn{7}{c}{**Virtual**}
& | **OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES** | **OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES**
\multicolumn{16}{l}{\cellcolor{gray!15}*생성 모델*}
Qwen-Image-Edit  | 20B | 0.75 | 0.68 | 0.66 | 0.67 | 0.71 | 0.75 | 5.72 | 0.78 | 0.75 | 0.73 | 0.74 | 0.75 | 0.81 | 5.21
GPT-Image-1.5  | - | 0.74 | 0.69 | 0.67 | 0.68 | 0.68 | 0.75 | 5.78 | 0.73 | 0.72 | 0.71 | 0.71 | 0.70 | 0.80 | 5.28
Nano Banana Pro  | - | 0.77 | 0.72 | 0.70 | 0.71 | 0.72 | 0.75 | 5.79 | 0.80 | 0.78 | 0.77 | 0.78 | 0.78 | 0.81 | 5.28
\multicolumn{16}{l}{\cellcolor{gray!15}*통합 모델*}
Lumina-DiMOO  | 8B | 0.22 | 0.23 | 0.19 | 0.20 | 0.19 | 0.69 | 5.53 | 0.22 | 0.25 | 0.21 | 0.22 | 0.20 | 0.72 | 4.76
Ovis-U1  | 2.4B+1.2B | 0.40 | 0.37 | 0.34 | 0.35 | 0.35 | 0.72 | 5.32 | 0.37 | 0.40 | 0.38 | 0.39 | 0.33 | 0.75 | 4.66
BAGEL  | 7B+7B | 0.60 | 0.59 | 0.53 | 0.55 | 0.55 | 0.74 | 5.71 | 0.57 | 0.60 | 0.56 | 0.57 | 0.54 | 0.78 | 5.19
InternVL-U | 2B+1.7B | 0.77 | 0.73 | 0.70 | 0.71 | 0.72 | 0.75 | 5.70 | 0.79 | 0.77 | 0.75 | 0.75 | 0.77 | 0.80 | 5.12
```

<!-- source:tables/final/textedit-mllm.tex:3 -->
**표.** ** 텍스트 에디트 (MLLM 기반 매트릭스) 에서 텍스트 중심의 이미지 편집을 평가한다.** ``A + B''의 통일 모델의 크기는 분리된 이해 (A) 및 생성 (B) 매개 변수를 나타낸다. ``Real'는 실제 세계 장면에서 이미지 소스를 의미하며, ``Virtual'는 가상 장면에서 이미지를 의미한다. 약자: **TA**: 텍스트 정확성, **TP**: 텍스트 보존, **SI**: 장면 무결성, **LR**: 로컬 리얼리즘, **VC**: 시각적 일관성, **Avg**: MLLM 전체 평균. 자세한 평가 매트릭은 부록 섹션 §: 텍스트:

<!-- source:tables/final/textedit-mllm.tex:1-34 -->
```text
\centering  \multirow{2}{*}{**Models**} | \multirow{2}{*}{**# Params**} | \multicolumn{6}{c|}{**Real**} | \multicolumn{6}{c}{**Virtual**}
& | **TA** | **TP** | **SI** | **LR** | **VC** | **Avg** | **TA** | **TP** | **SI** | **LR** | **VC** | **Avg**
\multicolumn{14}{l}{*생성 모델*}
Qwen-Image-Edit  | 20B | 0.92 | 0.82 | 0.75 | 0.57 | 0.80 | 0.77 | 0.57 | 0.79 | 0.92 | 0.80 | 0.77 | 0.77
GPT-Image-1.5  | - | 0.96 | 0.94 | 0.86 | 0.80 | 0.93 | 0.90 | 0.82 | 0.93 | 0.96 | 0.91 | 0.87 | 0.90
Nano Banana Pro  | - | 0.96 | 0.95 | 0.85 | 0.88 | 0.93 | 0.91 | 0.87 | 0.92 | 0.96 | 0.94 | 0.89 | 0.92
\multicolumn{14}{l}{*통합 모델*}
Lumina-DiMOO  | 8B | 0.17 | 0.06 | 0.04 | 0.02 | 0.05 | 0.09 | 0.02 | 0.06 | 0.16 | 0.05 | 0.03 | 0.08
Ovis-U1  | 2.4B+1.2B | 0.31 | 0.12 | 0.12 | 0.07 | 0.18 | 0.18 | 0.06 | 0.16 | 0.31 | 0.14 | 0.13 | 0.19
BAGEL  | 7B+7B | 0.68 | 0.60 | 0.38 | 0.35 | 0.56 | 0.53 | 0.38 | 0.51 | 0.68 | 0.62 | 0.42 | 0.54
InternVL-U | 2B+1.7B | 0.94 | 0.90 | 0.71 | 0.80 | 0.80 | 0.88 | 0.87 | 0.86 | 0.91 | 0.82 | 0.62 | 0.83
```

<!-- source:tables/final/rise.tex:3 -->
**표.** **RISEBench에서 추론에 기반한 이미지 편집 능력을 평가 .** ``A + B''의 통일 모델의 크기는 A) 과 B) 의 차원별 이해의 매개 변수를 나타낸다. 요약: **IR**= 지침 추론, **AC**= 외관의 일관성, **VP****= 시각적 유연성.} \zazebox{0.9~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<!-- source:tables/final/rise.tex:1-33 -->
```text
\centering **Models** | **#Params** | **Temporal** | **Causal** | **Spatial** | **Logical** | **Overall** | **IR** | **AC** | **VP**
\multicolumn{10}{l}{*생성 모델*}
FLUX.1 Kontext  | 12B | 2.3 | 5.5 | 13.0 | 1.2 | 5.8 | 26.0 | 71.6 | 85.2
Qwen-Image-Edit  | 20B | 4.7 | 10.0 | 17.0 | 2.4 | 8.9 | 37.2 | 66.4 | 86.9
Seedream 4.0  | - | 12.9 | 12.2 | 11.0 | 7.1 | 10.8 | 58.9 | 67.4 | 91.2
Nano Banana Pro  | - | 41.2 | 61.1 | 48.0 | 37.6 | 47.2 | 77.0 | 85.5 | 94.4
GPT-Image-1.5  | - | 54.1 | 60.0 | 62.0 | 21.2 | 50.0 | 69.7 | 92.5 | 94.9
\multicolumn{10}{l}{*통합 모델*}
Lumina-DiMOO  | 8B | 2.4 | 1.1 | 4.0 | 1.2 | 2.2 | 34.0 | 50.7 | 72.3
Ovis-U1  | 2.4B+1.2B | 1.2 | 3.3 | 4.0 | 2.4 | 2.8 | 33.9 | 52.7 | 72.9
BAGEL  | 7B+7B | 2.4 | 5.6 | 14.0 | 1.2 | 6.1 | 36.5 | 53.5 | 73.0
InternVL-U | 2B+1.7B | 3.5 | 2.2 | 5.0 | 3.5 | 3.6 | 35.6 | 52.7 | 75.9
InternVL-U (w/ CoT) | 2B+1.7B | 4.7 | 7.8 | 1.8 | 5.9 | 9.4 | 43.9 | 64.4 | 79.7
```

<!-- source:sections/6.conclusion.tex:1 -->
## 결론

<!-- source:sections/6.conclusion.tex:3 -->
이 작업에서 우리는 이해, 추론, 생성 및 편집의 능력을 효과적으로 민주화하는 통일된 다모달 모델인 InternVL-U를 제시했습니다. 모달리티 특유의 모듈러리티와 분리된 시각 표현으로 통일된 컨텍스트 모델링의 원칙을 준수함으로써, 우리의 건축은 생산적 능력을 강력한 이해 척추로 원활하게 통합한다. 고 수준의 지능과 시각적 생성 사이의 격차를 더 잘 다하기 위해 우리는 체인 오브 튜트 (CoT) 패러다임과 함께 종합적인 데이터 합성 파이프라인을 도입하여 모형이 추상적 사용자 의도를 정확한 시각적 실행과 일치시킬 수 있도록했습니다. 경험적 결과는 InternVL-U는 지식-이용적인 생성 및 편집뿐만 아니라 AGM 및 시각적 추론에 대한 경쟁적 성능을 유지한다는 것을 확인한다. 우리는 UMM-I의 포괄적 인 발전을 가속화하고, 포괄적 인 발전을 위한 기대를 강화하고 있다.

<!-- source:sections/appendix.tex:1 -->
## TextEdit 벤치마크

<!-- source:sections/appendix.tex:4 -->
### 설계 동기

<!-- source:sections/appendix.tex:5 -->
실제 세계 응용 프로그램에서 텍스트-진상 및 이미지 편집 모델의 채택이 증가함에 따라 ** 텍스트 중심 이미지 편집**는 광고 디자인, 포스터 개정, UI 현지화 및 상업적 자산 업데이트에서 빈번한 요구 사항이되었습니다. 그러나 기존의 일반적 이미지 편집 모델은 텍스트 콘텐츠를 처리 할 때 신뢰할 수 없다. 한편으로는 생성 된 텍스트는 종종 철자 오류, 왜곡 된 글리프, 깨진 다 줄 라인 레이아웃 또는 배경과 부합된다. 한편으로는 텍스트를 대체하면서 모델은 종종 의도하지 않고 목표지 않은 지역을 변경한다. 예를 들어, 재료 텍스처, 얼굴 세부 사항 또는 배경 구조), 효과적으로 `` 편집 텍스트를 ' 전체 이미지'로 변환한다. 또한, 테이블에서 보여지는 것처럼: ``, e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e-e- 또한, 이러한 기준은 편집의 충실성과 시각적 보존에 대한 체계적인 평가가 부족한다.

<!-- source:sections/appendix.tex:8 -->
이미지 편집 모델의 능력을 종합적으로 평가하기 위해 **TextEdit**를 도입한다. 이것은 새로운, 세심하게 구성된 기준이다. TextEdit은 보다 체계적이고 세밀하고 인간으로 구성된 평가 프레임워크를 제공함으로써 기존 텍스트 중심의 편집 기준의 한계를 해결한다. 다음과 같은 주요 장점으로 구별된다.

<!-- source:sections/appendix.tex:10 -->
- **인류에서 관리된 데이터 파이프라인:** 합성 또는 자동으로 수집된 데이터에 크게 의존하는 이전 벤치마크와 달리, TextEdit은 고품질의, 현실적인 편집 시나리오를 보장하고 노이즈 또는 모호한 샘플을 줄이기 위해 인간으로 필터링된 파이프라인을 채택한다.
<!-- source:sections/appendix.tex:12 -->
- ** 수동적으로 표시된 지상 진실:** 우리는 정확한 양적 평가를 가능하게 하는 ** 수동적으로 편집된 지상 진실 (GT) 이미지를 제공 한다. 이것은 픽셀 수준의 충실성 매트릭의 신뢰할 수 있는 계산과 배경 보존의 정확한 평가를 지원한다.
<!-- source:sections/appendix.tex:14 -->
- **완료한 시나리오 분류:** TextEdit은 텍스트 편집 시나리오의 **18개의 다양한 하위 클래스를** 다루고 있으며, 제한적이거나 대략적인 분류를 가진 기존 벤치마크와 비교하여 보다 체계적이고 상세한 평가를 제공한다.
<!-- source:sections/appendix.tex:16 -->
- **LLM 기반 지침과 조화를 이루기:** 기준은 현대 LLM 기반 상호 작용과 조화를 이루는 순수한 텍스트- 지시 패러다임을 따르고 있다. 그것은 글리프 지도 또는 세그먼트 마스크와 같은 보조 입력의 필요성을 제거하여 명령에 따라하는 능력의 더 자연스러운 평가를 가능하게한다.
<!-- source:sections/appendix.tex:18 -->
- ** 하이브리드 평가 프로토콜:** 우리는 고전적인 OCR, 이미지 충실성 매트릭과 현대적인 멀티모달 LLM 기반 평가와 목표 정확성, 텍스트 보존, 장면 무결성, 로컬 리얼리즘 및 시각적 일관성을 결합한다. 이 쌍방향 프로토콜은 종합적인 평가를 가능하게한다.
<!-- source:sections/appendix.tex:21 -->
### 설계 세부사항

<!-- source:sections/appendix.tex:22 -->
실제 사용자 시나리오에 기반을 둔 TextEdit은 체계적인 ** 시나리오 분류학**과 강력한 ** 평가 프로토콜**을 통해 다양한 실제 요구와 모델 평가 사이의 격차를 다룬다. 이 통합 설계는 기술 텍스트 편집 성능과 실용적인 사용성을 모두 종합적으로 평가할 수 있다.

<!-- source:sections/appendix.tex:23 -->
#### 시나리오 분류체계

<!-- source:sections/appendix.tex:25 -->
본문 중심의 편집 시나리오를 두 개의 전반적인 영역으로 구성한다. ** 가상 장면** 및 ** 실제 세계 장면**. 이 세밀한 분류학은 §tab: 벤치마크-클래스에서 정의와 통계로 상세히 설명되어 있으며, * 포스터*, * 코믹*, * 슬라이드* 및 * GUI*와 같은 디지털 형식에서 * 제품*, * 빌딩*, * 보드 같은 미디어*, * 개인 액세스*, * 교통*, * 워터마크* 및 * 종이에 대한 미디어* 같은 실제 세계 환경까지 다양한 텍스트 통신자의 뉘앙스를 포착한다.

<!-- source:sections/appendix.tex:32-32 -->
**그림 설명.** \textbf{TextEdit 기준의 데이터 분포.

<!-- source:sections/appendix.tex:39 -->
#### 평가 지표

<!-- source:sections/appendix.tex:42 -->
텍스트 편집의 양적 평가는 특정 텍스트 콘텐츠를 조작하는 두 가지 요구 사항으로 인해 도전적이다. 전체적인 평가 제공을 위해 ** 클래식 매트릭스**와 **MLLM 기반 매트릭스를 결합한 하이브리드 평가 전략을 사용한다.

<!-- source:sections/appendix.tex:44 -->
** 클래식 매트릭스**는 텍스트의 존재와 정확성에 초점을 맞추고 있다. 우리는 편집 거리와 탐지 속도를 측정하기 위해 표준 OCR 도구를 사용한다. 구체적으로, 우리는 평가를 * 목표 지역* (편집 성공을 측정하는) 및 * 배경 지역* (보존 기능을 측정하는) 으로 분리한다. 또한, 우리는 일반적인 이미지 품질과 의미적 조화를 평가하기 위해 CLIPScore를 사용한다.

<!-- source:sections/appendix.tex:46 -->
**MLLM 기반의 메트릭스**는 ``ゴー스팅' 유물, 조명 불합동성 또는 부분 삭제를 더 잘 캡처하기 위해 추가로 도입된다. 전문가의 법학 분석을 시뮬레이션함으로써 우리는 가장 강력한 멀티모달 이해 모델을 Gemini-3-Pro를 판사로 사용하여 지역 현실주의와 장면 무결성 같은 차원에 대해 세밀한 점수를 제공한다. 인간의 선호도에 더 가깝게 조화를 이루는 평가를 제공한다.

<!-- source:sections/appendix.tex:48 -->
아래는 테이블 §tab:benchmark_metrics의 구조에 따라 조직된 각 평가 매트릭의 상세한 구현이 있다.

<!-- source:sections/appendix.tex:51 -->
**(a) 클래식 매트릭 ( 텍스트 중심) **

<!-- source:sections/appendix.tex:54 -->
먼저 레벤슈타인 거리를 기반으로 한 정상화 된 유사성 함수를 정의한다.

<!-- source:sections/appendix.tex:55-57 -->
```text
S(s_1, s_2) = 1 - frac{D_(lev)(s_1, s_2)}(max(|s_1|, |s_2|, 1))
```

<!-- source:sections/appendix.tex:58 -->
매플라세홀더0와 매플라세홀더1는 비교 문자열 두 개를 나타내고 매플라세홀더2는 각각의 길이를 나타낸다. 매플라세홀더3라는 용어는 명칭이 0이 아닌 것을 보장하기 위해 정상화 요소로 작용하여 매플라세홀더4의 유사점 점수를 매플라세홀더5 범위 내에서 제한하여 매플라세홀더6는 완벽한 일치를 나타낸다.

<!-- source:sections/appendix.tex:60 -->
* (i) OCR 정확성*

<!-- source:sections/appendix.tex:61 -->
이 측정값은 편집 영역에서 표본 텍스트가 올바르게 렌더링되었는지 여부를 평가한다. $\mathcal{T}_{gen}$는 생성된 이미지에서 발견된 텍스트 문자열의 집합이므로 표본 편집 영역과 크게 겹치는 것 (연합, $\text{IoU} > 0.5$). 정확도는 검출된 텍스트와 기본 진실 표본 텍스트 $t_{tgt}$ 사이의 최대 유사성으로 정의된다.

<!-- source:sections/appendix.tex:62-64 -->
```text
(Acc) = max_{t ∈ \mathcal(T)_(gen)} S(t, t_(tgt)) × P_(fail)
```

<!-- source:sections/appendix.tex:65 -->
여기서, $t$는 $\mathcal{T}_{gen}$ 집합 내에서 후보 문자열을 나타낸다. $\mathbb{P}_{fail}$라는 용어는 편집 시도가 실패한 경우 처벌을 위해 설계된 벌인 계수이다. 구체적으로, $\mathbb{P}_{fail}$는 원래 소스 텍스트 $t_{src}$이 여전히 지역에서 발견되는 경우 $t_{tgt}$의 표본 텍스트가 없는 경우 $0.2$로 설정된다. 그렇지 않으면, $\mathbb{P}_{fail} = 1.0$.

<!-- source:sections/appendix.tex:67 -->
*(ii) OCR 정확성*

<!-- source:sections/appendix.tex:68 -->
이 측정값은 배경 텍스트 보존의 정확성을 측정하여 환각 또는 잘못된 배경 텍스트를 처벌한다. 배경 영역에서 발견된 각 텍스트 항목 $t_i$ ( $\text{IoU} < 0.5$ 과 대상 지역) 에 대해 우리는 원본 배경 텍스트 $\mathcal{T}_{bg}^{orig}$에서 가장 잘 일치하는 것을 찾습니다.

<!-- source:sections/appendix.tex:69-71 -->
```text
(Precision) = frac(1){|\mathcal(T)_(bg)^(gen)|} Σ_{t ∈ \mathcal(T)_(bg)^(gen)} max_{t' ∈ \mathcal(T)_(bg)^(orig)} S(t, t')
```

<!-- source:sections/appendix.tex:72 -->
여기서 $\mathcal{T}_{bg}^{gen}$는 생성된 이미지에서 발견된 배경 텍스트의 집합을 나타내고 $|\mathcal{T}_{bg}^{gen}|$는 그 카드나리티이다. 이 측정값은 발견된 모든 배경 텍스트가 원본 텍스트와 밀접하게 일치하면 높은 점수를 달성하고, 따라서 거짓 텍스트 생성을 피한다.

<!-- source:sections/appendix.tex:74 -->
* (iii) OCR 회수*

<!-- source:sections/appendix.tex:75 -->
이 측정값은 배경 텍스트 보존의 완전성을 평가하여, 부족한 배경 텍스트를 처벌한다. $\mathcal{T}_{bg}^{orig}$에서 각 원본 배경 텍스트 $t'$에 대해 생성된 이미지에 얼마나 잘 보존되었는지 측정합니다:

<!-- source:sections/appendix.tex:76-78 -->
```text
(Recall) = frac(1){|\mathcal(T)_(bg)^(orig)|} Σ_{t' ∈ \mathcal(T)_(bg)^(orig)} max_{t ∈ \mathcal(T)_(bg)^(gen)} S(t, t')
```

<!-- source:sections/appendix.tex:79 -->
높은 기억은 원래 배경 텍스트의 대부분은 실수로 삭제되거나 변경되지 않고 편집된 이미지에 성공적으로 보존된다는 것을 나타낸다.

<!-- source:sections/appendix.tex:81 -->
*(iv) OCR F1 점수*

<!-- source:sections/appendix.tex:82 -->
F1 점수는 OCR 정확성 및 OCR 회수의 조화적 평균을 계산함으로써 균형 잡힌 매트릭을 제공한다.

<!-- source:sections/appendix.tex:83-85 -->
```text
(F1) = 2 × frac{(Precision) × (Recall)}{(Precision) + (Recall)}
```

<!-- source:sections/appendix.tex:86 -->
이 통일된 측정은 배경 텍스트 보존의 정확성과 완전성을 모두 파악하여 텍스트 수준의 편집 품질에 대한 포괄적인 평가를 제공한다.

<!-- source:sections/appendix.tex:88 -->
*(v) ROI-Aware NED*

<!-- source:sections/appendix.tex:89 -->
이 측정값은 원래 소스 텍스트 경계 상자에서 정의된 특정 관심 지역 (ROI) 내 편집 품질을 엄격하게 평가한다. ROI에서 추출된 예측 된 텍스트 문자열 $t_{pred}$와 목표 문자열 $t_{tgt}$ 사이의 유사성을 계산한다. 소스 텍스트와 잔여 유사성이 높을 경우 * 실패한 삭제 벌금 * 가 적용됩니다:

<!-- source:sections/appendix.tex:90-92 -->
```text
(NED) = S(t_(pred), t_(tgt)) × I_(resid)
```

<!-- source:sections/appendix.tex:93 -->
매프라세홀더0는 ROI에서 직접 추출된 OCR 인식 결과를 나타낸다. 매프라세홀더1는 상형 용어로 작용하는 잔여 지표 함수이다. 매프라세홀더2 (원 텍스트 매프라세홀더3가 효과적으로 삭제되지 않았다는 것을 암시하는) 와 매프라세홀더5은 그렇지 않습니다. 이 측정은 대상 영역이 올바른 새로운 텍스트를 포함하고 원본 텍스트를 완전히 제거하는 것을 보장한다.

<!-- source:sections/appendix.tex:96 -->
**(b) 클래식 매트릭스 (전반)**

<!-- source:sections/appendix.tex:99 -->
*(i) CLIPScore*

<!-- source:sections/appendix.tex:100 -->
CLIPScore를 사용하여 예측된 편집된 이미지와 캡션 텍스트 사이의 의미적 조화를 측정한다. 첫째, 우리는 Qwen3-VL를 사용하여 표시된 GT 이미지의 간결한 캡션 텍스트를 생성한다. 긴 길이는 CLIP 텍스트 코딩의 입력 제한을 만족한다. $\mathbf{v}_{img}$는 예측된 편집된 이미지의 CLIP 시각적 임베디션을 표시하고 $\mathbf{v}_{text}$는 생성된 캡션의 CLIP 텍스트 임베디션을 나타낸다. CLIPScore는 코시네 유사성으로 계산된다.

<!-- source:sections/appendix.tex:101-103 -->
```text
(CLIPScore) = frac{(v)_(img) · (v)_(text)}{|(v)_(img)| · |(v)_(text)|}
```

<!-- source:sections/appendix.tex:104 -->
더 높은 CLIPS 점수는 시각적 내용과 텍스트 설명 사이의 더 나은 의미적 일관성을 나타낸다. 이는 편집된 텍스트가 현장 맥락에 성공적으로 통합되는 것을 반영한다.

<!-- source:sections/appendix.tex:106 -->
*(ii) 미술 점수*

<!-- source:sections/appendix.tex:107 -->
생성된 이미지의 전체적인 시각적 매력을 평가하기 위해 CLIP 기반의 미술 예측을 사용한다. $f_{\text{aes}}(\cdot)$는 미적 품질 점수에 임베디션된 CLIP 이미지를 지도하는 미술 예측 모델을 나타낼 수 있다.

<!-- source:sections/appendix.tex:108-110 -->
```text
(AesScore) = f_{(aes)}((v)_(img))
```

<!-- source:sections/appendix.tex:111 -->
미적 점수는 일반적으로 1에서 5 (또는 정상화 후 0에서 1) 사이로 나뉘는데, 더 높은 값은 더 나은 시각적 품질, 구성 및 인식적 호소성을 나타낸다. 이 측정은 텍스트 편집이 전체 이미지 품질을 떨어뜨리지 않도록 돕습니다.

<!-- source:sections/appendix.tex:114 -->
**(c) MLLM 기반 매트릭스**

<!-- source:sections/appendix.tex:117 -->
우리는 강력한 상업 MLLM (즉 Gemini-3-Pro-Preview) 를 사용하여 $N=5$ 차원 ($D_1$에서 $D_5$) 를 통해 전문가의 법학적 분석을 시뮬레이션한다. 각 차원은 1에서 5까지의 리커트 스케일에서 평가된다. 더 높은 점수는 더 나은 품질을 나타낸다.

<!-- source:sections/appendix.tex:120 -->
*(i) 목표 정확성 ($D_1$).*

<!-- source:sections/appendix.tex:121 -->
이 차원은 편집된 지역에서 표본의 철자 정확성과 삭제 품질을 평가한다. MLLM는 다음과 같은 기준으로 $s_1 \in [1, 5]$ 점수를 부여한다.

<!-- source:sections/appendix.tex:123 -->
- 목적 텍스트가 올바른 철자법으로 번역되었는지
<!-- source:sections/appendix.tex:124 -->
- 원본 텍스트가 완전히 삭제되었는지
<!-- source:sections/appendix.tex:125 -->
- 새로운 텍스트의 시각적 명확성과 읽기 쉬운
<!-- source:sections/appendix.tex:127 -->
5의 점수는 원본 텍스트에서 잔류 유물이 없는 완벽한 텍스트 교체를 나타낸다.

<!-- source:sections/appendix.tex:129 -->
*(ii) 텍스트 보존 ($D_2$).*

<!-- source:sections/appendix.tex:130 -->
이 차원은 타겟이 아닌 배경 텍스트가 편집 작업에 영향을 받지 않고 그대로 남아 있는지 여부를 평가한다. MLLM는 다음과 같은 것을 평가한다.

<!-- source:sections/appendix.tex:132 -->
- 배경 텍스트 보존의 완전성
<!-- source:sections/appendix.tex:133 -->
- 주변 텍스트에 의도하지 않은 변경 사항이 없는 경우
<!-- source:sections/appendix.tex:134 -->
- 텍스트 레이아웃과 위치 보존
<!-- source:sections/appendix.tex:136 -->
$s_2 \in [1, 5]$ 점수는 모델이 원래의 배경 텍스트 요소를 성공적으로 보존하는 정도를 반영한다.

<!-- source:sections/appendix.tex:138 -->
*(iii) 장면의 무결성 ($D_3$).*

<!-- source:sections/appendix.tex:139 -->
이 차원은 배경 기하학과 물체의 안정성을 측정하고 편집 과정에서 도입된 구조적 왜곡이나 유물들을 확인한다. 평가 기준은 다음과 같습니다.

<!-- source:sections/appendix.tex:141 -->
- 건축 요소, 객체 경계가 보존되고 공간적 관계가 보존된다.
<!-- source:sections/appendix.tex:142 -->
- 기하학적 왜곡이나 왜곡 효과가 없는 경우
<!-- source:sections/appendix.tex:143 -->
- 장면 관점과 깊이 신호의 유지
<!-- source:sections/appendix.tex:145 -->
$s_3 \in [1, 5]$ 점수는 전체적인 장면 구조가 얼마나 잘 유지되고 있는지 나타낸다.

<!-- source:sections/appendix.tex:147 -->
*(iv) 지역 현실주의 ($D_4$).*

<!-- source:sections/appendix.tex:148 -->
이 차원은 편집된 지역에서 인 페인트링의 질을 평가하며 다음과 같은 사항에 초점을 맞추고 있다.

<!-- source:sections/appendix.tex:150 -->
- 편집된 지역과 원본 지역 사이의 가장자리 청결성과 원활성
<!-- source:sections/appendix.tex:151 -->
- 미분화, 유령화,  등의 눈에 보이는 유물들이 없는 상태
<!-- source:sections/appendix.tex:152 -->
- 새로운 텍스트와 그 직경 환경의 자연적인 통합
<!-- source:sections/appendix.tex:154 -->
$s_4 \in [1, 5]$ 점수는 지역 편집 지역의 사진 현실적 품질을 반영한다.

<!-- source:sections/appendix.tex:156 -->
*(v) 시각적 일관성 ($D_5$).*

<!-- source:sections/appendix.tex:157 -->
이 차원은 원본 장면 맥락과 글꼴 스타일, 조명 및 텍스처의 조화를 평가한다. MLLM는 다음과 같이 평가한다.

<!-- source:sections/appendix.tex:159 -->
- 주변 텍스트 또는 장면 미술과 글꼴 스타일의 일관성
<!-- source:sections/appendix.tex:160 -->
- 조명 방향, 강도, 색상 온도 일치
<!-- source:sections/appendix.tex:161 -->
- 배경과 자연스럽게 혼합되는 그림자 가스팅과 텍스처 패턴
<!-- source:sections/appendix.tex:163 -->
$s_5 \in [1, 5]$ 점수는 편집된 텍스트가 전체적인 시각적 스타일에 얼마나 잘 통합되는지를 측정한다.

<!-- source:sections/appendix.tex:166 -->
*(vi) 점수 정상화 및 절감 메커니즘.*

<!-- source:sections/appendix.tex:167 -->
매프라세홀더1의 원본 리커트 점수는 매프라세홀더1로 매핑을 사용하여 매프라세홀더2로 정상화된다. 평가 유효성을 보장하기 위해 **Cutoff 메커니즘을 구현합니다**: 주요 편집 작업 (목표 텍스트 정확성, $D_1$) 가 크게 실패하면 (즉, $s_1 < 4$), 부차적 차원의 점수는 0으로 처벌된다. 실패한 텍스트 편집자가 다른 품질 평가 점수를 의미없게 만듭니다. 최종 중량 $V_{score}$는 다음과 같이 구성됩니다:

<!-- source:sections/appendix.tex:168-170 -->
```text
V_(score) = w_1 s'_1 + I_((s_1 ≥ 4)) · Σ_(i=2)^(5) w_i s'_i
```

<!-- source:sections/appendix.tex:171 -->
이 문법:

<!-- source:sections/appendix.tex:173 -->
- $s'_i$는 $i$ 차원의 정상화된 점수를 나타낸다.
<!-- source:sections/appendix.tex:174 -->
- $w_i$는 $i$ 차원에 부여된 무게를 나타낸다. $\sum_{i=1}^{5} w_i = 1$를 만족시킵니다. 기본적으로 우리는 $w_1 = 0.4$, $w_2 = 0.3$, $w_3 = 0.1$, $w_4 = 0.1$, $w_5 = 0.1$을 사용한다.
<!-- source:sections/appendix.tex:175 -->
- $s_1$는 기본 텍스트 정확성 차원의 원본 점수를 나타낸다.
<!-- source:sections/appendix.tex:176 -->
- $\mathbb{I}_{(s_1 \ge 4)}$는 매프라CEHOLDER1 조건이 충족되면 매프라CEHOLDER1과 다른 조건이 충족되면 매프라CEHOLDER3와 동등한 지표 함수이다. 이것은 텍스트 내용이 잘못되면 (점 $<4$), 배경의 시각적 품질 (매치 $D_2$에서 $D_5$) 은 최종 점수에 기여하지 않습니다.
<!-- source:sections/appendix.tex:180 -->
*(vii) MLLM 전체 평균*

<!-- source:sections/appendix.tex:181 -->
전체 MLLM 기반 매트릭은 5개 차원의 중계 평균으로 정의되며, 절감 메커니즘이 적용된다.

<!-- source:sections/appendix.tex:182-184 -->
```text
(MLLM Overall Avg) = V_(score) = w_1 s'_1 + I_((s_1 ≥ 4)) · Σ_(i=2)^(5) w_i s'_i
```

<!-- source:sections/appendix.tex:185 -->
이 종합 매트릭은 기본 편집 실패에 대한 적절한 처벌과 함께, 주요 텍스트 편집 성공과 두 번째 시각 품질 요소를 모두 포착하는 단일 규모 값을 제공한다. 매트릭은 기준의 ** 가상** (합성 장면, 카테고리 1.x.x) 및 ** 실제** (실현 세계 장면, 카테고리 2.x) 하위 집합을 위해 개별적으로 계산되며, 각 각 장의 미세한 성능 분석을 가능하게한다.

<!-- source:sections/appendix.tex:189 -->
{% \sfamilie % 开始无线字体模式

<!-- source:sections/appendix.tex:191 -->
당신은 전문가의 형사 이미지 분석가이자 디자인 QA 전문가가에요

<!-- source:sections/appendix.tex:193 -->
여러분의 임무는 3개의 이미지를 비교하여 인공지능 편집된 이미지의 품질을 평가하는 것이다.

<!-- source:sections/appendix.tex:195 -->
**사진 (순위):**

<!-- source:sections/appendix.tex:197 -->
- **본 이미지**: 텍스트를 포함하고 있는 편집되지 않은 소스 이미지 ``\{raw_text\}''.
<!-- source:sections/appendix.tex:198 -->
- **Ground Truth Image**: 이상적인 결과를 텍스트로 보여주는 인간 제작된 참조 ``\{target_text\}''.
<!-- source:sections/appendix.tex:199 -->
- ** 편집된 이미지**: AI에서 생성된 결과를 평가한다.
<!-- source:sections/appendix.tex:202 -->
** 편집 작업 정보:**

<!-- source:sections/appendix.tex:204 -->
- ** 삭제해야 할 텍스트**: ``\{raw_text\}'
<!-- source:sections/appendix.tex:205 -->
- ** 텍스트 추가**: ``\{target_text\}'
<!-- source:sections/appendix.tex:208 -->
**평가  (1-5 점수 시스템) **

<!-- source:sections/appendix.tex:210 -->
** 편집된 이미지**를 다음 5가지 차원에 기초하여 평가해 주십시오. 아래의 엄격한 기준을 사용하여 1에서 5까지의 점수를 부여한다.

<!-- source:sections/appendix.tex:211 -->
} % 结束字体作用域

<!-- source:sections/appendix.tex:216 -->
**Q1. [목표 텍스트 정확성]**

<!-- source:sections/appendix.tex:218 -->
``\{target_text\}'}의 철자, 삭제 정확성, 읽기 가능성

<!-- source:sections/appendix.tex:220 -->
- **5 (완전) **: 정확한 철자 일치 (사건에 민감한). 오래된 텍스트는 완전히 삭제되었습니다. 귀신화 없다.
<!-- source:sections/appendix.tex:221 -->
- **4 (미소 결함)**: 텍스트는 정확하지만 1자 문자 오류/타이포, 또는 가벼운 인체 문제, 또는 매우 희미한 유령화만 면밀히 검사하면 볼 수 있다.
<!-- source:sections/appendix.tex:222 -->
- **3 (읽기 가능하지만 결함) **: 2~3개의 문자 오류가 있지만 단어 인식이 가능한다. 또는 청결성에 영향을 미치는 오래된 텍스트의 유령화/유적물들이 눈에 띄는 경우.
<!-- source:sections/appendix.tex:223 -->
- **2 (중위 오류) **: $>$3 문자 오류 (거대하게 잘못 표기) 또는 오래된 텍스트는 여전히 명확하게 읽을 수 있습니다 (실패 삭제).
<!-- source:sections/appendix.tex:224 -->
- **1 (실패) **: 텍스트가 없어지고, 거스란하거나 완전히 잘못된 단어이다. 오래된 텍스트는 완전히 손상되지 않았습니다.
<!-- source:sections/appendix.tex:230 -->
**Q2. [목적 없는 텍스트 보존]**

<!-- source:sections/appendix.tex:232 -->
*중심: 편집된 목표 이외의 배경 텍스트의 보존/독성성.*

<!-- source:sections/appendix.tex:234 -->
- **5 (완전)**: 모든 타겟 아닌 텍스트는 100% 보존되고 읽을 수 있으며, 원본/GT와 동일한다.
<!-- source:sections/appendix.tex:235 -->
- **4 (좋은) **: 주요 배경 텍스트는 보존되어 있다. 작은 먼 텍스트는 약간 부드럽고 미묘하지만 여전히 읽을 수 있다.
<!-- source:sections/appendix.tex:236 -->
- **3 (공정) **: 두 개의 중추 텍스트 요소가 흐려지고, 손상되거나, 실종된다.
<!-- source:sections/appendix.tex:237 -->
- **2 (빈)**: 중요한 가까운 텍스트 (목적과 직접한) 는 손상되거나 지워지거나 환각된다.
<!-- source:sections/appendix.tex:238 -->
- **1 (멸종) **: 배경 텍스트의 광범위한 파괴 또는 환각.
<!-- source:sections/appendix.tex:244 -->
**Q3. [세계적인 무대 무결성]**

<!-- source:sections/appendix.tex:246 -->
*중심: 편집되지 않은 영역의 기하학적 안정성 ( 배경, 물체, 사람) *

<!-- source:sections/appendix.tex:248 -->
- **5 (완전) **: 배경 기하학의 픽셀-완전 보존. 왜곡이 없다.
<!-- source:sections/appendix.tex:249 -->
- **4 (좋은) **: 거의 완벽하지만 배경 선이나 관점에서 매우 작은 변화 ($<$1%)
<!-- source:sections/appendix.tex:250 -->
- **3 (알릴 수 있는)**: 직선 (파) 에서 보이는 왜곡 또는 물체/면체의 가벼운 왜곡.
<!-- source:sections/appendix.tex:251 -->
- **2 (중심) **: 큰 구조적 손해 (예를 들어, 사람의 얼굴이 녹아, 건물이 붕괴되었다).
<!-- source:sections/appendix.tex:252 -->
- **1 (Chaos) **: 장면 구조는 오리지널과 비교했을 때 완전히 변경되거나 무의미한다.
<!-- source:sections/appendix.tex:258 -->
**Q4. [지역현실주의와 유물]**

<!-- source:sections/appendix.tex:260 -->
*중심: 화면 질, 가장자리 청결성, 그리고 편집된 영역을 원활하게 만드는 것.*

<!-- source:sections/appendix.tex:262 -->
- **5 (우수) **: 보이지 않는 편집. 깨끗한 가장자리, 반짝이는 빛, 얼룩없는. 전문적인 품질.
<!-- source:sections/appendix.tex:263 -->
- **4 (좋은) **: 매우 작은 유물 (예를 들어, 확대에서 약간의 픽셀레이션) 하지만 한 눈에 자연스러운 것 같습니다.
<!-- source:sections/appendix.tex:264 -->
- **3 (공정한) **: 눈에 보이는 , 흐릿한 정사각형 패치, 또는 ``'무더러진' 텍스트를 둘러보세요.
<!-- source:sections/appendix.tex:265 -->
- **2 (빈) **: 명백한 유물, 엉뚱한 가장자리, 또는 흰색/검은 상자 유물.
<!-- source:sections/appendix.tex:266 -->
- **1 (쓰레기) **: 편집된 영역은 손상된 파일이나 순수한 소음처럼 보이다.
<!-- source:sections/appendix.tex:269-269 -->
**그림 설명.** **MLLM 기반의 자동 평가**에 사용되는 시스템 프롬프트 템플릿, 분석가 인격, 작업 정의 및 첫 번째 네 가지 점수 차원을 포함하는 (Q1~Q4).

<!-- source:sections/appendix.tex:276 -->
**Q5. [아스테틱 & 라이트링 하모니]**

<!-- source:sections/appendix.tex:278 -->
*중심: 스타일 (font), 조명, 그림자, 그리고 텍스처 조화.*

<!-- source:sections/appendix.tex:280 -->
- **5 (무연한) **: 글꼴 스타일은 GT/콘텍스트와 완벽하게 일치한다. 조명/늘은 물리적으로 올바릅니다. 텍스처 (밀) 는 사진과 일치한다.
<!-- source:sections/appendix.tex:281 -->
- **4 (융합) **: 좋은 스타일 일치. 조명 은 대부분 정확 한다. 질감 은 약간 부드럽지만 수용 할 수 있다.
<!-- source:sections/appendix.tex:282 -->
- **3 (공예) **: 텍스트는 '`` pasted on' (디지털 스티커 లుక్) 로 보인다. 글꼴 스타일은 일반적 (예를 들어, Arial) 이며, 현상과 충돌한다.
<!-- source:sections/appendix.tex:283 -->
- **2 (부동) **: 잘못된 색상, 잘못된 관점, 또는 필요한 경우 그림자가 없다.
<!-- source:sections/appendix.tex:284 -->
- **1 (불합동) **: 텍스트는 무섭게 떠다니며, 전체적으로 현장의 물리학과 스타일을 무시한다.
<!-- source:sections/appendix.tex:290 -->
** 최종 출력 형식 (JSON만) **

<!-- source:sections/appendix.tex:292 -->
두 개의 사전을 포함하는 유효한 JSON 객체를 출력해야 합니다: 점수 (전수) 및 이유 (줄).

<!-- source:sections/appendix.tex:294 -->
** 예제 출력:**

<!-- source:sections/appendix.tex:299 -->
** 지침:** *"문서 \textquotesingle MUSIC\textquotesingle\ 를 \textquotesingle PARTY\textquotesingle 로 대체하십시오."*

<!-- source:sections/appendix.tex:308 -->
"점수":

<!-- source:sections/appendix.tex:309 -->
"Q1": 5, \\

<!-- source:sections/appendix.tex:310 -->
"Q2": 1, \\

<!-- source:sections/appendix.tex:311 -->
"Q3": 2, \\

<!-- source:sections/appendix.tex:312 -->
"Q4": 5, \\

<!-- source:sections/appendix.tex:313 -->
"Q5": 4 \\

<!-- source:sections/appendix.tex:315 -->
"유의":

<!-- source:sections/appendix.tex:316 -->
"Q1": "목적 텍스트 \textquotesingle PARTY\textquotesingle\는 올바르게 철자 되어 있으며 명확하게 읽을 수 있다. 제거해야 할 특정 목표 텍스트 (\textquotesingle MUSIC\textquotesingle\) 는 Ghosting 없이 완전히 사라졌습니다.", \\

<!-- source:sections/appendix.tex:317 -->
"Q2": "모델은 타겟 아닌 텍스트를 널리 파괴했습니다. \textquotesingle NIGHT CLUB\textquotesingle\ , \textquotesingle 31 OCT\textquotesingle\ , \textquotesingle FREE Drinks\textquotesingle\ , \textquotesingle LIVE\textquotesingle\ , \textquotesingle PRICE\textquotesingle\ 모두 잘못 제거되었고 \textquotesingle 10\$\textquotesingle\ , \textquotesingle 1TY\textquotesingle\ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \ , \textquotesingle \textquotesingle \ , \textquotesingle \ , \textquotesingle , \textquotesingle , \textquotesingle , \textquotes

<!-- source:sections/appendix.tex:318 -->
"Q3": "세계적인 장면의 무결성이 심각하게 손상되었습니다. 마라카를 쥐고 있는 골격 의 팔이 지워졌고, 마라카가 공중에서 떠 있는 것을 남겨두고, 이 그림의 물리적 논리를 깨뜨렸습니다".

<!-- source:sections/appendix.tex:319 -->
"Q4": "말론적 오류에도 불구하고, 이미지의 기술 품질은 훌륭하다. 가장자리는 날카롭고, 배경 색상은 매끄럽고, 눈에 보이는 픽셀 유물, 흐릿하거나 소음이 없습니다".

<!-- source:sections/appendix.tex:320 -->
"Q5": "PARTY\textquotesingle\textquotesingle\에 선택된 글꼴 스타일은 포스터의 손으로 그려진 벡터 미술과 잘 통합되지만, 색상은 원본 텍스트의 밝은 빨간색과 비교했을 때 더 어두운 갈색입니다". \\

<!-- source:sections/appendix.tex:336 -->
JSON 블록 외부에서 표시 또는 대화 텍스트를 출력하지 마십시오.

<!-- source:sections/appendix.tex:339-339 -->
**그림 설명.** **평가를 위한 명령어**의 계속과 최종 점수 차원 (Q5) 과 분석 결과에 필요한 엄격한 JSON 출력 스케마를 상세히 설명한다.

<!-- source:sections/appendix.tex:344 -->
### MiniSet-500 결과

<!-- source:sections/appendix.tex:345 -->
오픈소스 커뮤니티에 대한 가벼운 표준화된 평가 하위집단을 제공하기 위해, 우리는 전체 텍스트 에디트 벤치마크에서 **MiniSet-500**를 구축한다. 시나리오 유형 중 균형있는 분포를 보장하기 위해 18 가지 하위 범주 중 각에서 무작위로 샘플링 인스턴스를 사용하여 구축된다. MiniSet-500는 전체 **500 이미지 편집 쌍을 포함한다. 작업의 다양성을 보존하면서 평가 비용을 크게 줄이다. 그것은 빠른 벤치마크 및 압축 연구의 효율적인 프로토콜으로 작용하지만, 전체 벤치마크는 종합적인 평가의 표준이 남아 있다. 테이블:expedit_text_rule_min 및 테이블 §miniset-text-mllm에서 우리는 텍스트 에디트-MiniSet 벤치마크에 대한 다양한 모델의 성능을보고한다.

<!-- source:sections/appendix.tex:350 -->
## 데이터 구축 세부사항

<!-- source:sections/appendix.tex:352 -->
이 섹션에서는 데이터 구축 과정에 대한 세부 사항을 제공한다.

<!-- source:sections/appendix.tex:354 -->
### 일반 과학 이미지 생성을 위한 필터링 세부사항

<!-- source:sections/appendix.tex:357 -->
필터링의 두 번째 단계는 다음과 같은 차원을 기반으로 한다.

<!-- source:sections/appendix.tex:360 -->
- 이미지 타입: 이미지는 MMMU에서 정의된 30개의 이미지 유형 중 하나로 분류된다 예: {포스터, 다이어그램, 스크린샷}. 특정 이미지 유형은 주체에 따라 제거된다. 예를 들어 생물학에 대한 {미경_ 이미지} 또는 모든 주체에 대한 {표}와 같은.
<!-- source:sections/appendix.tex:362 -->
- 주체: 이미지는 특정 주체 목록에 분류되며 문학, 예술, 디자인 등과 같은 주체에 속하는 경우 제거된다. 이러한 이미지는 일반적으로 그림이나 사진과 같은 자연스러운 이미지로 간주되기 때문이다.
<!-- source:sections/appendix.tex:364 -->
- 텍스트 길이는: 이미지 들 의 모든 텍스트 를 추출 한다. 200 문자 이상 의 텍스트 를 가진 이미지 들 은 제거 된다.
<!-- source:sections/appendix.tex:366 -->
- 이미지 복잡성: 이미지들은 복잡성 1 (매우 복잡) 에서 10 (매우 간단) 까지 평가된다. 즉, 구성 요소, 객체 및 텍스트의 수와 복잡성을 고려하여 이미지가 그리기에는 너무 복잡하 여는 것이다. 우리는 중간 복잡성의 이미지를 필터링하기 위해 각 주체에 대해 다른 범위 (예: 5-7) 를 설정한다.
<!-- source:sections/appendix.tex:368 -->
- 주체 지식 밀도는: 이미지 복잡성과 비슷하게, 이미지는 모형이 주체 지식과 추론을 필요로 하는지에 따라 평가된다. 1 (최소 지식) 에서 10 (매우 밀도가 높은 지식) 까지. 각 주체에 대해서도 다른 범위가 적용됩니다 예: 7-8.
<!-- source:sections/appendix.tex:371 -->
### 화학 텍스트-이미지 데이터 합성

<!-- source:sections/appendix.tex:372 -->
기존 데이터 세트와 인터넷에서 필터링된 일반 과학 텍스트-진상 데이터 외에도 화학 이미지용 대규모 복잡한 유기 화합물 데이터를 획득하기 위해 자동화된 파이프라인을 설계했습니다. 초기 단계에서 공개적으로 액세스 할 수 있는 권위있는 화학 저장소인 PubChem에서 800,000 개의 원료 항목을 수집하기 위해 자동화된 획득 프로토콜을 사용했습니다. 이 원료 코퍼스는 독특한 화합물 ID (CID) 와 화학 명칭, 분자 공식, SMILES 표현 및 2D 구조 다이어그램을 포함한 필수 물리화학 설명체를 포함한다. 이후 우리는 잘못된 또는 불완전한 화학 자료를 제거하여 데이터 세트를 정화하기 위해 엄격한 필터링 메커니즘을 구현하여, 600,000 개의 높은-DESI 데이터 세트를 구성하여 성공적으로 생성했습니다. 두 번째 단계에서 QA와 QA의 화학적 인 구조 구조를 통합하여, QA와 QA의 특정 화학적 인 구조를 통합하여, 600,000 개의 높은 수준의 정보를 통합하여, QA와 QA의 특정 화학적 인 구조를 통합하여, QA와 QA의 특정 화학적 인 구조를 통합한다.

<!-- source:sections/appendix.tex:374 -->
### 컴퓨터 과학 편집

<!-- source:sections/appendix.tex:377 -->
각 작업의 정의는 아래와 같다.

<!-- source:sections/appendix.tex:381 -->
- 트리 토폴로지 편집 및 노드 조작: 나무에 완료 (완전한 바이너리 트리), 삽입 (특정 위치에서 새로운 노드를 삽입) 또는 절단 (특정 지역 내의 노드와 그 하목 또는 노드를 삭제) 을 수행한다.
<!-- source:sections/appendix.tex:383 -->
- 트리 트래버셜 시각화: 트래버셜 경로를 시각화하거나 사전 순서, 순서 및 순서 후를 포함한 바이너리 트리의 트래버셜 순서를 표시한다.
<!-- source:sections/appendix.tex:385 -->
- 바이너리 검색 트리 (BST) 운영: BST에 노드를 삽입하거나 BST를 검증하고 교환된 노드를 수정한다.
<!-- source:sections/appendix.tex:387 -->
- 힙 운영 및 이중 관측: 힙에 대한 삽입 또는 추출 루트 작업을 1-3 단계 수행하고 메모리 배열을 시각화하십시오. 픽업 및 픽업 프로세스를 포함해야한다.
<!-- source:sections/appendix.tex:389 -->
- 허프만 코딩 트리: 문자 주파수를 고려하면 허프만 코딩 트리를 구성하거나 노드 융합을 수행하십시오.
<!-- source:sections/appendix.tex:391 -->
- 트리 로스트 코먼 선조 (LCA) 및 경로 강조: 두 개의 노드를 주어지면 LCA를 강조하거나 그 사이의 연결 경로를 그려보십시오.
<!-- source:sections/appendix.tex:393 -->
- 그래프 $k$-hop 이웃: 중앙 노드를 주어지면 모든 노드를 정확하게 $k$의 거리로 시각적으로 표시하십시오.
<!-- source:sections/appendix.tex:395 -->
- 그래프 레벨 식별: 특정 값과 같은 수준의 모든 노드를 식별하고 박스하십시오.
<!-- source:sections/appendix.tex:397 -->
- 그래프 사이클 탐지: 그래프에서 독특한 간단한 사이클을 묘사한다.
<!-- source:sections/appendix.tex:399 -->
- 2파티트 그래프 색상: 2파티트 그래프 색상 없이 색상화 된 2파티트 그래프를 색상화하여, 그 인접 노드가 다른 색상을 가지고 있어야 한다는 제약이 있다.
<!-- source:sections/appendix.tex:401 -->
- 그래프 최단 경로: 시작 노드와 끝 노드를 주어 두 노드 사이의 가장 짧은 연결 경로를 도출하십시오.
<!-- source:sections/appendix.tex:403 -->
- 방향 그래프 접근성: 방향 그래프에서 원천 노드에서 앞으로 접근 가능한 하류 노드의 전체 집합을 박스하십시오.
<!-- source:sections/appendix.tex:406 -->
- FSM 문자열 추적: 입력 문자열을 가지고 FSM에서 완전한 상태 전환 경로를 그리십시오.
<!-- source:sections/appendix.tex:408 -->
- FSM 국가 역할 식별: FSM의 시작 상태 및 수용 상태를 식별하고 색칠한다.
<!-- source:sections/appendix.tex:410 -->
- FSM 전환 논리 완료: 미흡한 화살 가장자리와 입력 라벨을 미완성 FSM에서 완료하십시오.
<!-- source:sections/appendix.tex:417 -->
### 입체기하

<!-- source:sections/appendix.tex:420 -->
각 임무의 수행은 다음과 같습니다.

<!-- source:sections/appendix.tex:424 -->
- 혁명 고체: 우리는 먼저 3D 혁명 고체들의 가족을 GeoGebra를 사용하여 세 가지 가능한 회전축 (x, y, 또는 z) 로 매개로 구성한다. z 축을 예로 들자면, 회전축에 있는 한 가장자리가 있는 xoz 평면에서 평면 다각형을 생성한다. 구체적으로, 우리는 y 좌표를 0으로 고정하고, 단렬적으로 증가하는 정수 z 좌표를 가진 톱니의 연속을 샘플링한다. x 좌표를 엄격하게 긍정적 인 정수 (polygon lies on the positive half-axis) 또는 엄격하게 부정적 (polygon lies on the negative x half-axis) 으로 샘플링한다. 첫 번째와 마지막 톱니들은 z-axis (HPx = 0LA) 에 위치하도록 정렬되어 있으며, 각 각의 톱니의 한 축이 선택된 다각형의 주변과 일치한다는 것을 보장한다.
<!-- source:sections/appendix.tex:425 -->
- 평면 대칭: 평면 대칭은 또한 지오게브라와 함께 구현된다. 시각적으로 유쾌한 레이아웃을 유지하기 위해, 우리는 대칭 평면이 조이 평면과 상추를 이루도록 제한하고, 원형 고형이 반사하기 전에 이 평면의 한 쪽에 완전히 놓여 있는지 확인한다. 데이터 세트의 다양성을 부양하기 위해, 우리는 일반 프리즘, 일반 피라미드, 실린더, 구석 및 구석 등 여러 가지 구성 가능한 기하학적 원형을 지원한다. 프리즘 및 피라미드에서는 일반 다각형의 가장자 수가 $[3, 6]$ 범위에서 표시되며 가장자 길이는 기본 구성된다. 또한, 고형의 색과 평면의 색 모두 매개 변수화되어 있으며, 다양한 기하학적 모양과 시각적 명확성을 유지하면서 가장 큰 표본을 생성할 수 있다.
<!-- source:sections/appendix.tex:427 -->
- 포인트 시메트리: 포인트 시메트리에서는 각각 지오게브라와 매트플로틀리브를 기반으로 한 두 개의 병렬 샘플 생성 파이프라인을 구현한다. 두 파이프라인의 경우, 기하학적 원시의 종류 (예: 프리즘, 피라미드, 실린더, 코인, 구구) 및 그 색상은 무작위로 구성될 수 있으며, 다양한 인스턴스 모양을 가능하게한다. 데이터 세트의 다양성을 더 높이기 위해, 우리는 각각의 기본 솔리드에 무작위 초기 회전을 적용하고 카메라 시점 관점을 샘플들 사이에 다양하게 허용한다.
<!-- source:sections/appendix.tex:429 -->
- 솔리드 번역: 번역 작업은 3D 솔리드의 종류와 색이 완전히 구성될 수 있는 matplotlib 기반 렌더링 파이프라인을 사용하여 구현된다. 시각 효과를 미적으로 즐겁고 제어할 수 있도록, 우리는 번역 벡터를 x 축, y 축 또는 z 축을 따라 세 가지 가공적인 구성으로 제한한다. 각 샘플에 대한 번역 크기는 범위에 있는 정수로 무작위로 선택된다.
<!-- source:sections/appendix.tex:430 -->
$[4,10]$, 원본 및 번역된 고체의 상대적 위치에서 충분한 변형을 도입하면서 두 가지가 동일한 시선에서 명확하게 볼 수 있도록 보장한다.

<!-- source:sections/appendix.tex:432 -->
- 솔리드 프로젝션: 프로젝션 작업은 matplotlib에서 실행되며, 3D 솔리드의 종류와 색이 무작위로 샘플링된다. 각 솔리드는 먼저 축에 맞선 퇴행성을 피하기 위해 구성 가능한 각로 회전하고, 그 다음 오토그래픽으로 조이 평면에 프로젝된다.
<!-- source:tables/text-bench-compare.tex:3 -->
**표.** \textbf{키는 오픈소스 텍스트 생성 또는 편집 기준을 비교하는 속성이다.

<!-- source:tables/text-bench-compare.tex:1-23 -->
```text
\centering \small  {\linewidth}{l@{\extracolsep{\fill}}ccccccc} **Benchmarks** | **Type** | **Size** | **Human Filter** | **GT Ann.** | **Sub-class** | **Traditial Eval.** | **LLM Eval.**
AnyText  | Text Generation | 2,000 | {\color{red}\ding{55}} | {\color{red}\ding{55}} | - | {\color{green!60!black}\checkmark} | {\color{red}\ding{55}}
LongText  | Text Generation | 320 | {\color{green!60!black}\checkmark} | {\color{red}\ding{55}} | 8 | {\color{red}\ding{55}} | {\color{green!60!black}\checkmark}
CVTG-2K  | Text Generation | 2,000 | {\color{green!60!black}\checkmark} | {\color{red}\ding{55}} | 2 | {\color{green!60!black}\checkmark} | {\color{red}\ding{55}}
MARIO-Eval-edit  | Text Edit | 4,000 | {\color{red}\ding{55}} | {\color{red}\ding{55}} | - | {\color{green!60!black}\checkmark} | {\color{red}\ding{55}}
**TextEdit (Ours)** | Text Edit& 2,148 | {\color{green!60!black}\checkmark} | {\color{green!60!black}\checkmark} | **18** | {\color{green!60!black}\checkmark} | {\color{green!60!black}\checkmark}
```

<!-- source:tables/text-bench-classification.tex:7 -->
**표.** 데이터 통계와 통일된 기준 분류학.

<!-- source:tables/text-bench-classification.tex:1-56 -->
```text
\centering \small   **Major** | **ID** | **Category (Mid)** | **ID** | **Specific Scene (Sub)** | **Count**
\multirow{15}{*}{\rotatebox{90}{**Virtual Scenes**}} | 1.1 | Poster Scenes | 1.1.1 | Activities | Promotions Posters | 57
& | & 1.1.2 | Product | Advertising Posters | 74
& | & 1.1.3 | Movie | Art Posters | 107
\cmidrule(l){2-6} % 修改点2：横线延伸到第6列 | 1.2 | Comic Scenes | 1.2.1 | Dialogue | Narration | 65
& | & 1.2.2 | Onomatopoeia | Special-effects Text | 26
\cmidrule(l){2-6} | 1.3 | Slide / Presentation | 1.3.1 | Titles | Subtitles | 71
& | & 1.3.2 | Charts | Explanatory Text | 73
\cmidrule(l){2-6} | 1.4 | GUI Scenes | 1.4.1 | Game Interfaces | 138
& | & 1.4.2 | Browser Interfaces | 44
& | & 1.4.3 | App Interfaces (Mobile/TV) | 45
& | & 1.4.4 | Operating-System Desktops | 61
\multirow{7}{*}{\rotatebox{90}{**Real-world**}} | 2.1 | Objects Surface | - |  e.g., Packages, Bottles, Boxes, Coins | 168
& 2.2 | Signage Surface &-&e.g., Building Signs, Storefronts, Billboards | 339
& 2.3 | Board-like Media Surface&-&e.g., Blackboards, Whiteboards | 235
& 2.4 | Personal Accessories Surface &-&e.g., Clothing Prints, Badges | 192
& 2.5 | Transport Surface  |  -& e.g., Cars, Buses, Trains, Ships | 257
& 2.6 | Watermarks |  - | e.g., Photo watermarks, Brand Marks, Corner Stamps | 69
& 2.7 | Paper Media Surface&-&e.g., Papers, Books, Newspapers, Menus  | 127
**Total** |  | **2148**
```

<!-- source:tables/text-bench-evluation.tex:7 -->
**표.** **평가 매트릭의 개요.** 우리는 매트릭을 객관적 ( 텍스트 중심, 일반) 과 인식적 (MLLM 기반) 차원으로 분류한다. 상세한 공식은 §sec:metrics 섹션에서 제공된다.

<!-- source:tables/text-bench-evluation.tex:1-33 -->
```text
\centering \small **Category** | **Metric** | **What it Measures**
\multirow{8}{*}{\makecell[l]{**Classic**
& **OCR Accuracy** | Maximum similarity between the generated text in the target region and the ground-truth string.
& **OCR Precision** | Accuracy of background text preservation (penalizes hallucinated or incorrect background text).
& **OCR Recall** | Completeness of background text preservation (penalizes missing background text).
& **OCR F1-Score** | Harmonic mean of OCR Precision and OCR Recall.
& **ROI-Aware NED** | Normalized Edit Distance specifically within the source text bounding box.
\hdashline \multirow{2}{*}{\makecell[l]{**Classic**
& **CLIPScore** | Semantic alignment between the edited image and the target caption.
& **Aesthetic Score** | Visual appeal score predicted by a CLIP-based aesthetic predictor.
\multirow{5}{*}{**MLLM-based**} | **Target Accuracy** | Evaluation of spelling correctness and erasure quality of the target text.
& **Text Preservation** | Assessment of whether non-target background text remains intact.
& **Scene Integrity** | Stability of background geometry and objects (checking for distortions).
& **Local Realism** | Quality of inpainting edges, checking for artifacts like blurring or seams.
& **Visual Coherence** | Harmony of font style, lighting, and texture with the original scene.
& **MLLM Overall Avg** | Weighted average of the MLLM-based sub-scores (40/30/10/10/10).
```

<!-- source:tables/final/textedit-rule-miniset.tex:4 -->
**표.** ** 텍스트 중심의 이미지 편집의 평가 (TextEdit MiniSet-500 (Classic Metrics) 에.* ``A + B''의 통일 모델의 크기는 (``A + B'') 의 개별 이해 (A) 및 생성 (B) 매개 변수를 나타낸다. ``Real'는 실제 세계 장면에서 이미지 소스를 의미하며, `Virtual'는 합성 가상에서 이미지를 의미한다. 약자: **OA**=OCR 정확성, **OP**=OCR 정확성, **OR**=OCR 회수, **F1**=OCR F1-Score, **NED**=I-Aware NED, **CLIP****buildCLI-Score, **AES**=Aesthetic Score.

<!-- source:tables/final/textedit-rule-miniset.tex:1-50 -->
```text
\centering \multirow{2}{*}{**Models**} | \multirow{2}{*}{**# Params**} | \multicolumn{7}{c}{**Real**} | \multicolumn{7}{c}{**Virtual**}
& | **OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES** | **OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES**
\multicolumn{16}{l}{\cellcolor{gray!15}*생성 모델*}
Qwen-Image-Edit  | 20B | 0.76 | 0.69 | 0.67 | 0.67 | 0.70 | 0.75 | 5.81 | 0.74 | 0.71 | 0.70 | 0.70 | 0.70 | 0.80 | 5.27
GPT-Image-1.5  | - | 0.72 | 0.68 | 0.66 | 0.67 | 0.67 | 0.75 | 5.85 | 0.68 | 0.69 | 0.68 | 0.68 | 0.65 | 0.80 | 5.32
Nano Banana Pro  | - | 0.76 | 0.71 | 0.69 | 0.70 | 0.70 | 0.75 | 5.86 | 0.77 | 0.76 | 0.75 | 0.75 | 0.76 | 0.81 | 5.32
\multicolumn{16}{l}{\cellcolor{gray!15}*통합 모델*}
Lumina-DiMOO  | 8B | 0.20 | 0.22 | 0.18 | 0.19 | 0.19 | 0.70 | 5.58 | 0.22 | 0.25 | 0.21 | 0.22 | 0.19 | 0.73 | 4.87
Ovis-U1  | 2.4B+1.2B | 0.37 | 0.34 | 0.32 | 0.32 | 0.33 | 0.72 | 5.39 | 0.39 | 0.41 | 0.38 | 0.39 | 0.33 | 0.74 | 4.75
BAGEL  | 7B+7B | 0.61 | 0.59 | 0.52 | 0.54 | 0.54 | 0.74 | 5.79 | 0.53 | 0.58 | 0.53 | 0.55 | 0.51 | 0.78 | 5.25
InternVL-U | 2B+1.7B | 0.77 | 0.74 | 0.70 | 0.71 | 0.71 | 0.76 | 5.79 | 0.74 | 0.72 | 0.69 | 0.70 | 0.72 | 0.79 | 5.14
```

<!-- source:tables/final/textedit-mllm-miniset.tex:3 -->
**표.** ** 텍스트에 초점을 맞춘 이미지 편집의 평가 (TextEdit MiniSet-500(MLLM 기반 매트릭스).** ``A + B''의 통일 모델의 크기는 (`A + B') 매개 변수를 분리하여 이해하고 (A) 생성 (B) 를 나타낸다. ``Real'는 실제 현장에서 이미지들을 소스하는 것을 의미하며, 'Virtual'는 가상 현장에서 이미지들을 의미한다. 약자: **TA**: 텍스트 정확성, **TP**: 보존, **SI**: 장면의 무결성, **LR**: 로컬 리얼리즘, **VC**: 시각적 일관성, **MVC**: 전체 평균. **Avg: MLL.

<!-- source:tables/final/textedit-mllm-miniset.tex:1-35 -->
```text
\centering \multirow{2}{*}{**Models**} | \multirow{2}{*}{**# Params**} | \multicolumn{6}{c}{**Real**} | \multicolumn{6}{c}{**Virtual**}
& | **TA** | **TP** | **SI** | **LR** | **VC** | **Avg** | **TA** | **TP** | **SI** | **LR** | **VC** | **Avg**
\multicolumn{14}{l}{\cellcolor{gray!15}*생성 모델*}
Qwen-Image-Edit  | 20B | 0.93 | 0.85 | 0.77 | 0.55 | 0.78 | 0.80 | 0.60 | 0.82 | 0.91 | 0.81 | 0.74 | 0.76
GPT-Image-1.5  | - | 0.97 | 0.94 | 0.86 | 0.79 | 0.92 | 0.91 | 0.85 | 0.93 | 0.95 | 0.92 | 0.83 | 0.88
Nano Banana Pro  | - | 0.96 | 0.95 | 0.85 | 0.86 | 0.92 | 0.91 | 0.87 | 0.92 | 0.96 | 0.93 | 0.87 | 0.92
\multicolumn{14}{l}{\cellcolor{gray!15}*통합 모델*}
Lumina-DiMOO  | 8B | 0.16 | 0.04 | 0.04 | 0.02 | 0.06 | 0.08 | 0.02 | 0.05 | 0.19 | 0.07 | 0.03 | 0.10
Ovis-U1  | 2.4B+1.2B | 0.29 | 0.11 | 0.11 | 0.08 | 0.20 | 0.17 | 0.04 | 0.16 | 0.35 | 0.18 | 0.15 | 0.22
BAGEL  | 7B+7B | 0.68 | 0.61 | 0.38 | 0.34 | 0.59 | 0.53 | 0.36 | 0.52 | 0.69 | 0.64 | 0.40 | 0.54
InternVL-U | 2B+1.7B | 0.94 | 0.91 | 0.72 | 0.73 | 0.75 | 0.89 | 0.88 | 0.87 | 0.90 | 0.78 | 0.57 | 0.79
```
