# 초록

<!-- src: sections/0.abstract.tex:L2-L2 -->
이해, 추론, 생성, 편집을 통합하는 unified multimodal model(UMM)은 강력한 의미 이해 능력을 유지하는 것과 강력한 생성 능력을 획득하는 것 사이에서 본질적인 trade-off에 직면한다.

<!-- src: sections/0.abstract.tex:L3-L3 -->
본 보고서에서는 이러한 능력을 하나의 통합 프레임워크 안에서 대중화하는 경량 4B-parameter UMM인 InternVL-U를 제시한다.

<!-- src: sections/0.abstract.tex:L4-L4 -->
unified contextual modeling, modality-specific modular design, decoupled visual representation이라는 원칙에 따라 InternVL-U는 최신 Multimodal Large Language Model(MLLM)에 특화된 MMDiT 기반 visual generation head를 통합한다.

<!-- src: sections/0.abstract.tex:L5-L5 -->
미적 생성과 고수준 지능 사이의 간극을 더욱 좁히기 위해, text rendering과 scientific reasoning처럼 semantic density가 높은 과제를 겨냥한 포괄적인 데이터 합성 pipeline을 구축한다. 이 pipeline은 Chain-of-Thought(CoT)를 활용해 추상적인 사용자 의도와 세밀한 시각 생성 세부 사항을 더 잘 정렬하는 reasoning-centric 패러다임을 따른다.

<!-- src: sections/0.abstract.tex:L6-L6 -->
광범위한 실험은 InternVL-U가 성능과 효율성 사이에서 우수한 균형을 달성함을 보여준다. 단 4B parameters만 사용하면서도 여러 생성 및 편집 과제에서 BAGEL(14B)처럼 규모가 3× 이상 큰 unified baseline model을 일관되게 능가하며, 동시에 강력한 multimodal understanding 및 reasoning 능력을 유지한다.

# 1. 서론

<!-- figure: fig:teaser; src: sections/1.introduction.tex:L2-L9 -->
**그림 1. 일반 text-to-image 생성(위)과 image editing(아래)에 대한 InternVL-U의 사례.** InternVL-U는 어떤 해상도에서도 high-fidelity image generation 및 editing을 지원한다.

<figure data-figure="1"><img src="source/figures/teasers/overview_page1.pdf" alt="그림 1"></figure>

<!-- figure: fig:teaser2; src: sections/1.introduction.tex:L11-L18 -->
**그림 2. 공간 중심, 지각, 과학 중심, 유머 중심, 추론 중심 text-to-image 생성 또는 editing 과제에 대한 InternVL-U의 사례.** InternVL-U는 다양한 시각 도메인에 걸쳐 이러한 핵심 multimodal 능력을 보여준다.

<figure data-figure="2"><img src="source/figures/teasers/overview_page2.pdf" alt="그림 2"></figure>

<!-- src: sections/1.introduction.tex:L45-L47 -->
Unified multimodal model(UMM)은 최근 몇 년 동안 빠르게 발전해 왔다 [team2024chameleon; chen2025blip3; li2025onecat; tian2025unigen; tang2025unilip]. GPT-4o [hurst2024gpt] 같은 모델의 등장은 native image generation과 고도화된 언어 능력의 통합이 사용자가 자연어로 복잡한 시각 과제를 수행하도록 할 뿐 아니라 Artificial General Intelligence(AGI)와 World Model을 탐구하는 길도 연다는 점을 보여준다 [deng2025bagel; cui2025emu3]. 폐쇄형 모델이 뛰어난 범용 성능을 보이는 동안, 연구 커뮤니티는 이러한 unified model을 구축하기 위해 다양한 architecture 및 representation 전략을 활발히 탐구해 왔다. 이러한 노력은 대체로 두 패러다임으로 나뉜다. (1) **Fully-native UMM** [team2024chameleon; cui2025emu3; deng2025bagel; wang2025ovis; xin2025lumina; xie2025show]은 처음부터 학습하거나 unimodal component(예: ViT, LLM)로 초기화한 뒤 multimodal understanding 및 generation 과제를 처음부터 공동 학습한다. (2) **Fully-ensemble UMM** [pan2025transfer; lin2025uniworld; song2025query; wu2025openuni]은 사전 학습된 multimodal understanding model과 사전 학습된 image generation model을 사후 정렬하여 unified system을 구축한다. 그러나 두 패러다임 모두 상당한 한계가 있다.

<!-- src: sections/1.introduction.tex:L49-L50 -->
Fully-native UMM의 경우 modeling, representation, architecture 전반에서 최적 설계가 무엇인지 아직 커뮤니티의 합의가 이루어지지 않았다 [he2025emmaefficientmultimodalunderstanding]. 이론적 견해 차이가 존재할 뿐 아니라 어떤 단일 접근법도 성능이나 효율성에서 결정적인 우위를 보여주지 못했다 [li2025onecat]. 더욱이 multimodal understanding 및 generation 능력을 처음부터 공동 학습하는 일은 특히 서로 다른 modality의 상충하는 데이터 분포를 균형 있게 맞춰야 한다는 점에서 상당한 engineering 난제를 야기한다. 무엇보다 이 패러다임은 커뮤니티에서 이미 이용할 수 있는 최신(SOTA) multimodal understanding model [Qwen-VL; chen2024internvl]의 이점을 포기해야 하는 경우가 많아, 감당하기 어려운 학습 비용과 위험을 초래한다. 반대로 fully-ensemble UMM은 일반적으로 외부에서 별도로 사전 학습된 image generator를 visual generation head로 부착한다 [xie2024sana; flux2024; rombach2022high]. 실제로 이들은 반복적인 trade-off에 직면한다. Qwen-Image [wu2025qwen]와 Hunyuan Image 3.0 [cao2025hunyuanimage]처럼 head의 parameter 수를 매우 크게 확장하여 최상급 시각 품질을 달성할 수 있지만, 이는 학습 및 배포 비용을 크게 높인다. 다른 선택으로는 작은 head를 유지하면서 Stable Diffusion 3 [mmdit]의 multi-encoder text conditioning이나 Z-Image [cai2025z]의 text condition과 image condition을 분리하는 설계처럼 정교하지만 흔히 파편화된 conditioning pipeline을 도입할 수 있다. 어느 쪽이든 결과적인 interface를 단일 MLLM의 hidden-state 공간에 깔끔하게 정렬하기 어려우며, 이는 제한된 자원 아래 post-alignment training으로 얻을 수 있는 이득을 제약한다.

<!-- src: sections/1.introduction.tex:L52-L52 -->
이러한 난제를 해결하기 위해 먼저 modeling, architecture, representation이라는 세 차원에서 unified model의 설계 원칙을 체계적으로 분석한다. 통합된 semantic reasoning 공간 안에서 모델은 서로 다른 modality의 통계적 특성에 대응하기 위해 hybrid modeling objective를 사용하고, 전체 architecture 효율성을 높이기 위해 modality-specific modularity를 따르며, 고수준 semantic understanding과 저수준 pixel reconstruction 사이의 균형을 위해 decoupled visual representation을 사용해야 한다고 본다. 이 원칙에 따라 간결하고 효율적인 unified multimodal model인 InternVL-U를 제안한다. SoTA 성능의 open-source MLLM인 InternVL 3.5 [wang2025internvl3_5]를 기반으로, MLLM hidden state와 정렬되는 unified semantic conditioning interface를 갖춘 custom MMDiT 기반 visual generation head를 통합한다. 3단계 progressive training 전략을 통해 InternVL-U는 전신 모델의 견고한 understanding 및 reasoning 능력을 물려받을 뿐 아니라 강력한 multimodal generation 및 editing 능력도 습득한다. 또한 InternVL-U는 self-reflection reasoning을 활용해 MLLM에서 물려받은 world knowledge를 이용함으로써 이러한 능력을 더욱 향상한다.

<!-- src: sections/1.introduction.tex:L54-L54 -->
그러나 설계의 통합만으로는 진정한 AGI 지향 UMM이 보장되지 않는다. 모델이 궁극적으로 획득하는 능력은 학습에 사용된 objective와 data regime의 영향을 강하게 받기 때문이다 [rombach2022high; wang2025internvl3_5]. Unified multimodal model에는 시각적 능력과 의미적 신뢰성이 모두 기대되지만, 오늘날의 visual generation model과 multimodal understanding model은 근본적으로 다른 목표와 사용 사례에 최적화되어 있다. 전통적인 generation model은 주로 미학과 visual fidelity 같은 *저수준* 지각 품질을 겨냥하는 반면, understanding model은 knowledge injection과 reasoning emergence를 포함한 *고수준* 지능을 강조한다. 이러한 objective 불일치는 AGI 지향 UMM 개발의 주요 장애물이다. 그 핵심 원인은 학습 데이터 분포의 domain gap이라고 주장한다. Generation model은 texture와 high-frequency detail은 풍부하지만 semantic density는 비교적 낮은 자연 이미지 corpus(예: 인물 및 풍경)를 주로 학습한다. 대조적으로 understanding model은 GUI, infographic, OCR 중심 문서 같은 합성 이미지를 포함하여 text가 풍부하고 구조적으로 조직된 데이터에 크게 의존한다. 이러한 데이터는 texture는 단순할 수 있지만 조밀한 의미, 풍부한 textual cue, 구조화된 지식을 담고 있다.

<!-- src: sections/1.introduction.tex:L56-L58 -->
이 진단과 일치하게 차세대 상용 모델(예: Nano-Banana Pro [deepmind_gemini3proimage_2025])은 미학만을 추구하는 데서 벗어나 typography의 정밀성과 지식에 충실한 콘텐츠 생성을 강조함으로써 이 간극을 적극적으로 좁히기 시작했다. 이러한 흐름에서 영감을 받고 InternVL-U의 AGI 지향 UMM으로서의 잠재력을 끌어내기 위해 text rendering, scientific reasoning, 공간 및 유머 생성 등 다양한 능력을 겨냥하는 포괄적인 multimodal 데이터 합성 pipeline을 구축한다. 구체적으로 “high semantic density” text 시나리오에는 bilingual typography와 local consistency editing을 포괄하는 완전 자동 text rendering 및 editing pipeline을 설계하여 generative model의 symbolic precision 부족을 해결한다. “knowledge-intensive” 과학 시나리오에는 programmatic tool(예: GeoGebra, SVG)과 academic corpus를 활용하여 수학, 물리학, 컴퓨터 과학 등 여러 분야에 걸친 구조화된 visual-text 데이터를 구축한다. 또한 사용자 의도가 지닌 추상적이고 불충분하게 명시된 성격을 더 잘 포착하기 위해 “Reasoning-centric” 데이터 합성 패러다임을 제안한다. 명시적 Chain-of-Thought(CoT)를 도입하여 모호한 instruction을 planning과 constraint가 담긴 실행 가능한 단계로 변환하고, meme generation, geometric transformation, logically constrained editing 같은 과제에서 단순한 instruction following을 넘어 깊은 intent alignment로 도약한다. 이러한 pipeline의 데이터를 통합함으로써 InternVL-U는 강력한 범용 생성 능력을 유지하면서도 정확한 text rendering 및 editing, spatial reasoning, humor generation, multidisciplinary scientific knowledge 생성 능력을 크게 향상한다.

<!-- src: sections/1.introduction.tex:L60-L60 -->
광범위한 실증 평가는 InternVL-U가 성능과 효율성 사이에서 우수한 균형을 달성함을 보여준다. 5절에서 논의하듯 text-to-image 생성에서 기존 unified model을 일반, text-centric, knowledge-intensive benchmark 전반에 걸쳐 일관되게 능가하며, 훨씬 큰 specialized generation model의 능력에 근접한다. 특히 뛰어난 instruction following을 보이며, 이전 unified architecture가 읽을 수 있는 text rendering에 취약했던 문제를 효과적으로 해결한다. 핵심적으로 CoT 전략의 통합은 generation과 editing 모두에 중요한 촉매로 작용하여, 지식이 풍부한 generation 및 복잡한 논리에 의존하는 editing 과제에서 모델이 탁월한 성능을 발휘하고 괄목할 성능 향상을 내도록 한다. 또한 multimodal understanding 측면에서 InternVL-U는 전신 모델의 견고한 능력을 유지하며 native vision-language comprehension을 훼손하지 않고 비교 가능한 unified baseline을 능가한다. 커뮤니티의 효율적인 benchmarking을 지원하기 위해 UMM 평가를 간소화하는 *GenEditEvalKit* [umm_evalkit_github]와 더욱 포괄적인 text-editing benchmark를 제공하는 *TextEdit Benchmark* [textedit_github]도 소개한다.

<!-- src: sections/1.introduction.tex:L62-L70 -->
요약하면 기여는 다음 세 가지다.

1. InternVL-U는 Unified Contextual Modeling, Decoupled Visual Representations, Modality-Specific Modularity를 토대로 구축한 효율적인 UMM이다. Decoupled ViT 및 VAE representation과 맞춤형 MMDiT 기반 generation head를 통합한 architecture는 semantic understanding과 pixel reconstruction 사이의 충돌을 해결하여 native understanding 능력을 훼손하지 않으면서 강력한 generative skill을 가능하게 한다.
2. Text rendering, scientific reasoning, spatial manipulation, humor generation 등 high-semantic-density 과제를 겨냥하는 포괄적인 데이터 pipeline을 구축한다. 또한 Chain-of-Thought를 활용해 추상적인 사용자 instruction을 실행 가능한 plan으로 바꾸는 “Reasoning-centric” 패러다임을 도입하여, 모호한 의도와 정밀한 시각적 실행 사이의 간극을 효과적으로 좁힌다.
3. 광범위한 평가는 InternVL-U가 generation과 editing, 특히 text-rich 및 knowledge-intensive 시나리오에서 unified baseline을 일관되게 능가함을 보여준다. 핵심적으로 vision-language comprehension을 훼손하지 않으면서 견고한 multimodal understanding 능력을 유지하고 비교 가능한 unified model을 능가한다.

# 2. 관련 연구

## 2.1 Multimodal Large Language Model

<!-- src: sections/2.related.tex:L3-L6 -->
최근 Multimodal Large Language Model(MLLM)의 발전은 vision-language 과제에 혁신을 일으켰다. LLaVA [liu2023llava; liu2023improvedllava; liu2024llavanext], Qwen-VL [Qwen-VL; Qwen2-VL; Qwen2.5-VL; Qwen3-VL], InternVL [chen2024internvl; chen2024expanding; chen2024far; zhu2025internvl3; luo2024mono_internvl; mono_internvl_v1.5; wang2025internvl3_5] 같은 대표적인 open-source 계열과 GPT [achiam2023gpt; GPT-5], Gemini [team2024gemini; comanici2025gemini; gemini25; Gemini-3-Flash] 같은 proprietary model은 visual understanding에서 뛰어난 능력을 입증했다. 표준 MLLM은 일반적으로 adapter [li2022blip; liu2023improvedllava]를 통해 vision encoder [dosovitskiy2020image]와 LLM [touvron2023llama; yang2025qwen3; anil2023palm]을 연결하는 unified architecture를 채택한다. 또한 최근 흐름은 interleaved image-text sequence 처리 [cui2025emu35nativemultimodalmodels; deng2025bagel; tian2024mminterleaved; yang2024vision]와 video understanding [2023videochat; Maaz2023VideoChatGPT; lin2023video; wang2025internvideo2; yang2025cambrian; yang2025kwai]으로 확장되어 long-context multimodal interaction의 경계를 넓히고 있다.

## 2.2 Visual Generative Model

<!-- src: sections/2.related.tex:L8-L12 -->
Visual generation은 초기 GAN [isola2017image; karras2019style; goodfellow2020generative]에서 우수한 scalability와 sample quality를 제공하는 주류 diffusion 기반 프레임워크 [ho2020denoising; rombach2022high; flux2024] 및 flow matching 패러다임 [lipman2024flowmatchingguidecode; liu2022flow]으로 발전했다. 이와 병행하여 discrete token 기반 접근법 [tian2024visual; esser2021taming; ramesh2021zero; chang2022maskgit]은 VQ 계열 codec을 통해 이미지를 autoregressive 방식으로 생성하여 LLM과 통합된 token 공간을 가능하게 한다. Stable Diffusion 3.5 [rombach2022high], FLUX.2 [flux-2-2025], Hunyuan Image 3.0 [cao2025hunyuanimage], Qwen-Image [wu2025qwen]를 비롯한 최신 text-to-image model은 instruction following과 복잡한 scene generation을 강조한다. 한편 커뮤니티는 복잡한 구조와 text의 rendering, 그리고 긴 prompt 및 multi-concept description에 대한 generalization을 개선하기 위해 data-centric 및 architecture-centric 접근법을 탐구해 왔다 [wu2025qwen; wang2025ovis_image; team2025longcat; cai2025z]. 아울러 Nano Banana Pro [deepmind_gemini3proimage_2025], GPT-Image-1.5 [GPT-Image-1.5], Seedream 4.0 [seedream2025seedream] 같은 여러 폐쇄형 최신 시스템도 instruction-following과 복잡한 multi-concept image generation 과제에서 강력한 성능을 보여주었다. 이 밖에 instruction-driven editing [brooks2023instructpix2pix; labs2025flux1kontextflowmatching; liu2025step1x-edit]도 주목받고 있으며, 이 과제는 semantic consistency를 보존하면서 특정 영역을 조작할 것을 모델에 요구한다.

## 2.3 Unified Multimodal Model

<!-- src: sections/2.related.tex:L14-L20 -->
Unified Multimodal Model(UMM)은 하나의 파운데이션 모델 안에 understanding, generation, editing을 통합하는 것을 목표로 한다. 강력한 LLM을 visual tokenizer 또는 latent representation과 결합함으로써 UMM은 시각 콘텐츠를 통합된 방식으로 이해하고 생성할 수 있다. 기존 접근법은 일반적으로 두 범주로 나뉜다. (1) Chameleon [team2024chameleon], Emu3 [cui2025emu3], SynerGen-VL [li2025synergen] 같은 **Auto-Regressive Discrete-token 방식**은 image generation을 next-token prediction으로 취급하여 modality를 자연스럽게 통합하지만 visual fidelity에서 어려움을 겪는 경우가 많다. (2) BLIP-3o [chen2025blip3o], BAGEL [deng2025bagel], Ovis-U1 [wang2025ovis] 및 기타 모델 [li2025onecat; tian2025unigen; shen2025mammothmoda2; liu2025tuna; wang2025skywork; li2025uniworld; he2025emmaefficientmultimodalunderstanding] 같은 **Diffusion/Hybrid 방식**은 LLM의 reasoning power와 diffusion 또는 flow matching model의 high-fidelity generation을 결합한다. 최근 연구는 이 밖에도 서로 다른 unified 패러다임 [modelmanzano; tang2025unilip; li2025lavida; yang2025mmada; xin2025lumina]을 탐구한다. 이러한 연구 흐름에 따라 본 연구의 InternVL-U는 open-source MLLM, 즉 InternVL3.5 [wang2025internvl3_5]를 기반으로 하며, 하나의 프레임워크 안에서 범용 understanding, generation, editing뿐 아니라 domain-specific 시나리오(예: text rendering, science, meme)를 위한 능력도 통합한다.

# 3. 방법: InternVL-U

<!-- figure: fig:overall_arch; src: sections/3.methodology.tex:L3-L10 -->
**그림 3. InternVL-U의 architecture 설계.** 프레임워크는 세 가지 설계 원칙을 강조한다. (1) modality-adaptive generation target을 지원하는 unified contextual modeling, (2) unified backbone과 modality-specific modular design을 통한 structural efficiency, (3) understanding 및 generation 과제를 위한 decoupled visual representation이다. Und.와 Gen.은 각각 Understanding과 Generation을 뜻한다.

<figure data-figure="3"><img src="source/figures/method/method-1.pdf" alt="그림 3"></figure>

## 3.1 모델 Architecture

<!-- src: sections/3.methodology.tex:L12-L14 -->
이 절에서는 InternVL-U의 전체 architecture 설계 원칙과 visual generation head의 상세 architecture를 설명한다.

### 3.1.1 전체 설계 원칙

<!-- src: sections/3.methodology.tex:L16-L20 -->
그림 3에서 보듯 모든 modality에 동질화된 processing pipeline을 강제하는 최근 접근법 [liang2024mixture]과 달리, 본 architecture는 서로 다른 modality에 맞춘 처리가 효율성과 성능을 극대화하는 데 필요하다는 철학을 따른다. 설계 원칙은 modeling paradigm, structural efficiency, data representation이라는 세 핵심 차원으로 정리한다.

#### Modality-Adaptive Generation을 적용한 Unified Contextual Modeling

<!-- src: sections/3.methodology.tex:L22-L30 -->
첫 번째 원칙은 multimodal understanding(context)과 generation(prediction) 사이의 이분법을 다룬다. Contextualization에는 깊은 semantic fusion을 촉진하는 unified representation이 유리하지만, generation은 각 modality에 내재한 통계적 특성을 존중해야 한다고 주장한다.

- **Unified Context, Adaptive Target:** context 단계에서는 visual token과 linguistic token을 모두 공유 latent space에 projection하고 causal masking을 적용한 unified autoregressive(AR) 패러다임을 사용한다. 이는 reasoning 과정에서 modality 간 복잡한 고수준 semantic dependency를 모델이 포착하도록 보장한다.
- **Hybrid Generative Objective:** 그러나 prediction target에는 “모든 것을 tokenization”하는 접근법 [cui2025emu3]에서 벗어난다. 본질적으로 discrete하고 sequential한 text는 cross-entropy loss를 사용하여 유한 vocabulary에 대한 categorical distribution으로 modeling하는 것이 가장 적합하다. 반면 visual signal은 continuous하고 공간적으로 상관되어 있다. Discrete visual tokenization도 실행 가능한 대안이지만(VQ-VAE 기반 AR model의 경우처럼), quantization bottleneck을 유발하고 세밀한 spatial modeling을 덜 직접적으로 만들 수 있다. 따라서 hybrid AR + Diffusion modeling 패러다임을 채택한다. Image generation은 diffusion을 일반화한 formulation인 Flow Matching을 사용하여 continuous multivariate probability space에서 modeling하고, text에는 AR objective를 유지한다. 이 설계는 text에 대한 autoregressive language modeling의 강점을 보존하면서 image에는 diffusion 기반 방식의 high-fidelity generation 능력을 활용하도록 한다.

#### Modality-Specific Modular Design을 통한 Structural Efficiency

<!-- src: sections/3.methodology.tex:L36-L44 -->
두 번째 원칙은 모든 modality를 동일한 token sequence로 취급하는 완전히 modality-agnostic한 architecture(예: Mixture-of-Transformer(MoT) [liang2024mixture])의 계산 비효율을 다룬다. 서로 다른 modality는 상이한 “semantic density”를 지니며, text는 의미적으로 조밀하지만 raw visual patch는 희소하고 중복적이라고 주장한다.

- **Encoder-Based MLLM Initialization:** generic transformer로 raw modality를 처리할 때 본질적으로 발생하는 parameter 및 FLOPs 낭비를 줄이기 위해 modality-specific encoding stem을 통합한다. 더 monolithic하거나 native multimodal design [luo2025mono; tian2025navil] 대신 사전 학습된 ViT [chen2024internvl]를 활용하는 encoder 기반 architecture로 multimodal context modeling backbone을 초기화한다. 이 설계는 visual information이 unified latent space에 들어가기 전에 이를 효율적으로 집계하는 데 필요한 inductive bias를 도입한다.
- **Modality-Specific Generation Head:** 또한 text와 image의 decoding 요구가 다름을 고려하여, 사전 학습된 MLLM에 image generation을 위한 Multimodal Diffusion Transformer(MMDiT) [mmdit] architecture 기반의 전용 generation head를 확장한다. Context modeling backbone에 pixel-level synthesis 부담을 지우는 대신, MMDiT가 unified hidden state를 conditioning signal로 받아 continuous visual latent space에서 image를 합성하는 전용 generative module 역할을 한다. 이 hierarchical design은 backbone이 semantic reasoning에 집중하고 특화된 stem과 head가 modality-specific translation을 처리하도록 하여, 더 통합적이면서도 계산 효율적인 UMM을 만든다.

#### Understanding과 Generation을 위한 Decoupled Visual Representation

<!-- src: sections/3.methodology.tex:L47-L56 -->
세 번째 원칙은 image를 이해하는 데 쓰는 visual representation이 image 생성에 쓰는 것과 같아야 한다는 가정에 이의를 제기한다. Image understanding은 주로 의미적으로 유용한 feature에 의존하지만 image generation은 이에 더해 복원 가능한 저수준 시각 세부 사항을 보존하는 representation을 필요로 한다는 관찰에서 비대칭 representation 전략을 제안한다. 이는 사람이 반드시 그릴 수 있는 것은 아닌 복잡한 scene도 지각할 수 있는 것과 유사하다.

- **Context Understanding을 위한 Semantic Input:** understanding 과제(context)에는 사전 학습된 ViT가 raw pixel에서 직접 추출한 고수준 semantic feature만 사용한다. 이는 복잡한 reasoning에 필요한 semantic fidelity를 보존하는 데 도움이 된다.
- **Generation Target을 위한 Compressed Output:** generation 과제(target)에는 image reconstruction을 위해 별도로 학습된 Variational Autoencoder(VAE)를 사용한다. 이 VAE는 image를 synthesis에 적합한 latent space로 압축한다.

이러한 representation의 decoupling은 단일 encoder가 understanding에 필요한 고수준 abstraction과 generation에 필요한 저수준 pixel detail 사이에서 균형을 맞추느라 고전하는 “optimization trade-off”를 피할 뿐 아니라, generation target을 context backbone에 입력할 때 발생하는 계산 비용 증가 및 infrastructure 복잡성도 피한다. 이를 통해 generative quality를 훼손하지 않으면서 understanding에 이용 가능한 가장 강력한 사전 학습 encoder를 활용할 수 있다.

<!-- figure: fig:overall_arch_head; src: sections/3.methodology.tex:L58-L64 -->
**그림 4. Visual Generation Head의 Architecture.** (a) dual-stream MMDiT block을 갖춘 head의 개요. (b) Dual-Stream Attention Block과 Dual-Stream FFN Block의 상세 구조. (c) VAE image latent와 multimodal context embedding에 적용한 Unified MSRoPE(Multi-Scale Rotary Positional Embeddings)의 도해.

<figure data-figure="4"><img src="source/figures/method/method-2.pdf" alt="그림 4"></figure>

### 3.1.2 Visual Generation Head

<!-- src: sections/3.methodology.tex:L66-L68 -->
제안한 원칙을 바탕으로 이 절에서는 그림 4에 나타낸 custom-developed visual generation head의 구현을 더 자세히 설명한다.

#### Context 및 Target Input을 위한 Dual Projector

<!-- src: sections/3.methodology.tex:L70-L70 -->
Multimodal hidden state(*context*)와 VAE image latent(*target*)의 feature distribution은 서로 크게 다르다. 이러한 이질성을 연결하기 위해 독립적인 linear projector를 사용하여 둘을 visual generation module의 conditioning space로 mapping한다. 특히 multimodal context embedding은 VAE latent보다 magnitude가 더 크고 outlier가 더 두드러지는 경향이 있음을 관찰한다. 이러한 scale mismatch를 줄이고 학습 안정성을 개선하기 위해 projection 전 VLM branch에 normalization layer를 추가하여 context feature의 variance를 명시적으로 1로 정규화한다.

#### Gated Attention을 적용한 Dual-Stream MMDiT Block

<!-- src: sections/3.methodology.tex:L72-L78 -->
Multimodal context와 generative target의 서로 다른 통계적 특성을 고려하기 위해 완전한 Dual-Stream architecture를 채택한다. 두 stream은 token-level dependency를 포착하기 위해 joint self-attention으로 상호작용하지만 QKVO projection과 Feed-Forward Network(FFN)에는 분리된 parameter를 사용한다. 또한 high-resolution, long-context 시나리오에서 non-linearity를 높이고 “attention-sink” 현상을 완화하기 위해 element-wise Gating Mechanism [qiu2025gated]을 attention block에 통합한다. 형식적으로 attention layer의 modulated output **O′**는 다음과 같다.

<pre class="equation">O′ = O ⊙ σ(XW_g)</pre>

여기서 σ는 sigmoid function을 뜻하고, **X**와 **O**는 각각 attention layer의 input과 output이며, **W_g**는 학습 가능한 gating projection matrix를 뜻한다. 이 matrix 역시 각 stream에 대해 분리된다. 아는 한 이는 MMDiT architecture 안에 gating mechanism을 통합한 최초의 사례이며, 최소한의 parameter overhead로 향상된 expressivity를 제공한다.

#### Resolution Interpolation을 적용한 Unified MSRoPE

<!-- src: sections/3.methodology.tex:L80-L84 -->
공간 구조를 엄밀하게 보존하기 위해 positional information을 encoding하는 Multimodal Scalable RoPE(MSRoPE) [wu2025qwenimagetechnicalreport]를 사용한다.

- **Unified 3D Encoding:** multimodal context의 visual token을 flattened 1D sequence로 취급하는 경우가 많은 이전 연구 [wu2025qwenimagetechnicalreport]와 달리, generative target과 context 내 visual token 모두에 unified 3D positional embedding(temporal, height, width)을 적용한다. 이러한 정렬은 image editing처럼 정밀한 spatial reasoning이 필요한 과제에 상당한 이점을 준다.
- **Positional Interpolation:** resolution scaling을 지원하기 위해 high-resolution fine-tuning 중 position index를 직접 extrapolation할 때 관찰되는 “tiling artifact”를 다룬다. 대신 Resolution Interpolation 전략을 채택한다. 최대 target resolution(예: 1024px)을 기준으로 position embedding 범위를 정의한다. 초기 low-resolution pre-training(예: 512px) 중에는 더 작은 index 범위를 쓰는 대신 전체 범위를 사용하되 인접 token 사이의 stride를 늘린다. 이는 모델이 처음부터 일관된 global spatial representation을 학습하도록 보장하고, 더 높은 resolution으로 scale을 확장할 때 domain gap을 최소화한다.

## 3.2 학습 전략

### 3.2.1 학습 Objective

<!-- src: sections/3.methodology.tex:L87-L91 -->
UMM에 multimodal content를 처리하고 생성하는 능력을 부여하기 위해 joint optimization objective를 formulation한다. Multimodal context sequence **c**가 주어지면 모델은 discrete text token **x**와 continuous image latent representation **z**를 동시에 예측하도록 학습된다.

#### Autoregressive Text Generation

<!-- src: sections/3.methodology.tex:L93-L98 -->
Text 구성 요소에서는 text generation을 discrete vocabulary에 대한 sequence modeling 문제로 취급한다. 표준 Next-Token Prediction(NTP) objective를 사용하여 context와 preceding token을 조건으로 하는 target token의 negative log-likelihood를 최소화한다.

<pre class="equation">L_NTP = −(1/T) Σ_(t=1)^T log p_θ(x_t | x_&lt;t, c)</pre>

여기서 x_t는 길이 T인 text sequence의 t번째 token이고, x_<t는 preceding token이며, θ는 unified model을 parameterize한다. 이 objective는 MLLM backbone에 내재한 reasoning 및 instruction-following 능력을 모델이 유지하도록 보장한다.

#### Image Generation을 위한 Flow Matching

<!-- src: sections/3.methodology.tex:L100-L108 -->
Visual 구성 요소에는 image latent의 continuous distribution을 modeling하기 위해 velocity parameterization을 사용하는 Flow Matching 프레임워크를 채택한다. Noise ε을 예측하는 diffusion model과 달리, Gaussian noise distribution에서 data distribution으로 probability density를 운반하는 velocity vector field v_θ를 regression한다. Flow Matching에서 흔히 사용하는 formulation과 Optimal Transport에서 영감을 받은 transport path를 따라, noise **z₀ ∼ N(0, I)**와 ground-truth image latent **z₁** 사이의 표준 linear interpolation path를 가정한다. 시간 **t ∈ [0, 1]**에서 intermediate state는 **z_t = tz₁ + (1−t)z₀**로 정의한다. Objective는 predicted velocity와 target drift 사이의 mean squared error를 최소화하는 것이다.

<pre class="equation">L_FM = E_(t ∼ U[0,1], z₀ ∼ N(0,I), z₁ ∼ p_data) [ ‖v_θ(z_t, t, c) − (z₁ − z₀)‖² ]</pre>

여기서 **v_θ(z_t, t, c)**는 context **c**를 조건으로 시간 **t**의 velocity vector를 예측하는 model output이고, **(z₁ − z₀)**는 linear trajectory를 따르는 ground-truth instantaneous velocity를 나타낸다.

#### Unified Training Objective

<!-- src: sections/3.methodology.tex:L110-L116 -->
최종 training objective는 discrete loss와 continuous loss의 weighted sum이다.

<pre class="equation">L_Total = α · L_NTP + β · L_FM</pre>

여기서 **α**와 **β**는 두 modality 사이의 균형을 맞추는 scalar hyperparameter다. 실제로는 visual fidelity나 reasoning 능력 같은 특정 능력을 우선하기 위해 서로 다른 학습 stage(예: pre-training 대 supervised fine-tuning)에 걸쳐 이 coefficient를 동적으로 조정한다.

### 3.2.2 학습 Pipeline

<!-- src: sections/3.methodology.tex:L118-L120 -->
3.1.1절에서 설명한 architecture 원칙을 따르면서 학습 효율성을 극대화하기 위해, understanding 과제에만 최적화된 사전 학습 MLLM으로 UMM을 초기화한다. Base MLLM에는 visual generative 능력이 없으므로, visual synthesis skill을 점진적으로 해제한 뒤 semantic reasoning과 통합하는 3단계 curriculum을 설계한다.

#### Stage 1: Generation Head Pre-training

<!-- src: sections/3.methodology.tex:L122-L124 -->
초기 단계에서는 새로 초기화한 visual generation head를 MLLM latent space에 grounding하는 데 집중한다. Semantic representation을 보존하기 위해 MLLM을 freeze하고 generation head와 projector만 학습한다. 이전 연구 [xie2024sana]를 따라 256px pre-training을 생략하고 고정 resolution 512px을 사용하여 초기 convergence를 가속한다. 초기화에 text-to-image data만 사용하는 이전 접근법 [wang2025ovis; wu2025qwenimagetechnicalreport]과 달리, 시작부터 text-to-image generation 및 image editing dataset의 mixture를 포함한다. 이 multi-task 전략은 generation head가 text instruction과 visual context token 모두에 동시에 attention하도록 강제하여 multimodal condition alignment를 위한 견고한 기반을 마련한다.

#### Stage 2: Any-resolution Continued Pre-training

<!-- src: sections/3.methodology.tex:L126-L130 -->
안정적인 초기화를 기반으로 다양한 aspect ratio를 처리하고 visual fidelity를 높이기 위해 variable-resolution training으로 진행한다. MLLM backbone은 freeze된 상태를 유지한다. Training corpus를 2차로 filtering하여 aesthetic quality가 높은 sample만 남기고, 학습 불안정을 유발할 수 있는 극단적 aspect ratio의 sample은 버린다. 생성 image의 resolution은 512~1024 pixels 범위로 제어하고, aspect ratio는 0.5~2.0 범위로 유지한다. Image editing 과제에서는 input condition과 output 사이의 pixel-level alignment 유지가 매우 중요하다. 이를 위해 condition image의 VAE latent를 visual generation head에 추가로 명시적으로 주입하여 더 나은 pixel-level consistency를 달성한다.

#### Stage 3: Unified Supervised Finetuning

<!-- src: sections/3.methodology.tex:L132-L135 -->
마지막 단계의 목표는 이전 단계에서 획득한 visual generative 능력과 사전 학습 MLLM의 reasoning 능력 사이에 더 큰 synergy를 만드는 것이다. 따라서 end-to-end optimization이 가능하도록 MLLM backbone을 포함한 전체 모델을 unfreeze한다. Training corpus는 더 엄격한 기준으로 추가 filtering하며, 4절에서 자세히 설명하는 CoT reasoning data도 추가한다. 이러한 CoT data를 image generation 및 editing data와 혼합함으로써 모델은 visual domain에서 실행하기 전에 textual reasoning을 통해 generation을 planning할 수 있다.


<!-- source: sections/4.data.tex:1 -->
# 4. 데이터 구축

<!-- source: tables/data-opensource.tex:1-14 -->
**표 1. 수집한 오픈소스 데이터셋 개요.**  
<span id="tab:tasks_datasets"></span>

| 과제 | 데이터셋 |
|---|---|
| Text-To-Image (T2I) | LAION, BLIP-3o, ShareGPT-4o-Image, OSP, Echo-4o-Image, OpenGPT-4o, FaceCaption, Flux-Reason-6M, HumanCaption, POSTER-TEXT, AutoPoster, CTW |
| Image Editing (IT2I) | InstructPix2Pix, AnyEdit, PIPE, ImgEdit, SEED-Data-Edit, OmniEdit, UltraEdit, HQEdit, ShareGPT-4o-Image, OpenGPT-4o, X2Edit, X2I2, UniWorld perception, NHR-Edit, GPT-hqedit, GPT-omniedit, GPT-ultraedit, Nano-consistent-150k, Pico Banana |

<!-- source: sections/4.data.tex:5 -->
InternVL의 강력한 멀티모달 이해 기반 위에서 InternVL-U에 멀티모달 생성 및 편집 능력을 부여하기 위해, 공개 데이터셋과 다양한 생성 및 편집 과제에 맞춘 합성 데이터 파이프라인을 결합하여 대규모 학습 코퍼스를 구축한다.

<!-- source: sections/4.data.tex:7-10 -->
## 4.1. 오픈소스 데이터 수집

표 1에 제시한 것처럼, 초기 데이터 풀로 다수의 고품질 이미지 생성 및 이미지 편집 데이터셋을 수집했다. 롱테일 사례, 특히 인물 초상과 텍스트가 풍부한 이미지 영역을 더 잘 다루기 위해 특화 데이터셋으로 이 오픈소스 코퍼스를 추가 확장한다.

<!-- source: sections/4.data.tex:12 -->
## 4.2. 일반 데이터 전처리 및 합성

<!-- source: sections/4.data.tex:14-22 -->
**그림 1. 파이프라인으로 합성한 일반 데이터의 예.** 합성 데이터는 다양한 텍스트 주석을 포함하며 초상, 포스터, 자연 장면 등을 비롯한 여러 시각 영역을 포괄한다.  
<figure><img src="source/figures/data/general_data_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:24 -->
먼저 이미지 생성과 이미지 편집을 위한 일반 데이터 전처리 및 합성 파이프라인을 설계한다. 대표적인 예는 그림 1에 제시한다.

<!-- source: sections/4.data.tex:26-33 -->
**그림 2. 일반 데이터 합성 파이프라인 개요.** 먼저 전처리 단계에서 필터링, 확장, 중복 제거를 적용하여 고품질 소스 풀을 구축한다. 이를 토대로 두 병렬 분기를 배치하여 각각 text-to-image 쌍과 instruction-guided 편집 데이터를 생성한다.  
<figure><img src="source/figures/data/general_data_pipeline.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:35-40 -->
### 4.2.1. 일반 전처리

수집한 오픈소스 데이터셋에 먼저 그림 2와 같이 필터링, 확장, 중복 제거를 위한 일반 전처리 파이프라인을 적용한다. 구체적으로는 저품질 샘플을 제외하기 위해 엄격한 다차원 필터링 프로토콜부터 적용한다. 이 과정은 미적 점수, 해상도 임계값, 안전 기준(예: NSFW 탐지), 워터마크 식별에 따른 필터링을 포함하며, 그 결과 오염되지 않은 고품질 샘플 부분집합을 얻는다.

영역 포괄 범위와 영역 내 다양성을 풍부하게 하기 위해 검색 기반 확장과 합성 기반 확장으로 이루어진 이중 분기 확장 워크플로를 이어서 구현한다. 검색 기반 분기에서는 대규모 검색 엔진에서 이미지 질의와 텍스트 질의를 모두 활용하여 표준 데이터셋에 없는 롱테일 개념과 현실 세계의 변이를 포착한다. 이를 보완하는 합성 기반 분기에서는 기존 샘플의 사실적인 변형을 만들어 이미지 다양체를 조밀하게 한다. 마지막으로 중복 없는 소스 풀을 보장하기 위해 수집한 모든 샘플의 perceptual hash(p-hash)를 계산하고 근접 중복을 제거하여 데이터 효율을 극대화한다.

<!-- source: sections/4.data.tex:42-53 -->
### 4.2.2. Text-to-Image 데이터

그림 2와 같이, 수집 데이터 캡션의 다양성과 품질을 높이기 위해 서로 다른 캡셔닝 전략을 채택한다. 구체적으로 사전학습 MLLM인 Qwen2.5-VL을 이미지 캡셔닝 agent로 채택하고, 다음과 같이 서로 다른 세분성 수준의 캡션을 생성하도록 프롬프트한다.

- **간결한 캡셔닝(Concise Captioning):** 핵심 시각 요소를 짧고 명료하게 기술하여 강한 개념 결속과 프롬프트 준수를 촉진한다.
- **조밀한 캡셔닝(Dense Captioning):** 모델이 전체 장면 구조와 세부 사항에 주의를 기울이도록 전경 피사체, 배경 환경, 스타일 특징을 포괄하는 계층적 설명을 생성한다.
- **인간 중심 캡셔닝(Human-Centric Captioning):** 초상화를 위해 특별히 설계하며 얼굴 특징, 표정, 자세, 의복 세부 사항과 같은 세밀한 속성에 초점을 둔다.

판독 가능한 텍스트를 포함한 이미지가 롱테일에서 희소한 문제를 해결하기 위해 텍스트가 풍부한 데이터에 맞춘 표적 데이터 확장 전략을 추가로 도입한다. 특정 텍스트 내용과 배경 환경이 주어지면 이미지 캡셔너가 먼저 변형 캡션을 생성한다. 그런 다음 이미지 생성 expert(예: Qwen-Image)를 사용해 대응 이미지를 합성한다. 이 과정은 고품질 텍스트-이미지 쌍의 분포를 크게 조밀화한다. 모델에 강건한 이중언어 능력을 부여하기 위해 데이터셋 전반에 포괄적인 영어-중국어 번역 파이프라인도 적용하여 모델이 두 언어 모두에서 동등한 숙련도로 콘텐츠를 해석하고 생성할 수 있게 한다.

<!-- source: sections/4.data.tex:55-78 -->
### 4.2.3. 이미지 편집 데이터

이미지 편집 데이터 합성을 위해 그림 2와 같이 더 정교한 파이프라인을 추가로 도입한다. 먼저 편집 과제를 네 가지 주요 부류로 분류한다.

1. **전역 수준(Global-level):** 구조적 레이아웃을 보존하면서 전체 스타일, 톤 또는 배경을 수정한다.
2. **객체 수준(Object-level):** 경계를 처리하면서 객체를 정밀하게 추가, 제거 또는 대체한다.
3. **속성 수준(Attribute-level):** 색상, 재질, 크기, 개수와 같은 세밀한 속성을 조정한다.
4. **합성적(Compositional):** 일관된 다단계 연산이 필요한 복합 instruction을 실행한다.

이어서 소스 데이터 풀을 바탕으로 multi-agent 프레임워크를 채택하여 instruction-edit 쌍을 생성한다. MLLM 기반 router는 각 소스 이미지에 해당하는 구체적인 편집 과제를 결정한다. 라우팅 결과에 따라 이미지를 특화 agent의 모듈식 풀로 전달한다. 고품질 합성을 보장하기 위해 이 agent들을 Instruction Generation과 Image Editing이라는 두 기능 범주로 계층화한다.

- **Instruction Generation:** 서로 다른 편집 과제는 서로 다른 수준의 의미적 세분성을 포착해야 한다는 점을 고려하여, 과제별 프롬프트를 조건으로 정밀하고 문맥을 인식하는 instruction을 생성하는 Qwen2.5-VL-72B로 이 agent들을 구현한다.
- **Image Editing:** 기존 오픈소스 모델은 부분적으로 학습 데이터 분포의 차이 때문에 서로 다른 강점을 보이므로, 이질적인 편집 모델 ensemble을 통합한다. 각 세분성에 가장 적합한 모델에 서로 다른 과제를 할당하여 전체 데이터셋에서 최적의 시각 충실도를 보장한다.

구축한 코퍼스의 신뢰성을 보장하기 위해 그림 2와 같이 자동화된 과제 인식 검증 모듈도 도입한다. MLLM이 평가하는 3분 평가 프로토콜을 다음과 같이 정의한다.

1. **Instruction Following:** 편집 이미지가 프롬프트를 충실하게 실행하는지 검증한다.
2. **Editing Consistency:** 소스 이미지와 의미적·구조적으로 일관되는지 평가한다.
3. **Generation Quality:** 시각 충실도, 사실성, 아티팩트 억제를 평가한다.

각 이미지-편집 쌍을 과제별 프롬프트에 따라 채점한다. 세 차원 모두에서 미리 정의한 임계값을 넘는 샘플만 유지한다. 이 적응형 필터링은 정렬되지 않았거나 품질이 낮은 예를 효과적으로 제거하며, 그 결과 instruction 정렬과 시각적 일관성이 강한 강건한 데이터셋을 얻는다.

<!-- source: sections/4.data.tex:82 -->
## 4.3. 텍스트 중심 데이터 합성

<!-- source: sections/4.data.tex:84-91 -->
**그림 3. 파이프라인으로 합성한 세 가지 유형의 텍스트 중심 데이터.** 첫 번째 유형은 마스킹된 배경 이미지를 사용하여 자연 이미지 위에 의미적으로 관련된 텍스트를 겹쳐 놓는다. 두 번째 유형은 단색 배경에 텍스트를 렌더링하며 깔끔하고 미적으로 보기 좋은 레이아웃에 초점을 둔다. 세 번째 유형은 번호판, 모바일 인터페이스, 간판 및 이와 유사한 표면의 텍스트를 수정하는 것처럼 기존 이미지 내부의 텍스트를 편집한다.  
<figure><img src="source/figures/data/text_data_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:94-96 -->
시각 매체의 텍스트 요소는 의미 밀도가 매우 높고 의사소통에 중요하므로, 정확한 텍스트 렌더링과 세밀한 편집은 현실 응용에 필수적이다. 텍스트 관련 과제에서 최근 진전이 있었음에도 일반 멀티모달 모델은 여전히 텍스트 중심 생성 및 편집에 어려움을 겪으며, 철자 오류, 비알파벳 언어에 대한 미흡한 지원, 레이아웃 오정렬, 의도하지 않은 시각적 아티팩트를 흔히 보인다.

그 중요성을 고려하여 텍스트 렌더링 및 편집 능력을 한층 더 향상하기 위한 텍스트 중심 데이터 합성 파이프라인을 추가로 도입한다. 그림 3과 같이 세 가지 대표 데이터 유형, 즉 (1) 자연 이미지에 의미적으로 관련된 텍스트 렌더링, (2) 순색 배경에 텍스트 렌더링, (3) 이미지 내부 텍스트 편집을 포괄하며, 이들은 함께 시각적 문맥에서 텍스트 콘텐츠를 이해하고 생성하고 수정하는 모델의 통합 능력을 강화한다.

<!-- source: sections/4.data.tex:98-104 -->
**그림 4. 텍스트 렌더링 데이터 구축 파이프라인.** 합성 텍스트 렌더링을 위해 마스크 이미지, 글꼴 색상, 글꼴 스타일, 적응형 레이아웃 옵션을 준비한다. 렌더링 과정에서는 이러한 속성을 무작위로 샘플링하고 텍스트 길이에 적응하는 타이포그래피로 텍스트를 렌더링한다.  
<figure><img src="source/figures/data/text_data_pipeline_render.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:106-110 -->
### 4.3.1. Text-to-Image 데이터

모델에 더 강한 시각적 텍스트 렌더링 능력을 부여하기 위해 고품질의 다양한 텍스트 데이터를 생성할 수 있는 포괄적이고 자동화된 텍스트 렌더링 데이터 합성 파이프라인을 설계한다. 이 파이프라인은 자연 이미지에 의미적으로 관련된 텍스트를 렌더링하는 방식과 순색 배경에 텍스트를 렌더링하는 방식을 모두 지원하며, 중국어와 영어라는 서로 다른 언어를 포괄한다.

구체적으로 그림 4와 같이, 자연 이미지에 의미적으로 관련된 텍스트를 렌더링할 때는 원래 쌍을 이루던 캡션 주석을 소스 이미지에 직접 렌더링한다. 텍스트 다양성을 높이기 위해 무작위로 선택한 순색 배경에 순수 텍스트 데이터도 렌더링한다. 렌더링 중에는 렌더링 영역의 마스크, 텍스트 색상과 글꼴 유형, 적응형 레이아웃 설계 방안도 고려한다. 이미지에 텍스트가 미적으로 배치되도록 줄바꿈을 자동 삽입하면서 텍스트 크기를 적응적으로 추가 조정할 수 있다. 마지막으로 이미지 캡셔너인 Qwen2.5-VL-72B를 사용하여 렌더링된 이미지에 캡션을 다시 생성한다.

<!-- source: sections/4.data.tex:112-116 -->
### 4.3.2. 이미지 편집 데이터

텍스트 인식 이미지 편집을 합성하기 위해 그림 5와 같이 3단계 파이프라인을 설계한다. 이 파이프라인은 자연 장면과 가상 장면 모두의 텍스트 편집을 포괄하는 고품질 쌍 샘플을 생성할 수 있다. 첫째, OCR 도구인 PaddleOCR을 사용하여 텍스트 영역을 탐지하고 인식된 텍스트, 신뢰도 점수, 경계 다각형을 추출한다. 둘째, MLLM 기반 instruction agent인 Qwen2.5-VL-72B에 후보 영역을 필터링하고 텍스트 관련성과 시각적 일관성을 검증하며 의미적으로 명시적인 편집 instruction을 생성하도록 프롬프트한다. 마지막으로 선택된 텍스트, 다각형, 편집 instruction을 텍스트 편집 agent(예: Flux-Text)의 입력으로 사용하여 정밀하고 문맥을 인식하는 텍스트 편집을 수행한다. 이 워크플로는 텍스트 인식 응용에 적합한 고품질의 의미적으로 정렬된 이미지-텍스트 편집 쌍을 산출한다.

<!-- source: sections/4.data.tex:118-124 -->
**그림 5. 텍스트 편집 데이터 구축 파이프라인.** 첫째, OCR 도구로 편집 후보 텍스트 영역을 추출한다. 둘째, 편집 instruction을 생성한다. 셋째, 생성 모델로 편집된 ground truth를 생성한다. 이 세 단계를 통해 고품질 텍스트 편집 triplet을 합성한다.  
<figure><img src="source/figures/data/text_data_pipeline_edit.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:126-135 -->
## 4.4. 과학 중심 데이터 합성

과학 이미지는 과학 학계와 AI 산업 모두에 매우 중요하다. 과학 중심 이미지의 이해는 폭넓은 관심을 받아 왔지만, 그 생성은 아직 비교적 초기 단계에 머물러 있다. 엄격한 구조성, 높은 의미적 일관성, 강한 지식 의존성, 깊은 추론이 필요한 이미지를 생성하는 모델의 능력을 향상하기 위해 text-to-image와 이미지 편집용 과학 중심 데이터를 선별하는 다양한 엄격한 파이프라인을 설계한다. 이 데이터는 물리학, 화학, 생물학, 컴퓨터 과학 등 여러 학문 분야를 포괄한다. 구체적으로 text-to-image 데이터는 주로 기존 이해 데이터셋과 웹 이미지에서 선별한다. 다양하고 의미 있는 편집 프롬프트가 포함된 입력-출력 이미지 쌍이 필요해 수집이 더 어려운 편집 데이터의 경우, 물리학과 컴퓨터 과학의 편집 데이터를 합성하기 위한 여러 데이터 engine을 설계한다. 과학 데이터 생성 파이프라인은 그림 6에, 과학 데이터 예는 그림 7에 제시한다.

<!-- source: sections/4.data.tex:139-147 -->
**그림 6. 과학 데이터 생성 파이프라인.** 일반 과학 T2I의 경우 웹 이미지와 오픈소스 데이터셋을 수집하고 오픈소스 모델을 이용한 자동 필터링 및 주석 생성을 설계한다. 물리학의 경우 PaddleOCR로 문서에서 이미지를 얻고, 고품질 이미지 쌍을 저렴하게 생성하기 위한 SVG 기반 파이프라인을 제안한다. 컴퓨터 과학의 경우 과제를 정의하고 Python 라이브러리로 이미지를 렌더링한다.  
<figure><img src="source/figures/data/science_data_pipeline.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:149-158 -->
**그림 7. 과학 중심 데이터의 예.** 일반 과학 T2I는 조밀하고 상세한 instruction을 특징으로 하며 여러 학문 분야의 개념을 묘사해야 한다. 물리학과 컴퓨터 과학은 학문적 추론을 수반하는 이미지 편집에 초점을 둔다.  
<figure><img src="source/figures/data/science_data_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:161-168 -->
### 4.4.1. 일반 과학 생성 데이터

Text-to-image 생성을 위한 이미지는 오픈소스 멀티모달 과학 이해 데이터셋(MMMU, AI2D, TQA, MV-Math, MAVIS, CMM, ChemEval, ChEBI, ChemQA), 교과서, 경시·선발 시험(예: IPHO, Gaokao, Kaoyan)을 비롯한 다양한 출처에서 수집한다. 이후 다단계 필터링 전략을 채택하여 고품질 데이터를 얻는다. 첫 단계에서는 해상도가 256p 미만인 이미지를 제거하고, 남은 이미지를 p-hash에 따라 중복 제거한다. 데이터 오염을 방지하기 위해 5절의 benchmark와 동일한 이미지도 제거한다. 두 번째 단계에서는 오픈소스 MLLM인 Qwen3-VL-8B를 사용해 이미지 유형, 주제, 텍스트 길이, 이미지 복잡도, 주제 지식 밀도를 비롯한 여러 차원에서 이미지를 평가하고 필터링한다. 필터링에 관한 자세한 내용은 부록의 일반 과학 절을 참조한다. 이어서 이미지 캡셔너인 Qwen3-VL-32B에 대응 캡션을 합성하도록 프롬프트한다.

<!-- source: sections/4.data.tex:171-186 -->
### 4.4.2. SVG 기반 물리학 편집 데이터

인터넷에는 물리학 이미지가 풍부하지만, 오픈소스 데이터셋에서 편집용 *쌍을 이룬* 물리학 이미지를 얻거나 기존 라이브러리와 소프트웨어로 이를 합성하기는 어렵다. 기존 독점 이미지 편집 모델(예: Nano Banana Pro)을 사용해 주어진 이미지로부터 쌍 이미지를 생성하면 비용이 극도로 높고 품질이 일관되지 않을 수 있다. 최근 Scalable Vector Graphics(SVG) 이해 및 생성의 발전과 최첨단 멀티모달 모델의 강력한 능력에서 영감을 받아, 그림 6과 같이 물리학 이미지 쌍을 합성하는 SVG 기반 파이프라인을 설계한다. SVG는 래스터 이미지를 직접 편집하는 대신 구조화된 SVG 코드를 조작함으로써 대상 이미지를 비용 효율적으로, 고품질이며 해상도에 독립적으로 생성할 수 있게 한다.

첫 단계에서는 물리학 교과서와 시험으로 이루어진 이질적 출처의 문서를 수집하고 PaddleOCR을 사용하여 이미지와 그 텍스트 문맥을 추출한다. 그런 다음 Qwen3-VL-8B를 사용하여 바람직하지 않은 영역의 이미지, 예를 들어 교과서의 삽화, 시험 문제의 현실 세계 사진, 수학 공식, SVG 형식으로 변환하기 어려운 복잡한 이미지를 걸러낸다. 이 이미지들은 전자기학, 역학, 광학, 회로, 열학, 원자물리학 등의 하위 분야를 포괄한다.

그다음 이미지와 그 문맥을 Gemini-3-Flash에 입력하여 원본 이미지에 대응하는 SVG 코드를 생성한다. 모델은 원본 이미지를 입력 이미지로 사용할지 출력 이미지로 사용할지도 결정하고, 편집 프롬프트와 나머지 이미지의 SVG 코드를 생성한다. 두 SVG 코드를 렌더링하여 이미지 쌍을 만든다. Gemini-3-Flash가 생성한 원본 프롬프트는 상세하고 명시적이므로 단계별 추론 프롬프트로 사용할 수 있다. 분야별 지식과 역량을 평가하기 위해 이 프롬프트에 핵심 정보 추출과 요약을 수행하여 단순화된 암시적 프롬프트를 최종 데이터로 얻는다.

마지막으로 `<input_image, prompt, output_image>`의 각 triplet에 다시 필터링을 수행하여 데이터의 정확성과 품질을 검사한다. Gemini-3-Flash를 사용해 풍부한 텍스트 서식을 포함한 이미지와 물리 구조 오류 또는 주석 오류가 있는 이미지를 필터링하여 제거한다. Nano Banana Pro로 출력 이미지를 직접 생성하는 방식과 비교할 때 이 SVG 기반 접근법은 샘플당 비용을 <code>0.16에서</code>0.03으로 크게 줄인다.

<!-- source: sections/4.data.tex:188-202 -->
### 4.4.3. 컴퓨터 과학 편집 데이터

여러 Python 라이브러리를 기반으로 컴퓨터 과학 편집 데이터용 데이터 engine을 구축한다. 이 데이터는 트리, 그래프, finite state machine(FSM) 같은 데이터 구조에 대한 연산과 알고리즘에 초점을 둔다. 구체적인 과제는 다음과 같다.

- **Tree:** 토폴로지 편집 및 노드 조작, 순회 시각화, binary search tree(BST) 연산, 이중 뷰를 갖는 heap 연산, Huffman coding tree, lowest common ancestor(LCA) 및 경로 강조.
- **Graph:** K-hop 이웃 식별, 차수 식별, 순환 탐지, 이분 그래프 색칠, 최단 경로 추론, 방향 그래프 도달 가능성.
- **FSM:** 문자열 추적, 상태 역할 식별, 전이 논리 완성.

이 과제들의 정의는 부록의 컴퓨터 과학 절에 제시한다.

고품질 데이터 생성을 보장하기 위해 먼저 과제 복잡도에 따라 과제별 렌더링 engine을 선택하여 효율과 시각 충실도의 균형을 맞춘다. 트리와 그래프처럼 구조적으로 단순한 과제에는 matplotlib을 사용해 생성 과정을 가속한다. 반면 조밀한 정보 표시가 필요한 state machine에는 최적의 토폴로지 명료성을 보장하기 위해 Graphviz(circo 레이아웃)를 사용한다. 이미지 쌍 전반에서 공간적 일관성(예: 이미지에서 노드 위치가 바뀌지 않아야 함)을 유지하기 위해 노드에 고정 anchor point를 정의한다. 이 제약은 불변 구성 요소가 시각적으로 일관되도록 보장한다.

그런 다음 두 노드 사이 또는 노드와 edge 사이의 거리를 계산하여 노드나 edge가 겹치는 샘플을 탐지하고 제거하는 검증을 수행한다. 이 가림 검사를 통과하지 못한 생성 instance는 모두 폐기하여 데이터셋의 전반적인 구조적 무결성을 보장한다. 마지막으로 전통적 solver로 문제를 풀고 다시 작성하여 CoT 편집 프롬프트를 생성하며, 자세한 내용은 4.7절에 제시한다.

<!-- source: sections/4.data.tex:205-213 -->
**그림 8. 공간 중심 데이터의 예.** 세 가지 공간 중심 시나리오, 즉 입체기하(예: 회전체, 대칭), multi-view CAD(삼면도), 3D 객체의 공간 회전을 고려한다.  
<figure><img src="source/figures/data/spatial_data_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:215-217 -->
## 4.5. 공간 중심 데이터 합성

모델의 공간 이해 능력을 향상하기 위해 입체기하, multi-view CAD, 일반 공간 회전이라는 서로 다른 세 영역에서 공간 중심 데이터를 합성한다. 이미지 예는 그림 8에 제시한다.

<!-- source: sections/4.data.tex:219-231 -->
### 4.5.1. 입체기하 편집 데이터

GeoGebra와 matplotlib을 사용하여 입체기하 편집 데이터를 렌더링한다. 과제는 다음과 같다.

- **회전체(Solid of Revolution):** 주어진 도형을 주어진 축 둘레로 회전하여 형성되는 입체를 그린다.
- **평면 대칭(Plane Symmetry):** 주어진 평면에 대해 주어진 입체와 중심 대칭인 입체를 그린다.
- **점 대칭(Point Symmetry):** 주어진 점에 대해 주어진 입체와 중심 대칭인 입체를 그린다.
- **입체 평행이동(Solid Translation):** 주어진 평행이동 벡터만큼 주어진 입체를 평행이동한다.
- **입체 투영(Solid Projection):** 주어진 입체를 \(xoy\)-평면에 직교 투영한 결과를 그린다.

이 과제들의 구현은 부록의 컴퓨터 과학 절에 제시한다.

<!-- source: sections/4.data.tex:233-236 -->
### 4.5.2. Multi-view CAD 편집 데이터

모델의 공간 이해 능력을 더욱 향상하기 위해 오픈소스 CAD 데이터셋을 기반으로 대응하는 삼면도 편집 데이터를 구축했다. 모델은 입력 등각 뷰와 편집 instruction을 바탕으로 대응하는 다른 뷰를 예측해야 했다. 구체적으로 오픈소스 ABC 데이터셋과 OCC Python 라이브러리를 사용하여 데이터셋의 CAD 파일을 등각 뷰, 정면도, 측면도, 평면도를 포함한 대응 시점의 이미지로 렌더링했다. 렌더링 과정에서 객체의 색상과 재질을 무작위로 설정하여 데이터 분포의 다양성도 높였다. 최종 구축한 편집 데이터셋의 예는 그림 7에 제시한다.

<!-- source: sections/4.data.tex:238-248 -->
### 4.5.3. 공간 회전 편집 데이터

**그림 9. 공간 회전 편집 데이터 합성 파이프라인 개요.** Stage 1에서는 필터링된 참조 이미지 풀을 준비한다. 이어서 Stage 2에서는 객체-문맥 통합을 위한 Object-First 전략 또는 엄격한 배경 보존을 위한 Background-First 전략을 통해 최종 편집 쌍을 생성한다.  
<figure><img src="source/figures/data/rotation_data_pipeline.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:251-264 -->
오픈소스 3D 모델 데이터셋 Objaverse를 활용하여 고품질 객체 회전 데이터를 구축한다. 먼저 객체를 균일한 각도로 회전시키고 렌더링한다. 이는 광범위한 일상 객체를 포괄하지만 일반적으로 풍부한 환경 문맥이 부족하다. 그림 9와 같이 이러한 객체에 적절한 배경을 부여하기 위해 처음에는 객체마다 배경을 포함한 서로 다른 참조 이미지 4개를 생성한다. 그런 다음 이 후보들에 엄격한 다단계 필터링 메커니즘을 적용한다.

- **Bounding Box Detection:** 객체의 bounding box를 탐지하여 변형을 평가하고, 종횡비가 <code>[0.9, 1.1]</code> 범위에 드는 instance만 유지한다. 또한 Background-First 전략의 실행 가능성을 보장하기 위해 회전 중 객체가 이미지 경계를 벗어나는 후보를 제외한다.
- **Object Consistency:** 방향을 특히 중시하여 핵심 시각 속성의 일관성을 평가하고, 원본 입력과 높은 일관성을 보이는 instance만 유지한다.
- **Generation Quality:** 객체-배경 통합의 개연성, 장면과의 스타일 일관성, 전반적인 시각 품질을 평가하고 객체마다 점수가 가장 높은 후보를 선택한다.

이어서 최종 데이터 합성을 위한 서로 다른 두 전략을 설계한다.

- **Object-First 전략:** 객체를 문맥에 자연스럽게 통합하는 것을 우선한다. 먼저 선택된 참조 이미지를 바탕으로 문맥이 풍부한 instruction을 생성한다. 그런 다음 Qwen-Image가 이 instruction과 참조 이미지를 함께 사용하여 편집 이미지를 합성한다. 이 편집 쌍의 높은 품질을 보장하기 위해 GPT-5.1로 객체의 새로운 방향 정확성과 배경 일관성이라는 두 차원에 따라 결과를 추가 필터링한다.
- **Background-First 전략:** 편집 전반에서 배경 일관성을 최대화하는 것을 우선한다. Flux.1 Kontext의 강력한 일관성 능력을 활용하여 객체 제거를 수행하고 깨끗한 배경 이미지를 얻는다. Qwen2.5-VL로 이 제거 연산의 성공 여부를 검증한다. 다음으로 앞서 탐지한 bounding box를 이용하여 다른 방향의 객체를 이 깨끗한 배경에 붙여 넣고, 이로써 배경 장면이 완벽하게 일관된 편집 쌍을 얻는다.

<!-- source: sections/4.data.tex:267-272 -->
**그림 10. 이미지 생성 및 편집용 meme 데이터 예.** 여기의 meme 데이터는 일상에서 흔히 발견되는 인간 유머의 요소와 표현의 미묘한 차이를 포착한다.  
<figure><img src="source/figures/data/humor_data_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:274-283 -->
## 4.6. 유머 중심 데이터 합성

<span id="meme"></span>

Meme은 시각 요소와 텍스트 요소의 결합을 통해 유머, 풍자, 문화 정보를 전달하는 인터넷상의 중요한 표현 형식이 되었다. 모델의 meme 생성 능력을 향상하기 위해 meme에 맞춘 두 가지 학습 데이터, 즉 text-to-image 생성 데이터와 image-to-image 편집 데이터를 합성한다. 예시는 그림 10에 제시한다. 생성 데이터는 사용자가 짧고 추상적인 의도 프롬프트를 제공하면 시스템이 유머, 빈정거림, 놀라움, 무력감 또는 다른 정서적 의도처럼 구체적이거나 암시적인 의미를 전달하는 이미지를 만드는 시나리오를 대상으로 한다. 편집 데이터는 사용자가 입력 이미지를 제공하고 원본 콘텐츠와 스타일을 가능한 한 보존하면서 자연어 instruction으로 이를 수정하는 시나리오를 대상으로 한다. 흔한 형식은 대비나 아이러니를 만들기 위해 간결하고 강렬한 텍스트(예: 자막, 레이블, 대화)를 추가하는 것이다.

<!-- source: sections/4.data.tex:284-290 -->
**그림 11. Meme 데이터 합성 파이프라인.** 5개 단계로 이루어지며, chain-of-thought 추론을 활용해 인터넷 meme을 처리하고 meme 생성 및 편집용 고품질 학습 데이터를 합성한다.  
<figure><img src="source/figures/data/humor_data_pipeline.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:292-302 -->
이 합성 데이터셋을 구축하기 위해 먼저 인터넷과 오픈소스 데이터셋에서 다수의 meme 이미지를 크롤링하여 수집하고, 이어서 자동화된 파이프라인(그림 11)을 적용해 고품질 쌍 이미지와 정렬된 instruction을 생성한다.

- **Stage 1 (Text Presence Detection):** VLM을 사용하여 샘플별 텍스트 탐지를 수행하고 이미지에 보이는 텍스트가 있는지 판정한다.
- **Stage 2 (Model-Augmented Instruction Generation):** 이미지 캡셔너 VLM을 사용해 입력 이미지와 원본 캡션을 바탕으로 model-augmented instruction을 생성하며, 시각적 세부 사항과 의미적 초점을 세밀하게 기술한다.
- **Stage 3 (User-Style Prompt Generation):** CoT captioner를 사용해 실제 사용자 질의에 더 가까운, 더 짧은 user-style 프롬프트를 생성한다.
- **Stage 4 (Paired Image Construction):** 텍스트 존재 여부에 따라 분기한다. 이미지에 텍스트가 있으면 “Text Removing Agent”를 호출하여 이미지 내 텍스트를 지우고 텍스트가 없는 버전을 얻는다. 그렇지 않으면 “Text Adding Agent”를 사용해 지시한 콘텐츠를 추가하거나 원본 이미지에 instruction-driven 수정을 수행하여 이미지 쌍을 구축한다.
- **Stage 5 (Editing Instruction Generation):** editing instruction generator를 사용하여 Stage 3에서 생성된 쌍 이미지와 엄격히 정렬된 편집 instruction을 생성하고, (소스 이미지, 대상 이미지, 편집 instruction)의 학습 triplet을 얻는다.

<!-- source: sections/4.data.tex:304-310 -->
## 4.7. 추론 중심 데이터 합성

<span id="sec:data-reasoning"></span>

현실 응용에서 사용자가 제공하는 생성 및 편집 instruction은 특히 복잡하거나 영역 특화된 시나리오에서 짧고 상위 수준이며 추상적인 경우가 많다. 이러한 간결한 프롬프트는 사용자에게 자연스럽고 편리하지만, 명시적인 속성 지정, 공간 관계, 실행 가능한 편집 단계, 영역별 제약과 같은 핵심 세부 사항을 흔히 생략하므로 모델이 의도를 정확히 해석하고 신뢰할 수 있는 결과를 일관되게 생성하기 어렵다.

이 문제를 해결하기 위해 원시 사용자 instruction과 최종 멀티모달 감독 신호 사이에 명시적인 추론 모듈을 *interpreter*로 도입하는 **추론 중심(reasoning-centric)** 데이터 합성을 제안한다. 짧고 추상적인 instruction이 주어지면 이 모듈은 정제된 목표, 분해된 하위 과제, 검증 가능한 제약, 순서가 지정된 편집 연산을 포함하여 더 구조적이고 구체적이며 실행 가능한 명세를 자동으로 도출한다. 이러한 구조화된 해석은 학습 중 더 명료한 학습 신호를 제공한다. 합성 데이터는 추상적 instruction, 이를 명시화한 추론 trace, 대응하는 실행 대상을 함께 구성하여 모델이 불충분하게 지정된 instruction을 더 잘 따르고, 까다로운 영역에서 강건성을 개선하며, 생성 및 편집 과제 모두에서 제어 가능성을 높이게 한다. 특히 네 가지 핵심 응용 설정, 즉 **(1) 일반 이미지(General Images)**, **(2) 지식 주입 이미지(Knowledge-infused Images)**, **(3) Meme 이미지(Meme Images)**, **(4) 과학 이미지(Science Images)**에 초점을 둔다.

<!-- source: sections/4.data.tex:313-318 -->
**그림 12. 일반 이미지 생성 및 편집을 위한 CoT 추론 및 강화의 예.** Chain-of-thought 추론을 통해 원본 프롬프트에 더 세밀한 세부 사항을 추가하여 강화하며, 이로써 모델은 더 정확하고 충실도 높게 생성 및 편집을 수행할 수 있다.  
<figure><img src="source/figures/data/cot_general_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:320-322 -->
**일반 이미지.** 일반 이미지 생성 및 편집에서 사용자가 제공하는 instruction은 흔히 짧고 불충분하게 지정되어 있다. 장면 구성, 대상 영역 또는 수정 속성을 모호하게 기술하면 모델이 사용자 의도를 잘못 해석하여 충실도가 낮은 생성이나 부정확한 세밀 편집으로 이어질 수 있다. 이 문제를 완화하려면 추론 기반 프롬프트 재작성과 정제가 중요하다. 이에 따라 구축한 데이터셋의 모든 instruction에 CoT augmentation을 적용한다. 생성 과제에서는 추상적 개념을 객체, 배경, 스타일에 대한 상세한 시각적 설명으로 확장한다. 편집 과제에서는 대상 영역을 국소화하기 위한 더 명료한 지시 대상, 수정하거나 보존할 명시적 속성, 필요한 시각 일관성 제약으로 instruction을 보강한다. 이 과정은 원래 의도를 바꾸지 않으면서 더 근거 있고 유익한 프롬프트를 생성하여 감독 신호의 학습 가능성과 결과의 제어 가능성을 개선한다. 그림 12와 같이 추론 시 CoT로 강화한 instruction을 사용하면 사용자 요구에 더 잘 정렬된, 눈에 띄게 더 정확한 생성 및 편집 결과를 얻는다.

<!-- source: sections/4.data.tex:324-325 -->
**지식 주입 이미지.** 지식 주입 이미지 생성 및 편집은 모델이 흔히 간결하고 추상적인 사용자 instruction을 정확히 이해할 뿐 아니라 지식 기반 추론 및 분석의 깊은 능력도 갖출 것을 요구한다. 이 과제의 핵심은 instruction 뒤에 숨은 암시적 배경지식을 해체하고 이를 구체적인 시각 개념 또는 상세한 장면 설명으로 변환하여 사용자 입력의 정보 격차를 효과적으로 메우는 데 있다. 이어서 이렇게 풍부해지고 명시화된 의미 정보를 생성 모델에 입력하여, 논리적 일관성을 유지하면서 사용자의 내재된 의도에 부합하는 고품질 이미지를 생성하도록 유도한다. 그림 13과 같이 선별한 지식 기반 이미지 생성 및 편집 데이터셋의 instruction에 오픈소스 모델을 사용하여 상세 수준의 추론 강화를 수행한다. 예를 들어 모델은 “Mid-Autumn Festival”과 그 전통 음식인 “mooncakes” 사이의 문화적 연관성을 자동으로 확립하거나, “banana after one week”의 상태를 “brown spots”이라는 시각 특징과 연결하여 추상적 개념을 구체적으로 표현할 수 있다.

<!-- source: sections/4.data.tex:327-335 -->
**그림 13. 지식 주입 T2I 및 편집을 위한 CoT 추론 및 강화의 예.** CoT 추론 후 추상적인 지식 개념이 구체화되어 더 정밀한 생성 및 편집이 가능해진다.  
<figure><img src="source/figures/data/cot_knowledge_example.pdf" alt="원문 피겨"></figure>

<!-- source: sections/4.data.tex:337-339 -->
**Meme 이미지.** 4.6절에서 meme 생성 및 편집 과제를 소개했다. Meme 시나리오에서 사용자 instruction은 흔히 짧고 매우 추상적이며(예: “내 행복을 표현하는 이미지를 생성하라”), 대개 구체적인 시각 세부 사항의 설명이 없다. 이를 해결하기 위해 추론 기반 프롬프트 강화를 도입하여 짧은 instruction을 명시적이고 제어 가능한 명세로 변환한다. 원래 의도를 바꾸지 않으면서 프롬프트에 (1) 구체적인 장면 및 시각 요소의 세부 사항, (2) 의도한 정서적 입장과 표현 메커니즘, 즉 유머 구조, (3) 템플릿 및 타이포그래피 제약(예: 캡션 배치 위치)을 보강한다. 편집 과제에는 국소 연산을 추가로 명시하고 어떤 영역과 속성을 그대로 유지해야 하는지 명확히 밝힌다. 결과 파이프라인은 그림 11에 제시한다. 이 추론 중심 instruction 구성은 더 강하고 안정적인 감독 신호를 제공하여 meme 생성과 편집 모두에서 제어 가능성과 사용자 의도와의 정렬을 개선한다.

<!-- source: sections/4.data.tex:341-346 -->
**과학 이미지.** 과학은 의미적으로 올바른 이미지를 생성하기 위해 상세한 추론이 필요한 대표 영역이다. 과학 T2I 과제, 특히 수학 공식과 화학 분자 표기 같은 구조화된 기호를 포함한 과제에서는 먼저 LLM으로 과학 개념을 파싱하여 개념 분석과 레이아웃 계획을 포함한 중간 추론 단계를 생성한 다음 최종 이미지 설명을 생성한다. 과학 이미지 편집에서는 모델이 소스 이미지와 instruction을 해석하고 추상적인 편집 의도를 올바른 과학 논리를 따르는 실행 가능한 텍스트 지시로 변환한다. 물리학 편집 데이터에는 요약 단계 이전의 프롬프트를 reasoning-informed 프롬프트로 사용하며, 여기에는 명시적이고 상세한 단계별 instruction이 포함된다. 컴퓨터 과학 편집 데이터의 경우 먼저 입력 및 출력 이미지를 바탕으로 문제 해결용 데이터 구조를 정의하고 전통적 알고리즘으로 문제를 푼다. 그런 다음 풀이 과정의 각 단계를 상세히 기록하고 사람이 준비한 미리 정의된 템플릿 1–3개에 매핑한다. CoT 데이터의 다양성을 높이기 위해 Qwen3-Max를 사용하여 이 템플릿을 다시 작성한다.

<!-- source: sections/4.data.tex:347-353 -->
**그림 14. 과학 T2I 및 편집을 위한 CoT 추론 및 강화의 예.** CoT 추론을 통해 과학 지식이 더 명시적이고 상세한 방식으로 생성 과정에 주입된다(예: 요소를 어떻게 묘사하고 연산을 어떻게 실행해야 하는지).  
<figure><img src="source/figures/data/cot_science_example.pdf" alt="원문 피겨"></figure>


<!-- source: sections/5.experiment.tex:1 -->
# 5. 실험

<!-- source: sections/5.experiment.tex:4-11 -->
## 5.1. 실험 설정

InternVL-U는 InternVL3.5-2B를 기반으로 구현하며, 그 가중치로 시각 이해 인코더와 멀티모달 문맥 백본을 초기화한다. 텍스트 토크나이저와 대화 형식도 동일하게 사용한다. 이미지 생성에는 Qwen-Image와 동일한 VAE를 사용한다.

시각 생성 헤드는 무작위로 초기화하며 1.7B개의 매개변수로 구성된다. InternVL-U의 총 매개변수 수는 4B이다. 자세한 구성은 표 2에 제시한다.

선행 연구를 따라 이미지 조건과 텍스트 조건 모두에 classifier-free guidance(CFG)를 적용한다. 학습 중 text-to-image 생성 데이터에서는 10% 확률로 조건을 제거한다. 이미지 편집 데이터에서는 텍스트와 이미지를 포함한 멀티모달 조건 전체를 5% 확률로 제거하며, 이미지 입력은 유지하되 텍스트만 제거할 확률도 5%로 둔다.

추론에는 20단계의 Flow-DPM-Solver를 사용한다. 전체 조건을 제거하는 경우와 텍스트 조건만 제거하는 경우(편집 과제)의 CFG 척도는 각각 3.5와 1.5로 설정한다.

그림 19는 설정별로 사용하는 시스템 프롬프트와 사용자 프롬프트를 보여준다. 이 프롬프트의 임베딩은 시각 생성 헤드에 입력할 때 절단한다.

단계별 세부 학습 설정은 표 3에 제시한다. 멀티모달 이해 및 추론 벤치마크는 VLMEvalKit으로 평가한다. 이미지 생성 및 편집 과제에는 자체 개발하여 오픈소스로 공개한 평가 도구인 GenEditEvalKit†을 사용한다.

† https://github.com/open-compass/GenEditEvalKit

<!-- source: tables/config-model.tex:1-17 -->
**표 2. InternVL-U 아키텍처의 상세 구성.**  
<span id="tab:model_config"></span>

| **구성** | **시각 이해 인코더** | **문맥 백본** | **시각 생성 헤드** |
|---|---:|---:|---:|
| **레이어 수** | 24 | 28 | 20 |
| **헤드 수(Q / KV)** | 16 / 16 | 16 / 8 | 12 / 12 |
| **헤드 크기** | 64 | 128 | 128 |
| **중간층 크기** | 4,096 | 6,144 | 6,144 |
| **패치 / 스케일 계수** | 14 | - | 2 |
| **매개변수 수** | 0.3B | 2B | 1.7B |

<!-- source: tables/config-train.tex:1-32 -->
**표 3. 학습 단계별 하이퍼파라미터.**  
<span id="tab:train_config"></span>

| **하이퍼파라미터** | **1단계** | **2단계** | **3단계** |
|---|---:|---:|---:|
| *학습 가능 모듈* |  |  |  |
| 백본 | × | × | ✓ |
| 시각 생성 헤드 | ✓ | ✓ | ✓ |
| 학습률 | 3e-04 | 1e-04 | 1e-05 |
| 학습률 스케줄러 | Constant | Cosine | Cosine |
| 가중치 감쇠 | 0.0 | 0.0 | 0.01 |
| 그래디언트 노름 클리핑 | 0.2 | 0.2 | 1 |
| 옵티마이저 | AdamW (β₁=0.9, β₂=0.999, ε=10⁻⁸) | AdamW (β₁=0.9, β₂=0.999, ε=10⁻⁸) | AdamW (β₁=0.9, β₂=0.999, ε=10⁻⁸) |
| 워밍업 스텝 | 1000 | 1000 | 1000 |
| 학습 스텝 | 250,000 | 60,000 | 20,000 |
| 배치 크기 | 2048 | 1024 | 1024 |
| 생성 해상도(최소, 최대) | (512, 512) | (512, 1024) | (512, 1024) |
| 이해 해상도(최소, 최대) | (448, 448) | (448, 448) | (448, 448) |
| 확산 타임스텝 시프트 | 3.0 | 3.0 | 3.0 |
| 데이터 / 과제 | T2I + IT2I | T2I + IT2I | T2I + IT2I + Und |
| 데이터 비율 | 4:1 | 3:4 | 1:1:2 |
| 손실 가중치(NTP:VP) | 0:1 | 0:1 | 1:20 |

<!-- source: sections/5.experiment.tex:19-40 -->
**그림 19. 과제별 학습에 사용하는 시스템 프롬프트와 사용자 프롬프트.** `<img_uncond>`는 이미지 생성을 위한 학습 가능 특수 토큰이다.  

<figure data-figure="19"><img src="source/figures/generated/figure19_prompt.png" alt="그림 19"></figure>
<span id="sys_prompt"></span>

*T2I 과제의 시스템 프롬프트*

“`text
<|im_start|>system
你是书生·万象，英文名是InternVL，是由上海人工智能实验室、清华大学及多家合作单位联合开发的多模态大语言模型。请通过详细描述图像中物体和背景的颜色、形状、大小、纹理、数量、文字内容以及空间位置关系等来对图像进行全面描述: <|im_end|>
“`

*IT2I 과제의 시스템 프롬프트*

“`text
<|im_start|>system
你是书生·万象，英文名是InternVL，是由上海人工智能实验室、清华大学及多家合作单位联合开发的多模态大语言模型。请描述输入图像的关键特征（颜色、形状、大小、纹理、物体、背景等），然后解释用户的文本指令应该如何改变或修改图像，从而生成一个满足用户要求的新图像，并适当保持与原始输入的一致性: <|im_end|>
“`

*이미지 조건과 텍스트 조건을 모두 제거할 때의 사용자 프롬프트*

“`text
<|im_start|>user
Here is a random image <img_uncond>:<|im_end|>
“`

*텍스트 조건만 제거할 때의 사용자 프롬프트*

“`text
<|im_start|>user
Generate an image based on reference images.<|im_end|>
“`

<!-- source: sections/5.experiment.tex:42-45 -->
## 5.2. 멀티모달 이해 및 추론

멀티모달 이해 및 추론 능력을 평가하기 위해 InternVL-U를 MME-P, SEED, ChartQA, OCRBench, MMMU, MathVerse, LogicVista 등 널리 인정받는 7개 MLLM 벤치마크에서 평가한다.

표 4와 같이 InternVL-U는 멀티모달 이해 및 추론 벤치마크에서 강건한 성능을 보이며, MME-P(1607.5)와 OCRBench(83.9) 같은 핵심 지표에서 Janus-Pro와 Ovis-U1 등 규모가 비슷한 UMM을 큰 폭으로 앞선다. 특히 소형 아키텍처(2B+1.7B)임에도 훨씬 큰 BAGEL(7B+7B)에 견줄 만한 추론 능력을 보이며, MMMU에서는 54.7 대 55.3으로 근접한다. 이는 통합 학습 전략이 이해 전용 기준 모델의 강력한 시각-언어 이해 능력을 효과적으로 보존하여 성능 저하를 최소화하는 동시에, 이해와 생성 사이에서 더 우수한 균형을 달성함을 보여준다.

<!-- source: tables/final/understand_reason_v2.tex:1-33 -->
**표 4. 멀티모달 이해 및 추론 벤치마크에서 InternVL-U와 기준 모델 비교.** *는 저자들의 평가 스크립트로 얻은 결과를 뜻한다. 통합 모델의 크기에서 “A + B”는 이해(A)와 생성(B)에 각각 사용되는 매개변수를 나타낸다.  
<span id="tab:exp_und_reason"></span>

| **모델** | **매개변수 수** | **MME-P** | **SEED** | **ChartQA** | **OCRBench** | **MMMU** | **MathVerse** | **LogicVista** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성기가 없는 MLLM* |  |  |  |  |  |  |  |  |
| LLaVA-1.5V | 7B | 1510.7 | 65.8 | 17.8 | 31.8 | 35.7 | 7.6 | -- |
| Qwen2.5-VL | 3B | 1574.9 | 73.7 | 84.0 | 79.7 | 53.1 | 31.2 | 40.3 |
| InternVL3.5 | 2B | 1552.1 | 75.3 | 80.7 | 83.6 | 59.0 | 53.4 | 47.7 |
| *생성기가 있는 UMM* |  |  |  |  |  |  |  |  |
| JanusFlow | 1.3B | 1333.1 | 70.5 | 42.4 | 53.2 | 29.3 | -- | -- |
| Janus-Pro | 1.5B | 1444.0 | 68.3 | 23.4 | 48.7 | 36.3 | -- | -- |
| Show-o2 | 1.5B | 1450.9 | 65.6 | 40.0 | 24.5 | 37.1 | -- | -- |
| TUNA | 1.5B | 1461.5 | 69.3 | 82.1 | 71.9 | 39.1 | -- | -- |
| MetaQuery-L | 3B+1B | 1574.3 | 73.8 | -- | -- | 53.1 | -- | -- |
| Ovis-U1 | 2.4B+1.2B | 1508.0* | 75.5* | 76.4* | 88.3 | 51.1 | 30.6* | 32.4* |
| Emu3 | 8B | -- | 68.2 | -- | 68.7 | 31.6 | -- | -- |
| BAGEL | 7B+7B | 1687.0 | 78.5 | 78.5 | 73.3 | 55.3 | 48.1* | 44.3* |
| InternVL-U | 2B+1.7B | 1607.5 | 75.2 | 76.6 | 83.9 | 54.7 | 45.6 | 40.3 |

<!-- source: sections/5.experiment.tex:50-56 -->
## 5.3. Text-to-Image 생성

Text-to-image 생성 능력을 종합적으로 평가하기 위해 일반 평가에는 GenEval, DPG-Bench, TIIF, OneIG를, 텍스트 렌더링 품질 평가에는 LongText와 CVTG-2k를, 지식 집약적 생성 평가에는 WISE와 GenExam을 사용한다.

### 5.3.1. 일반 이미지 생성

**GenEval.** GenEval은 객체의 동시 출현, 위치, 개수, 색상과 같은 조합적 이미지 속성을 평가하는 객체 중심 프레임워크이다. 표 5에서 InternVL-U는 BAGEL을 비롯한 기존 통합 모델보다 매개변수가 절반 이하에 불과하면서도 이들 중 가장 높은 종합 점수(0.85)를 달성한다. 또한 대부분의 생성 특화 모델보다 높은 성능을 보인다.

<!-- source: tables/final/geneval.tex:1-32 -->
**표 5. GenEval에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_geneval"></span>

| **모델** | **매개변수 수** | **단일 객체** | **두 객체** | **개수 세기** | **색상** | **위치** | **색상 귀속** | **종합** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 0.98 | 0.81 | 0.74 | 0.79 | 0.22 | 0.45 | 0.66 |
| SD3-Medium | 2B | 0.99 | 0.94 | 0.72 | 0.89 | 0.33 | 0.60 | 0.74 |
| Seedream 3.0 | - | 0.99 | 0.96 | 0.91 | 0.93 | 0.47 | 0.80 | 0.84 |
| GPT Image 1 [High] | - | 0.99 | 0.92 | 0.85 | 0.92 | 0.75 | 0.61 | 0.84 |
| Z-Image | 6B | 1.00 | 0.94 | 0.78 | 0.93 | 0.62 | 0.77 | 0.84 |
| Qwen-Image | 20B | 0.99 | 0.92 | 0.89 | 0.88 | 0.76 | 0.77 | 0.87 |
| *통합 모델* |  |  |  |  |  |  |  |  |
| Show-o2 | 7B | 1.00 | 0.87 | 0.58 | 0.92 | 0.52 | 0.62 | 0.76 |
| Janus-Pro | 7B | 0.99 | 0.89 | 0.59 | 0.90 | 0.79 | 0.66 | 0.80 |
| UniWorld-V1 | 7B+13B | 0.99 | 0.93 | 0.79 | 0.89 | 0.49 | 0.70 | 0.80 |
| OmniGen2 | 3B+4B | 1.00 | 0.95 | 0.64 | 0.88 | 0.55 | 0.76 | 0.80 |
| BAGEL | 7B+7B | 0.99 | 0.94 | 0.81 | 0.88 | 0.64 | 0.63 | 0.82 |
| InternVL-U | 2B+1.7B | 0.99 | 0.94 | 0.74 | 0.91 | 0.77 | 0.74 | 0.85 |

<!-- source: sections/5.experiment.tex:59-62 -->
**DPG-Bench.** DPG-Bench는 여러 객체를 기술하는 조밀한 프롬프트를 제공하여 text-to-image 모델의 정교한 의미 정렬 능력을 평가한다. 표 6에서 본 모델은 다른 통합 모델보다 강한 성능을 보이며, 특히 *Global*과 *Entity* 차원에서 두드러진다.

<!-- source: tables/final/dpgbench.tex:1-32 -->
**표 6. DPG-Bench에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_dpgbench"></span>

| **모델** | **매개변수 수** | **Global** | **Entity** | **Attribute** | **Relation** | **Other** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 82.10 | 89.50 | 88.80 | 91.10 | 89.40 | 84.00 |
| SD3-Medium | 2B | 87.90 | 91.01 | 88.83 | 80.70 | 88.68 | 84.08 |
| GPT Image 1 [High] | - | 88.89 | 88.94 | 89.84 | 92.63 | 90.96 | 85.15 |
| Nano Banana Pro | - | 91.00 | 92.85 | 91.56 | 92.39 | 89.93 | 87.16 |
| Z-Image | 6B | 93.39 | 91.22 | 93.16 | 92.22 | 91.52 | 88.14 |
| Qwen-Image | 20B | 91.32 | 91.56 | 92.02 | 94.31 | 92.73 | 88.32 |
| Seedream 4.5 | - | 89.24 | 94.30 | 92.14 | 92.23 | 93.83 | 88.63 |
| *통합 모델* |  |  |  |  |  |  |  |
| UniWorld-V1 | 7B+13B | 83.64 | 88.39 | 88.44 | 89.27 | 87.22 | 81.38 |
| OmniGen2 | 3B+4B | 88.81 | 88.83 | 90.18 | 89.37 | 90.27 | 83.57 |
| Ovis-U1 | 2.4B+1.2B | 82.37 | 90.08 | 88.68 | 93.35 | 85.20 | 83.72 |
| Janus-Pro | 7B | 86.90 | 88.90 | 89.40 | 89.32 | 89.48 | 84.19 |
| BAGEL | 7B+7B | 88.94 | 90.37 | 91.29 | 90.82 | 88.67 | 85.07 |
| InternVL-U | 2B+1.7B | 90.39 | 90.78 | 90.68 | 90.29 | 88.77 | 85.18 |

<!-- source: sections/5.experiment.tex:66-69 -->
**TIIF.** TIIF는 복잡한 instruction을 체계적으로 따르는 능력을 평가한다. 표 7과 표 8에서 InternVL-U는 통합 모델 가운데 강한 성능을 달성하며, 특히 고급 instruction 준수에서 뛰어나다. 다만 통합 모델과 생성 모델 사이에는 여전히 뚜렷한 격차가 있어 instruction 준수 능력을 앞으로 더 개선할 여지가 있음을 보여준다.

<!-- source: tables/final/tiif-short.tex:1-36 -->
**표 7. TIIF(짧은 프롬프트)에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. 약어: **Attr**=Attribute, **Rel**=Relation, **Reas**=Reasoning, **A+R**=Attribute+Relation, **A+Re**=Attribute+Reasoning, **R+Re**=Relation+Reasoning, **RW**=Real World.  
<span id="tab:exp_tiif_short"></span>

| **모델** | **매개변수 수** | **기본-Avg** | **Attr** | **Rel** | **Reas** | **고급-Avg** | **A+R** | **A+Re** | **R+Re** | **Style** | **Text** | **Designer-RW** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 83.1 | 87.1 | 87.3 | 75.0 | 65.8 | 67.1 | 73.8 | 69.1 | 66.7 | 43.8 | 70.7 | 71.1 |
| Z-Image | 6B | 78.4 | 79.5 | 80.5 | 75.1 | 72.9 | 72.9 | 67.0 | 73.9 | 90.0 | 94.8 | 88.1 | 80.2 |
| Seedream 3.0 | - | 87.1 | 90.5 | 89.6 | 80.9 | 79.2 | 79.8 | 77.2 | 75.6 | 100.0 | 97.2 | 83.2 | 86.0 |
| Qwen-Image | 20B | 86.2 | 90.5 | 88.2 | 79.8 | 79.3 | 79.2 | 78.9 | 75.6 | 100.0 | 92.8 | 90.3 | 86.1 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Show-o | 1.3B | 73.1 | 74.8 | 78.8 | 65.6 | 53.7 | 61.0 | 68.6 | 66.5 | 63.3 | 3.8 | 55.0 | 59.7 |
| Janus-Pro | 7B | 79.3 | 79.3 | 78.3 | 80.3 | 59.7 | 66.1 | 70.5 | 67.2 | 60.0 | 28.8 | 65.8 | 65.5 |
| Ovis-U1 | 2.4B+1.2B | 77.8 | 83.5 | 80.1 | 69.9 | 67.4 | 71.8 | 66.8 | 69.0 | 83.3 | 8.1 | 67.2 | 66.7 |
| BAGEL | 7B+7B | 81.8 | 82.5 | 83.0 | 79.9 | 70.2 | 74.4 | 67.4 | 72.0 | 86.7 | 29.4 | 68.3 | 71.5 |
| Lumina-DiMOO | 8B | 84.9 | 87.0 | 87.6 | 79.8 | 72.8 | 74.8 | 76.8 | 69.8 | 70.0 | 51.1 | 75.0 | 74.7 |
| InternVL-U | 2B+1.7B | 82.3 | 86.0 | 84.1 | 76.7 | 73.5 | 75.3 | 70.4 | 75.5 | 93.3 | 47.5 | 65.3 | 74.9 |

<!-- source: tables/final/tiif-long.tex:1-35 -->
**표 8. TIIF(긴 프롬프트)에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. 약어: **Attr**=Attribute, **Rel**=Relation, **Reas**=Reasoning, **A+R**=Attribute+Relation, **A+Re**=Attribute+Reasoning, **R+Re**=Relation+Reasoning, **RW**=Real World.  
<span id="tab:exp_tiif_long"></span>

| **모델** | **매개변수 수** | **기본-Avg** | **Attr** | **Rel** | **Reas** | **고급-Avg** | **A+R** | **A+Re** | **R+Re** | **Style** | **Text** | **Designer-RW** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 78.7 | 83.2 | 80.4 | 72.4 | 68.5 | 73.7 | 73.3 | 71.6 | 66.7 | 52.8 | 71.5 | 71.8 |
| Z-Image | 6B | 82.8 | 86.5 | 79.9 | 81.9 | 77.0 | 77.6 | 73.8 | 75.6 | 93.3 | 93.2 | 85.5 | 83.0 |
| Seedream 3.0 | - | 84.9 | 90.1 | 85.9 | 78.9 | 80.6 | 81.8 | 78.9 | 78.6 | 93.3 | 87.8 | 83.6 | 84.3 |
| Qwen-Image | 20B | 87.2 | 91.5 | 90.8 | 79.4 | 80.9 | 79.8 | 81.7 | 78.6 | 100.0 | 89.1 | 91.4 | 86.8 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Show-o | 1.3B | 75.8 | 79.8 | 78.3 | 69.3 | 50.4 | 56.8 | 69.0 | 56.2 | 66.7 | 2.8 | 50.9 | 58.9 |
| Janus-Pro | 7B | 78.3 | 82.3 | 73.3 | 79.1 | 58.8 | 56.2 | 70.8 | 60.0 | 70.0 | 33.8 | 60.3 | 65.0 |
| Ovis-U1 | 2.4B+1.2B | 79.4 | 81.5 | 81.4 | 75.2 | 67.8 | 68.3 | 73.8 | 65.9 | 86.7 | 12.7 | 68.7 | 68.2 |
| Lumina-DiMOO | 8B | 78.0 | 81.5 | 79.8 | 72.6 | 68.5 | 74.1 | 69.1 | 66.4 | 63.3 | 40.7 | 72.0 | 68.8 |
| BAGEL | 7B+7B | 80.1 | 83.5 | 79.9 | 76.8 | 72.2 | 75.0 | 70.1 | 74.9 | 83.3 | 33.9 | 67.9 | 71.7 |
| InternVL-U | 2B+1.7B | 81.5 | 81.5 | 82.2 | 80.9 | 72.7 | 76.2 | 67.6 | 75.8 | 83.3 | 50.7 | 66.8 | 73.9 |

<!-- source: sections/5.experiment.tex:71-74 -->
**OneIG-Bench.** 표 9와 표 10에서는 주제-요소 정렬, 텍스트 렌더링 정밀도, 추론을 통해 생성한 콘텐츠, 스타일화, 다양성을 세밀하게 평가하도록 설계된 OneIG-Bench에서 InternVL-U를 평가한다. InternVL-U는 작은 매개변수 규모로도 오픈소스 통합 모델 가운데 가장 높은 종합 점수를 기록하며, 다국어 강건성을 갖춘 세밀한 정렬 능력을 입증한다.

<!-- source: tables/final/oneig.tex:1-31 -->
**표 9. OneIG-EN에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_oneigbench"></span>

| **모델** | **매개변수 수** | **Alignment** | **Text** | **Reasoning** | **Style** | **Diversity** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |
| SDXL | 2.6B | 0.69 | 0.03 | 0.24 | 0.33 | 0.30 | 0.32 |
| FLUX.1 [dev] | 12B | 0.79 | 0.52 | 0.25 | 0.37 | 0.24 | 0.43 |
| Qwen-Image | 20B | 0.88 | 0.89 | 0.31 | 0.42 | 0.18 | 0.54 |
| Z-Image | 6B | 0.88 | 0.99 | 0.28 | 0.39 | 0.19 | 0.55 |
| Seedream 4.5 | - | 0.89 | 1.00 | 0.35 | 0.43 | 0.21 | 0.58 |
| Nano Banana Pro | - | 0.89 | 0.94 | 0.33 | 0.48 | 0.25 | 0.58 |
| *통합 모델* |  |  |  |  |  |  |  |
| Janus-Pro | 7B | 0.55 | 0.00 | 0.14 | 0.28 | 0.37 | 0.27 |
| Show-o2 | 7B | 0.82 | 0.00 | 0.23 | 0.32 | 0.18 | 0.31 |
| Ovis-U1 | 2.4B+1.2B | 0.81 | 0.03 | 0.22 | 0.45 | 0.18 | 0.34 |
| BAGEL | 7B+7B | 0.77 | 0.24 | 0.17 | 0.37 | 0.25 | 0.36 |
| Lumina-DiMOO | 8B | 0.82 | 0.55 | 0.28 | 0.40 | 0.23 | 0.46 |
| OmniGen2 | 3B+4B | 0.80 | 0.68 | 0.27 | 0.38 | 0.24 | 0.47 |
| InternVL-U | 2B+1.7B | 0.82 | 0.74 | 0.27 | 0.40 | 0.25 | 0.50 |

<!-- source: tables/final/oneig-zh.tex:1-32 -->
**표 10. OneIG-ZH에서 일반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_oneigbench_zh"></span>

| **모델** | **매개변수 수** | **Alignment** | **Text** | **Reasoning** | **Style** | **Diversity** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |
| Qwen-Image | 20B | 0.83 | 0.96 | 0.27 | 0.41 | 0.21 | 0.53 |
| Z-Image | 6B | 0.79 | 0.99 | 0.27 | 0.39 | 0.24 | 0.54 |
| Seedream 4.5 | - | 0.83 | 0.99 | 0.30 | 0.43 | 0.21 | 0.55 |
| Nano Banana Pro | - | 0.84 | 0.98 | 0.31 | 0.46 | 0.24 | 0.57 |
| *통합 모델* |  |  |  |  |  |  |  |
| Janus-Pro | 7B | 0.32 | 0.15 | 0.10 | 0.26 | 0.36 | 0.24 |
| BLIP-3o | 8B | 0.61 | 0.09 | 0.21 | 0.37 | 0.23 | 0.30 |
| Lumina-DiMOO | 8B | 0.68 | 0.15 | 0.23 | 0.37 | 0.24 | 0.33 |
| Ovis-U1 | 2.4B+1.2B | 0.72 | 0.15 | 0.21 | 0.43 | 0.20 | 0.34 |
| BAGEL | 7B+7B | 0.67 | 0.37 | 0.19 | 0.36 | 0.27 | 0.37 |
| InternVL-U | 2B+1.7B | 0.75 | 0.90 | 0.23 | 0.37 | 0.26 | 0.50 |

<!-- source: sections/5.experiment.tex:77-87 -->
**정성적 결과.** 정량 지표를 넘어 실제적인 강점을 더 분명히 보여주기 위해 추가 정성 비교를 제시한다. 그림 20과 같이 InternVL-U는 일반 이미지 생성에서 뛰어난 시각적 충실도를 보인다. 특히 복잡한 질감과 섬세한 조명 효과를 표현하면서 각 instruction의 의도를 정확히 포착한다.

**그림 20. 일반 이미지 생성 시각화.** 다른 오픈소스 모델과 비교할 때 InternVL-U는 복잡한 질감과 섬세한 조명 효과를 매우 충실하게 표현하며 각 instruction의 정확한 의도를 포착한다.  
<figure><img src="source/figures/experiment/gen_general_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:91-98 -->
### 5.3.2. 텍스트 중심 이미지 생성

**CVTG-2k.** 표 11에 복잡한 시각적 텍스트 생성을 위해 특별히 설계된 CVTG-2k의 결과를 제시한다. InternVL-U는 평균 단어 정확도 0.623으로 통합 모델 가운데 최고 성능을 달성한다.

<!-- source: tables/final/cvtg.tex:1-33 -->
**표 11. CVTG-2k에서 텍스트 중심 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_cvtg"></span>

| **모델** | **매개변수 수** | **NED** | **CLIPScore** | **단어 정확도-2 regions** | **3 regions** | **4 regions** | **5 regions** | **average** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 0.688 | 0.740 | 0.609 | 0.553 | 0.466 | 0.432 | 0.497 |
| Nano Banana Pro | - | 0.875 | 0.737 | 0.737 | 0.775 | 0.786 | 0.793 | 0.779 |
| Qwen-Image | 20B | 0.912 | 0.802 | 0.837 | 0.836 | 0.831 | 0.816 | 0.829 |
| Z-Image | 6B | 0.937 | 0.797 | 0.901 | 0.872 | 0.865 | 0.851 | 0.867 |
| Seedream 4.5 | - | 0.948 | 0.807 | 0.878 | 0.895 | 0.908 | 0.901 | 0.899 |
| *통합 모델* |  |  |  |  |  |  |  |  |
| Ovis-U1 | 2.4B+1.2B | 0.477 | 0.725 | 0.133 | 0.109 | 0.091 | 0.065 | 0.093 |
| BAGEL | 7B+7B | 0.657 | 0.779 | 0.498 | 0.391 | 0.332 | 0.291 | 0.356 |
| Lumina-DiMOO | 8B | 0.805 | 0.831 | 0.723 | 0.646 | 0.571 | 0.505 | 0.590 |
| InternVL-U | 2B+1.7B | 0.804 | 0.816 | 0.729 | 0.660 | 0.618 | 0.549 | 0.623 |

<!-- source: sections/5.experiment.tex:96-98 -->
**LongText-Bench.** LongText-Bench는 이미지에 긴 텍스트를 렌더링하는 능력을 평가한다. 표 12에서 InternVL-U는 영어 0.738, 중국어 0.860으로 강건한 다국어 텍스트 생성 성능을 보이며, 기존 통합 모델을 큰 폭으로 앞선다. 이 결과는 본 모델이 판독 가능한 텍스트 렌더링에서 기존 통합 모델이 보이던 약점을 효과적으로 해소함을 보여준다.

<!-- source: tables/final/longtext.tex:1-33 -->
**표 12. LongText-Bench에서 텍스트 중심 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_longtext"></span>

| **모델** | **매개변수 수** | **LongText-Bench-EN** | **LongText-Bench-ZH** |
|---|---:|---:|---:|
| *생성 모델* |  |  |  |
| FLUX.1 [dev] | 12B | 0.607 | 0.005 |
| Z-Image | 6B | 0.943 | 0.946 |
| Qwen-Image | 20B | 0.943 | 0.946 |
| Nano Banana Pro | - | 0.981 | 0.949 |
| Seedream 4.5 | - | 0.989 | 0.987 |
| *통합 모델* |  |  |  |
| Janus-Pro | 7B | 0.019 | 0.006 |
| BLIP-3o | 8B | 0.021 | 0.018 |
| Ovis-U1 | 2.4B+1.2B | 0.030 | 0.051 |
| BAGEL | 7B+7B | 0.373 | 0.310 |
| Lumina-DiMOO | 8B | 0.437 | 0.047 |
| OmniGen2 | 3B+4B | 0.561 | 0.059 |
| InternVL-U | 2B+1.7B | 0.738 | 0.860 |

<!-- source: sections/5.experiment.tex:101-109 -->
**정성적 결과.** 그림 21과 같이 InternVL-U는 중국어와 영어 문자뿐 아니라 숫자 및 수학 기호도 높은 판독성과 적은 아티팩트로 렌더링한다. BAGEL과 Ovis-U1 같은 오픈소스 통합 멀티모달 기준 모델보다 텍스트 렌더링 품질이 우수하며, 20B 대규모 모델 Qwen-Image 및 비공개 모델 Nano Banana Pro와도 경쟁력 있는 성능을 보인다.

**그림 21. 텍스트 중심 이미지 생성 시각화.** 결과는 InternVL-U가 중국어, 영어, 숫자 및 수식 기호를 렌더링하는 데 뛰어난 능력을 갖추었음을 보여준다. 오픈소스 통합 멀티모달 모델인 BAGEL과 Ovis-U1보다 렌더링 능력이 우수하며, 대규모 매개변수 모델 Qwen Image 및 상용 비공개 모델 Nano Banana Pro와 견줄 만한 성능을 보인다.  
<figure><img src="source/figures/experiment/gen_text_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:111-116; tables are placed before heading in source -->
### 5.3.3. 지식 기반 이미지 생성

**WISE.** WISE는 모델이 세계 지식을 text-to-image 생성에 통합할 수 있는지 평가한다. 표 13과 같이 CoT를 적용한 InternVL-U는 종합 점수가 0.46에서 0.58로 크게 향상되며 BAGEL, UniWorld-V1 같은 다른 통합 기준 모델을 앞선다. 이는 문화적 상식, 시공간 추론, 자연과학에서 높은 능력을 갖추었음을 시사한다.

<!-- source: tables/final/wise.tex:1-31 -->
**표 13. WISE에서 지식 기반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_wise"></span>

| **모델** | **매개변수 수** | **Cultural** | **Time** | **Space** | **Biology** | **Physics** | **Chemistry** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |
| SD3-Medium | 2B | 0.43 | 0.50 | 0.52 | 0.41 | 0.53 | 0.33 | 0.45 |
| FLUX.1 [dev] | 12B | 0.48 | 0.58 | 0.62 | 0.42 | 0.51 | 0.35 | 0.50 |
| Qwen-Image | 20B | 0.63 | 0.62 | 0.76 | 0.60 | 0.72 | 0.39 | 0.63 |
| *통합 모델* |  |  |  |  |  |  |  |  |
| Janus-Pro | 7B | 0.30 | 0.37 | 0.49 | 0.36 | 0.42 | 0.26 | 0.35 |
| Lumina-DiMOO | 8B | 0.35 | 0.43 | 0.59 | 0.31 | 0.49 | 0.34 | 0.40 |
| Ovis-U1 | 2.4B+1.2B | 0.36 | 0.46 | 0.64 | 0.35 | 0.52 | 0.28 | 0.42 |
| BAGEL | 7B+7B | 0.44 | 0.52 | 0.65 | 0.42 | 0.62 | 0.41 | 0.49 |
| UniWorld-V1 | 7B+13B | 0.53 | 0.55 | 0.73 | 0.45 | 0.59 | 0.41 | 0.55 |
| InternVL-U | 2B+1.7B | 0.37 | 0.51 | 0.68 | 0.39 | 0.62 | 0.39 | 0.46 |
| InternVL-U (w/ CoT) | 2B+1.7B | 0.55 | 0.57 | 0.74 | 0.51 | 0.72 | 0.46 | 0.58 |

<!-- source: sections/5.experiment.tex:116 -->
**GenExam.** GenExam은 시험 형식의 instruction을 통해 text-to-image 모델이 교과 지식을 활용한 추론을 이해하는 능력을 평가한다. 표 14에서 본 모델은 통합 모델 가운데 가장 높은 점수를 달성하며, 특히 물리학, 화학, 생물학에서 강하다. CoT를 적용하면 InternVL-U는 3.7B개의 매개변수만으로 종합 점수 22.9에 도달한다. 이는 과학 중심 이미지 생성에서 InternVL-U의 성능과 이해·추론·생성의 통합 능력을 입증한다.

<!-- source: tables/final/genexam.tex:1-37 -->
**표 14. GenExam(Relaxed Scores)에서 지식 기반 text-to-image 생성 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. 약어: **Math**=Mathematics, **Phy**=Physics, **Chem**=Chemistry, **Bio**=Biology, **Geo**=Geography, **Comp**=Computer Science, **Eng**=Engineering, **Econ**=Economics, **Hist**=History.  
<span id="tab:exp_genexam"></span>

| **모델** | **매개변수 수** | **Math** | **Phy** | **Chem** | **Bio** | **Geo** | **Comp** | **Eng** | **Econ** | **Music** | **Hist** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |
| FLUX.1 [dev] | 12B | 12.2 | 14.4 | 12.5 | 22.8 | 36.4 | 11.0 | 14.0 | 9.2 | 21.3 | 21.7 | 17.6 |
| HunyuanImage-3.0 | - | 17.0 | 17.2 | 18.8 | 18.7 | 30.4 | 15.5 | 16.9 | 11.7 | 23.9 | 20.4 | 19.1 |
| Qwen-Image | 20B | 18.9 | 26.3 | 15.3 | 32.1 | 49.6 | 18.9 | 32.0 | 20.3 | 23.4 | 38.6 | 27.5 |
| Seedream 4.5 | - | 44.7 | 63.4 | 48.9 | 75.8 | 67.6 | 57.9 | 69.7 | 67.3 | 38.0 | 55.0 | 58.8 |
| GPT-Image-1.5 | - | 65.8 | 85.4 | 78.1 | 91.9 | 92.5 | 75.8 | 86.4 | 85.5 | 70.8 | 90.9 | 82.3 |
| Nano Banana Pro | - | 86.3 | 95.1 | 88.7 | 95.9 | 96.5 | 91.7 | 95.1 | 97.2 | 91.0 | 99.9 | 93.7 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |
| BLIP-3o | 8B | 6.4 | 5.5 | 4.7 | 7.0 | 16.7 | 3.6 | 8.4 | 2.5 | 6.0 | 11.2 | 7.2 |
| Janus-Pro | 7B | 13.7 | 8.8 | 8.2 | 7.2 | 18.8 | 3.9 | 10.5 | 4.2 | 14.5 | 6.6 | 9.6 |
| Ovis-U1 | 2.4B+1.2B | 12.2 | 10.8 | 6.6 | 10.0 | 25.4 | 6.1 | 8.8 | 5.4 | 13.2 | 15.1 | 11.4 |
| BAGEL | 7B+7B | 14.7 | 10.6 | 7.9 | 10.8 | 24.5 | 6.8 | 10.2 | 5.3 | 13.7 | 14.4 | 11.9 |
| Show-o2 | 7B | 10.8 | 11.9 | 4.8 | 12.8 | 33.3 | 4.7 | 11.8 | 7.0 | 8.8 | 14.5 | 12.0 |
| InternVL-U | 2B+1.7B | 21.5 | 22.2 | 19.3 | 20.0 | 31.2 | 9.9 | 19.6 | 21.5 | 17.8 | 24.9 | 20.8 |
| InternVL-U (w/ CoT) | 2B+1.7B | 25.6 | 24.2 | 23.5 | 23.6 | 35.6 | 12.0 | 21.4 | 24.4 | 18.4 | 20.3 | 22.9 |

<!-- source: sections/5.experiment.tex:118-127 -->
**정성적 결과.** 그림 22와 같이 모델이 세계 지식을 이해해야 하는 프롬프트에서 InternVL-U는 지식에 더 충실한 렌더링을 제공한다. 복잡한 instruction에도 시각적으로 충실한 결과를 생성하며, 명시적으로 지식을 통합하지 않는 기준 모델보다 현저히 우수하다.

**그림 22. 지식 기반 이미지 생성 시각화.** InternVL-U는 지식을 정확히 렌더링하는 데 탁월한 능력을 보인다. 본 모델은 도메인 지식을 효과적으로 통합하여 복잡한 프롬프트에도 시각적으로 충실한 결과를 생성하며, 구체적인 세계 지식이 없는 기준 모델보다 성능이 크게 우수하다.  
<figure><img src="source/figures/experiment/gen_knowledge_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:130-146 -->
## 5.4. 이미지 편집

이미지 편집 평가에는 기존 벤치마크인 ImgEdit, GEdit-Bench, RISEBench를 사용한다. 또한 텍스트 편집의 광범위한 응용 시나리오를 고려하여, 가상 및 현실 세계 시나리오에서 텍스트 편집을 수행하는 모델의 정확도를 평가하는 텍스트 중심 이미지 편집 벤치마크 TextEdit를 추가로 구축한다.

### 5.4.1. 일반 이미지 편집

**ImgEdit.** ImgEdit는 다양한 단일 턴 및 다중 턴 편집 과제를 포괄한다. 표 15와 같이 InternVL-U는 통합 모델 가운데 경쟁력 있는 편집 능력을 보이며, CoT 모델은 종합 점수 3.82를 달성한다.

<!-- source: tables/final/imgedit.tex:1-33 -->
**표 15. ImgEdit에서 일반 이미지 편집 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다.  
<span id="tab:exp_imgedit"></span>

| **모델** | **매개변수 수** | **Add** | **Adjust** | **Extract** | **Replace** | **Remove** | **Background** | **Style** | **Hybrid** | **Action** | **Overall** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |
| FLUX.1 Kontext | 12B | 4.25 | 4.15 | 2.35 | 4.56 | 3.57 | 4.26 | 4.57 | 3.68 | 4.63 | 4.00 |
| GPT-Image-1 [High] | - | 4.61 | 4.33 | 2.90 | 4.35 | 3.66 | 4.57 | 4.93 | 3.96 | 4.89 | 4.20 |
| Qwen-Image-Edit | 20B | 4.38 | 4.16 | 3.43 | 4.66 | 4.14 | 4.38 | 4.81 | 3.82 | 4.69 | 4.27 |
| Z-Image-Edit | 6B | 4.40 | 4.14 | 4.30 | 4.57 | 4.13 | 4.14 | 4.85 | 3.63 | 4.50 | 4.30 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |
| Lumina-DiMOO | 8B | 3.41 | 2.38 | 1.90 | 3.26 | 2.21 | 2.11 | 4.19 | 2.26 | 3.17 | 2.77 |
| BAGEL | 7B+7B | 3.56 | 3.31 | 1.70 | 3.30 | 2.62 | 3.24 | 4.49 | 2.38 | 4.17 | 3.20 |
| UniWorld-V1 | 20B | 3.82 | 3.64 | 2.27 | 3.47 | 3.24 | 2.99 | 4.21 | 2.96 | 2.74 | 3.26 |
| OmniGen2 | 3B+4B | 3.57 | 3.06 | 1.77 | 3.74 | 3.20 | 3.57 | 4.81 | 2.52 | 4.68 | 3.44 |
| Ovis-U1 | 2.4B+1.2B | 3.99 | 3.73 | 2.66 | 4.38 | 4.15 | 4.05 | 4.86 | 3.43 | 4.68 | 3.97 |
| InternVL-U | 2B+1.7B | 4.13 | 3.40 | 2.27 | 4.13 | 3.39 | 3.84 | 4.77 | 3.03 | 4.05 | 3.67 |
| InternVL-U (w/ CoT) | 2B+1.7B | 4.24 | 3.80 | 2.58 | 4.36 | 3.51 | 3.92 | 4.69 | 3.00 | 4.31 | 3.82 |

<!-- source: sections/5.experiment.tex:145-146 -->
**GEdit-Bench.** GEdit-Bench는 현실적인 편집 요구와 높은 다양성을 함께 갖춘 프롬프트를 포함한다. 표 16에서 InternVL-U는 평균 점수 6.66으로 BAGEL(6.52), Ovis-U1(6.42) 등의 기준 모델을 앞선다. 특히 CoT 전략을 적용하면 점수가 6.88로 더 향상된다. Qwen-Image-Edit 같은 편집 특화 모델이 일부 지표에서는 여전히 앞서지만, InternVL-U의 성능은 다양한 편집 과제에 통합 아키텍처를 적용할 수 있음을 확인해 주며, 명시적 추론 단계를 더했을 때 특히 효과적임을 보여준다.

<!-- source: tables/final/gedit.tex:1-31 -->
**표 16. GEdit-Bench에서 일반 이미지 편집 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. 약어: **BC**=Background Change, **CA**=Color Alteration, **MM**=Material Modification, **MC**=Motion Change, **PB**=Portrait Beautification, **ST**=Style Transfer, **SA**=Subject Addition, **SR**=Subject Removal, **SRp**=Subject Replacement, **TM**=Text Modification, **TT**=Tone Transfer.  
<span id="tab:exp_gedit"></span>

| **모델** | **매개변수 수** | **BC** | **CA** | **MM** | **MC** | **PB** | **ST** | **SA** | **SR** | **SRp** | **TM** | **TT** | **Avg/G_O** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| GPT Image 1 | - | 6.96 | 6.85 | 7.10 | 5.41 | 6.74 | 7.44 | 7.51 | 8.73 | 8.55 | 8.45 | 8.69 | 7.49 |
| Qwen-Image-Edit | 20B | 8.23 | 8.30 | 7.33 | 8.05 | 7.49 | 6.74 | 8.57 | 8.09 | 8.29 | 8.48 | 8.50 | 8.01 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Lumina-DiMOO | 8B | 3.43 | 4.27 | 3.08 | 2.77 | 4.74 | 5.19 | 4.44 | 3.80 | 4.38 | 2.68 | 4.20 | 3.91 |
| Ovis-U1 | 2.4B+1.2B | 7.49 | 6.88 | 6.21 | 4.79 | 5.98 | 6.46 | 7.49 | 7.25 | 7.27 | 4.48 | 6.31 | 6.42 |
| BAGEL | 7B+7B | 7.32 | 6.91 | 6.38 | 4.75 | 4.57 | 6.15 | 7.90 | 7.16 | 7.02 | 7.32 | 6.22 | 6.52 |
| InternVL-U | 2B+1.7B | 7.08 | 7.05 | 6.38 | 7.02 | 6.03 | 6.27 | 7.13 | 6.55 | 6.33 | 6.59 | 6.85 | 6.66 |
| InternVL-U (w/ CoT) | 2B+1.7B | 7.05 | 7.87 | 6.50 | 6.99 | 5.77 | 6.10 | 7.33 | 7.16 | 7.12 | 7.36 | 6.46 | 6.88 |

<!-- source: sections/5.experiment.tex:148-156 -->
**정성적 결과.** 그림 23과 같이 InternVL-U는 원본 이미지의 조명과 구조적 세부 사항을 충실히 보존하면서 사실적인 질감과 스타일을 생성하는 데 뛰어나다. 그 결과 다른 오픈소스 모델보다 광범위한 시나리오에서 더 자연스럽고 일관된 편집 결과를 생성한다.

**그림 23. 일반 이미지 편집 시각화.** InternVL-U는 원본 이미지의 조명과 구조적 세부 사항을 높은 충실도로 유지하면서 사실적인 질감과 스타일을 생성하는 데 뛰어나며, 여러 과제에서 다른 오픈소스 모델보다 우수한 성능을 보인다.  
<figure><img src="source/figures/experiment/edit_general_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:158-168 -->
### 5.4.2. 텍스트 중심 이미지 편집

**TextEdit.** 텍스트 편집 능력을 엄밀하게 평가하기 위해 다양한 편집 시나리오와 고품질 편집 이미지 ground truth를 갖춘 2,148개 샘플의 새로운 벤치마크 **TextEdit**†를 제안한다. 벤치마크 구축에 관한 자세한 내용은 부록의 TextEdit 절을 참조한다. 표 17과 표 18에서 InternVL-U는 이 벤치마크에서 우수한 성능을 보인다. 고전적 지표에서 F1 점수 0.71을 달성하여 Nano Banana Pro와 동률을 이루고, Ovis-U1(0.35) 같은 통합 모델을 큰 폭으로 앞선다. MLLM 기반 평가에서도 이 우위가 재확인된다. InternVL-U는 현실 장면 이미지에서 평균 점수 0.88을 얻어 BAGEL(0.53)을 크게 앞서며, GPT-Image-1.5 같은 비공개 상용 모델과도 경쟁력 있는 능력을 보인다.

† https://github.com/open-compass/TextEdit

<!-- source: tables/final/textedit-rule.tex:1-44 -->
**표 17. TextEdit의 텍스트 중심 이미지 편집 평가(고전적 지표).** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. “Real”은 현실 세계 장면의 소스 이미지를, “Virtual”은 가상 장면의 이미지를 뜻한다. 약어: **OA**=OCR Accuracy, **OP**=OCR Precision, **OR**=OCR Recall, **F1**=OCR F1-Score, **NED**=ROI-Aware NED, **CLIP**=CLIPScore, **AES**=Aesthetic Score. 자세한 평가 지표는 부록의 TextEdit 절을 참조한다.  
<span id="tab:exp_textedit_rule"></span>

| **모델** | **매개변수 수** | **Real-OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES** | **Virtual-OA** | **OP** | **OR** | **F1** | **NED** | **CLIP** | **AES** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Qwen-Image-Edit | 20B | 0.75 | 0.68 | 0.66 | 0.67 | 0.71 | 0.75 | 5.72 | 0.78 | 0.75 | 0.73 | 0.74 | 0.75 | 0.81 | 5.21 |
| GPT-Image-1.5 | - | 0.74 | 0.69 | 0.67 | 0.68 | 0.68 | 0.75 | 5.78 | 0.73 | 0.72 | 0.71 | 0.71 | 0.70 | 0.80 | 5.28 |
| Nano Banana Pro | - | 0.77 | 0.72 | 0.70 | 0.71 | 0.72 | 0.75 | 5.79 | 0.80 | 0.78 | 0.77 | 0.78 | 0.78 | 0.81 | 5.28 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Lumina-DiMOO | 8B | 0.22 | 0.23 | 0.19 | 0.20 | 0.19 | 0.69 | 5.53 | 0.22 | 0.25 | 0.21 | 0.22 | 0.20 | 0.72 | 4.76 |
| Ovis-U1 | 2.4B+1.2B | 0.40 | 0.37 | 0.34 | 0.35 | 0.35 | 0.72 | 5.32 | 0.37 | 0.40 | 0.38 | 0.39 | 0.33 | 0.75 | 4.66 |
| BAGEL | 7B+7B | 0.60 | 0.59 | 0.53 | 0.55 | 0.55 | 0.74 | 5.71 | 0.57 | 0.60 | 0.56 | 0.57 | 0.54 | 0.78 | 5.19 |
| InternVL-U | 2B+1.7B | 0.77 | 0.73 | 0.70 | 0.71 | 0.72 | 0.75 | 5.70 | 0.79 | 0.77 | 0.75 | 0.75 | 0.77 | 0.80 | 5.12 |

<!-- source: tables/final/textedit-mllm.tex:1-33 -->
**표 18. TextEdit의 텍스트 중심 이미지 편집 평가(MLLM 기반 지표).** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. “Real”은 현실 세계 장면의 소스 이미지를, “Virtual”은 가상 장면의 이미지를 뜻한다. 약어: **TA**=Text Accuracy, **TP**=Text Preservation, **SI**=Scene Integrity, **LR**=Local Realism, **VC**=Visual Coherence, **Avg**=MLLM Overall Average. 자세한 평가 지표는 부록의 TextEdit 절을 참조한다.  
<span id="tab:exp_textedit_mllm"></span>

| **모델** | **매개변수 수** | **Real-TA** | **TP** | **SI** | **LR** | **VC** | **Avg** | **Virtual-TA** | **TP** | **SI** | **LR** | **VC** | **Avg** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Qwen-Image-Edit | 20B | 0.92 | 0.82 | 0.75 | 0.57 | 0.80 | 0.77 | 0.57 | 0.79 | 0.92 | 0.80 | 0.77 | 0.77 |
| GPT-Image-1.5 | - | 0.96 | 0.94 | 0.86 | 0.80 | 0.93 | 0.90 | 0.82 | 0.93 | 0.96 | 0.91 | 0.87 | 0.90 |
| Nano Banana Pro | - | 0.96 | 0.95 | 0.85 | 0.88 | 0.93 | 0.91 | 0.87 | 0.92 | 0.96 | 0.94 | 0.89 | 0.92 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Lumina-DiMOO | 8B | 0.17 | 0.06 | 0.04 | 0.02 | 0.05 | 0.09 | 0.02 | 0.06 | 0.16 | 0.05 | 0.03 | 0.08 |
| Ovis-U1 | 2.4B+1.2B | 0.31 | 0.12 | 0.12 | 0.07 | 0.18 | 0.18 | 0.06 | 0.16 | 0.31 | 0.14 | 0.13 | 0.19 |
| BAGEL | 7B+7B | 0.68 | 0.60 | 0.38 | 0.35 | 0.56 | 0.53 | 0.38 | 0.51 | 0.68 | 0.62 | 0.42 | 0.54 |
| InternVL-U | 2B+1.7B | 0.94 | 0.90 | 0.71 | 0.80 | 0.80 | 0.88 | 0.87 | 0.86 | 0.91 | 0.82 | 0.62 | 0.83 |

<!-- source: sections/5.experiment.tex:166-175 -->
**정성적 결과.** 그림 24에서는 제안한 TextEdit 벤치마크에서 대표적인 최고 수준 오픈소스 및 상용 모델의 성능을 시각화한다. InternVL-U는 광범위한 텍스트 편집 시나리오에서 강한 결과를 보인다. 특히 이미지에서 교체할 텍스트의 위치를 정확히 찾아 목표 텍스트로 바꾸면서도 시각적 심미성과 텍스트 정확성을 모두 보존한다. 이 결과는 현재 최고 수준의 성능을 명확히 보여주고 기존 텍스트 편집 능력의 상한을 효과적으로 드러내며, 본 벤치마크가 텍스트 중심 이미지 편집의 성능 최전선을 어떻게 규정하는지 부각한다.

**그림 24. 텍스트 중심 이미지 편집 시각화.** InternVL-U는 더 정확하고 충실한 텍스트 편집 능력을 보이는 동시에, 편집 대상 영역 밖의 텍스트 및 시각 콘텐츠를 일관되게 보존한다.  
<figure><img src="source/figures/experiment/edit_text_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:177-186 -->
### 5.4.3. 추론 기반 이미지 편집

**RISEBench.** RISEBench에서 논리적 추론이 필요한 복잡한 편집 instruction을 처리하는 모델의 능력을 추가로 평가한다. 표 19와 같이 CoT 전략을 도입하면 InternVL-U의 종합 점수가 3.6에서 9.4로 크게 향상된다. 이에 따라 오픈소스 통합 기준 모델인 BAGEL(6.1)뿐 아니라 Qwen-Image-Edit(8.9) 같은 생성 특화 모델도 앞선다. 특히 CoT는 Instruction Reasoning(IR)과 Appearance Consistency(AC)를 크게 개선하며, 복잡하고 논리에 의존하는 편집 과제를 정확히 수행하려면 명시적 추론이 필수적임을 보여준다.

<!-- source: tables/final/rise.tex:1-32 -->
**표 19. RISEBench에서 추론 기반 이미지 편집 능력 평가.** 통합 모델 크기의 “A + B”는 이해(A)와 생성(B) 매개변수를 각각 나타낸다. 약어: **IR**=Instruction Reasoning, **AC**=Appearance Consistency, **VP**=Visual Plausibility.  
<span id="tab:exp_rise"></span>

| **모델** | **매개변수 수** | **Temporal** | **Causal** | **Spatial** | **Logical** | **Overall** | **IR** | **AC** | **VP** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *생성 모델* |  |  |  |  |  |  |  |  |  |
| FLUX.1 Kontext | 12B | 2.3 | 5.5 | 13.0 | 1.2 | 5.8 | 26.0 | 71.6 | 85.2 |
| Qwen-Image-Edit | 20B | 4.7 | 10.0 | 17.0 | 2.4 | 8.9 | 37.2 | 66.4 | 86.9 |
| Seedream 4.0 | - | 12.9 | 12.2 | 11.0 | 7.1 | 10.8 | 58.9 | 67.4 | 91.2 |
| Nano Banana Pro | - | 41.2 | 61.1 | 48.0 | 37.6 | 47.2 | 77.0 | 85.5 | 94.4 |
| GPT-Image-1.5 | - | 54.1 | 60.0 | 62.0 | 21.2 | 50.0 | 69.7 | 92.5 | 94.9 |
| *통합 모델* |  |  |  |  |  |  |  |  |  |
| Lumina-DiMOO | 8B | 2.4 | 1.1 | 4.0 | 1.2 | 2.2 | 34.0 | 50.7 | 72.3 |
| Ovis-U1 | 2.4B+1.2B | 1.2 | 3.3 | 4.0 | 2.4 | 2.8 | 33.9 | 52.7 | 72.9 |
| BAGEL | 7B+7B | 2.4 | 5.6 | 14.0 | 1.2 | 6.1 | 36.5 | 53.5 | 73.0 |
| InternVL-U | 2B+1.7B | 3.5 | 2.2 | 5.0 | 3.5 | 3.6 | 35.6 | 52.7 | 75.9 |
| InternVL-U (w/ CoT) | 2B+1.7B | 4.7 | 7.8 | 1.8 | 5.9 | 9.4 | 43.9 | 64.4 | 79.7 |

<!-- source: sections/5.experiment.tex:185-194 -->
**정성적 결과.** 그림 25와 같이 InternVL-U는 다단계 추론과 엄격한 논리 제약이 필요한 복잡한 편집 instruction을 기존 방법보다 안정적으로 처리한다. 달력 날짜 갱신과 같은 시간 계산, 이미지에 맞는 시를 검색하는 것과 같은 공간적·문화적 이해, 이진 탐색 트리 삽입과 같은 정밀한 알고리즘 규칙 등 다양한 제약을 정확히 해석하고 실행할 수 있다.

**그림 25. 추론 기반 이미지 편집 시각화.** InternVL-U는 다단계 추론이 필요한 복잡한 프롬프트를 처리할 때 최신 모델보다 우수하다. 달력 날짜를 갱신하는 시간 계산, 시를 배치하기 위한 공간적·문화적 이해, 이진 탐색 트리 삽입을 위한 정밀한 알고리즘 규칙에 이르는 다양한 논리 제약을 정확히 해석하고 실행하는 본 모델의 우수한 능력을 결과가 보여준다.  
<figure><img src="source/figures/experiment/edit_cot_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:196-201 -->
**그림 26. 더 특수한 이미지 편집 사례 시각화.** InternVL-U는 복잡한 편집 과제에서 발전된 공간 추론 능력과 정밀한 제어력을 보인다. 결과는 그래프 속성(예: 노드 차수)을 정확히 식별하고, 적절한 표현을 갖춘 유머 중심 콘텐츠를 생성하며, 좌표 벡터에 따라 정밀한 3D 기하 변환을 실행하는 본 모델의 우수한 능력을 부각하여 특수 영역에서의 폭넓은 적용 가능성을 보여준다.  
<figure><img src="source/figures/experiment/edit_more_data_comp.pdf" alt="원문 피겨"></figure>

<!-- source: sections/5.experiment.tex:203-204 -->
## 5.5. 추가 정성적 결과

그림 26에는 표준 편집을 넘어서는 InternVL-U의 독자적 능력을 보여주는 특수 편집 사례를 제시한다. InternVL-U는 컴퓨터 과학 지식, 유머 중심 콘텐츠 생성, 수학 관련 편집을 포함한 드물고 까다로운 요구도 강건하게 처리하며, 표준 편집 설정을 넘어선 강한 제어 가능성과 폭넓은 적용 가능성을 입증한다.


<!-- source: sections/6.conclusion.tex:1-3 -->
# 결론

본 연구에서는 이해, 추론, 생성, 편집 역량을 효과적으로 보편화하는 통합 멀티모달 모델 InternVL-U를 제시했다. 양식별 모듈성을 갖춘 통합 컨텍스트 모델링과 분리된 시각 표현이라는 원칙을 따름으로써, 제안 아키텍처는 강력한 이해 백본에 생성 역량을 매끄럽게 통합한다. 고수준 지능과 시각 생성 사이의 간극을 한층 더 좁히기 위해 사고 사슬(Chain-of-Thought, CoT) 패러다임을 적용한 포괄적인 데이터 합성 파이프라인을 도입했으며, 이를 통해 모델이 추상적인 사용자 의도를 정밀한 시각적 실행과 정렬할 수 있게 했다. 실험 결과는 InternVL-U가 지식 집약적 생성 및 편집에서 뛰어난 성능을 발휘할 뿐만 아니라 멀티모달 이해 및 추론 벤치마크에서도 경쟁력 있는 성능을 유지함을 확인해 준다. InternVL-U가 강건한 기준선으로 자리매김하고, 포괄적인 범용 역량을 갖춘 AGI 지향 통합 멀티모달 모델(UMM)을 개발하려는 커뮤니티의 진전을 가속하기를 기대한다.



# 부록


<!-- source: sections/appendix.tex:1-50 -->
# TextEdit 벤치마크



## 설계 동기

텍스트-이미지 생성 및 이미지 편집 모델이 실제 응용 분야에서 점차 널리 채택됨에 따라, **텍스트 중심 이미지 편집**은 광고 디자인, 포스터 수정, UI 현지화, 상업용 자산 업데이트에서 빈번히 요구되는 기능이 되었다. 그러나 기존의 범용 이미지 편집 모델은 텍스트 콘텐츠를 처리할 때 여전히 신뢰성이 낮다. 한편으로 생성된 텍스트에는 철자 오류, 왜곡된 글리프, 망가진 여러 줄 레이아웃, 배경과의 부자연스러운 융합이 자주 나타난다. 다른 한편으로 모델은 텍스트를 교체하면서 비대상 영역(예: 재질 텍스처, 얼굴 세부 묘사, 배경 구조)을 의도치 않게 변경하는 경우가 많아, 사실상 “텍스트 편집”이 “이미지 전체 편집”으로 변질된다. 또한 표~표 benchmarks-class에 제시한 것처럼, 기존의 텍스트 중심 벤치마크(예: AnyText, LongText, CVTG-2K)는 주로 텍스트 *생성*의 정확도에 초점을 맞추며, 구체적인 텍스트 *편집* 시나리오를 충분히 모델링하지 못한다. MARIO-Eval-edit와 같은 텍스트 편집 벤치마크가 존재하지만, 이미지 출처가 제한된 종류의 텍스트 시나리오만 포괄하므로 실제 환경과 합성 디자인 자료 모두에서 접하는 다양한 텍스트 매체와 레이아웃 형태를 충분히 반영하지 못한다. 더 나아가 이러한 벤치마크에는 편집 충실도와 시각적 보존에 대한 체계적인 평가가 없다.

### 표 20. 오픈소스 텍스트 생성·편집 벤치마크 비교

| Benchmark | Type | Size | Human Filter | GT Ann. | Sub-class | Traditional Eval. | LLM Eval. |
|---|---|---:|:---:|:---:|---:|:---:|:---:|
| AnyText | Text Generation | 2,000 | ✗ | ✗ | – | ✓ | ✗ |
| LongText | Text Generation | 320 | ✓ | ✗ | 8 | ✗ | ✓ |
| CVTG-2K | Text Generation | 2,000 | ✓ | ✗ | 2 | ✓ | ✗ |
| MARIO-Eval-edit | Text Edit | 4,000 | ✗ | ✗ | – | ✓ | ✗ |
| **TextEdit (본 연구)** | Text Edit | **2,148** | ✓ | ✓ | **18** | ✓ | ✓ |



이미지 편집 모델의 역량을 종합적으로 평가하기 위해, 새롭고 세심하게 구성한 벤치마크인 **TextEdit**를 제안한다. TextEdit는 더욱 체계적이고 세분화되었으며 사람이 선별한 평가 프레임워크를 제공함으로써 기존 텍스트 중심 편집 벤치마크의 한계를 해소한다. TextEdit의 주요 장점은 다음과 같다.

- **사람이 선별한 데이터 파이프라인:** 합성 데이터나 자동 수집 데이터에 크게 의존하는 기존 벤치마크와 달리, TextEdit는 사람이 필터링하는 파이프라인을 채택하여 사실적이고 품질이 높은 편집 시나리오를 확보하고 잡음이 있거나 모호한 샘플을 줄인다.

- **수작업으로 주석한 정답:** **사람이 직접 편집한 정답(Ground Truth, GT) 이미지**를 제공하여 정밀한 정량 평가를 가능하게 한다. 이를 통해 픽셀 수준 충실도 지표를 신뢰성 있게 계산하고 배경 보존 정도를 정확히 평가할 수 있다.

- **세분화된 시나리오 분류 체계:** TextEdit는 텍스트 편집 시나리오의 **서로 다른 18개 하위 클래스**를 포괄하여, 범주가 제한적이거나 거칠게 나뉜 기존 벤치마크보다 더 체계적이고 상세한 평가를 제공한다.

- **LLM 기반 지시와의 정렬:** 이 벤치마크는 현대적인 LLM 기반 상호작용에 부합하는 순수 텍스트 지시 패러다임을 따른다. 글리프 맵이나 분할 마스크 같은 보조 입력이 필요하지 않아 지시 이행 능력을 더욱 자연스럽게 평가할 수 있다.

- **하이브리드 평가 프로토콜:** 대상 정확도, 텍스트 보존, 장면 무결성, 국소적 사실성, 시각적 일관성에 걸쳐 전통적인 OCR 및 이미지 충실도 지표와 현대적인 멀티모달 LLM 기반 평가를 결합한다. 이 이중 트랙 프로토콜을 통해 종합적인 평가가 가능하다.

## 설계 세부 사항

실제 사용자의 시나리오에 기반한 TextEdit는 체계적인 **시나리오 분류 체계**와 강건한 **평가 프로토콜**을 통해 다양한 실세계 요구와 모델 평가 사이의 간극을 좁힌다. 이러한 통합 설계는 기술적인 텍스트 편집 성능과 실용적 사용성을 모두 종합적으로 평가할 수 있게 한다.

### 시나리오 분류 체계

텍스트 중심 편집 시나리오를 **가상 장면(Virtual Scenes)**과 **실세계 장면(Real-world Scenes)**이라는 두 개의 상위 영역으로 구성한다. 표 benchmarks-class에 정의 및 통계와 함께 자세히 제시한 이 세분화된 분류 체계는 *포스터*, *만화*, *슬라이드*, *GUI*와 같은 디지털 형식부터 *제품*, *건축물*, *보드형 매체*, *개인 액세서리*, *운송 수단*, *워터마크*, *종이 매체*와 같은 실세계 환경에 이르기까지 다양한 텍스트 매체의 미묘한 차이를 포착한다. 그림 text-bench에는 이러한 하위 범주의 분포를 추가로 제시한다. 이 데이터셋을 구축하기 위해 해당 시나리오에 부합하는 고품질 원본 이미지를 선별하고 규칙 기반 메커니즘으로 편집 지시를 합성했다. 그 결과 생성된 정답 이미지는 시각적 자연스러움과 지시 충실도를 보장하기 위해 엄격한 수작업 검증을 거쳤으며, 이를 통해 정량 평가를 위한 신뢰할 수 있는 골드 스탠더드를 확립했다.


<figure data-figure="27"><img src="source/figures/appendix/text-bench-data.pdf" alt="그림 27"><figcaption><b>그림 27.</b> TextEdit 벤치마크의 데이터 분포.</figcaption></figure>

### 표 21. TextEdit의 통합 분류 체계와 데이터 통계

| Major | ID | Category (Mid) | ID | Specific Scene (Sub) | Count |
|---|---:|---|---:|---|---:|
| Virtual Scenes | 1.1 | Poster Scenes | 1.1.1 | Activities / Promotions Posters | 57 |
|  |  |  | 1.1.2 | Product / Advertising Posters | 74 |
|  |  |  | 1.1.3 | Movie / Art Posters | 107 |
|  | 1.2 | Comic Scenes | 1.2.1 | Dialogue / Narration | 65 |
|  |  |  | 1.2.2 | Onomatopoeia / Special-effects Text | 26 |
|  | 1.3 | Slide / Presentation | 1.3.1 | Titles / Subtitles | 71 |
|  |  |  | 1.3.2 | Charts / Explanatory Text | 73 |
|  | 1.4 | GUI Scenes | 1.4.1 | Game Interfaces | 138 |
|  |  |  | 1.4.2 | Browser Interfaces | 44 |
|  |  |  | 1.4.3 | App Interfaces (Mobile/TV) | 45 |
|  |  |  | 1.4.4 | Operating-System Desktops | 61 |
| Real-world Scenes | 2.1 | Objects Surface | – | Packages, Bottles, Boxes, Coins 등 | 168 |
|  | 2.2 | Signage Surface | – | Building Signs, Storefronts, Billboards 등 | 339 |
|  | 2.3 | Board-like Media Surface | – | Blackboards, Whiteboards 등 | 235 |
|  | 2.4 | Personal Accessories Surface | – | Clothing Prints, Badges 등 | 192 |
|  | 2.5 | Transport Surface | – | Cars, Buses, Trains, Ships 등 | 257 |
|  | 2.6 | Watermarks | – | Photo Watermarks, Brand Marks, Corner Stamps 등 | 69 |
|  | 2.7 | Paper Media Surface | – | Papers, Books, Newspapers, Menus 등 | 127 |
| **Total** |  |  |  |  | **2,148** |



### 표 22. 평가 지표 개요

| Category | Metric | 측정 대상 |
|---|---|---|
| Classic — Text-centric | OCR Accuracy | 대상 영역의 생성 텍스트와 정답 문자열 사이의 최대 유사도 |
|  | OCR Precision | 배경 텍스트 보존의 정확성(환각·오류 배경 텍스트에 페널티) |
|  | OCR Recall | 배경 텍스트 보존의 완전성(누락된 배경 텍스트에 페널티) |
|  | OCR F1-Score | OCR Precision과 OCR Recall의 조화 평균 |
|  | ROI-Aware NED | 원본 텍스트 bounding box 내부의 normalized edit distance |
| Classic — General | CLIPScore | 편집 이미지와 대상 caption 사이의 의미 정렬 |
|  | Aesthetic Score | CLIP 기반 미학 예측기가 산출한 시각적 매력도 |
| MLLM-based | Target Accuracy | 대상 텍스트의 철자 정확성과 삭제 품질 |
|  | Text Preservation | 비대상 배경 텍스트의 온전한 보존 여부 |
|  | Scene Integrity | 배경 geometry와 객체의 안정성 및 왜곡 여부 |
|  | Local Realism | inpainting 경계와 blur·seam 등 artifact |
|  | Visual Coherence | 글꼴 style, lighting, texture와 원본 장면의 조화 |
|  | MLLM Overall Avg | MLLM 하위 점수의 가중 평균(40/30/10/10/10) |



### 평가 지표



텍스트 편집의 정량 평가는 특정 텍스트 콘텐츠를 조작하는 동시에 배경을 엄격히 보존해야 한다는 이중 요구 때문에 어렵다. 총체적인 평가를 제공하기 위해 **전통적 지표(Classic Metrics)**와 **MLLM 기반 지표(MLLM-based Metrics)**를 결합한 하이브리드 평가 전략을 사용한다.

**전통적 지표**는 텍스트의 존재 여부와 정확성에 초점을 맞춘다. 표준 OCR 도구를 사용하여 편집 거리와 검출률을 측정한다. 구체적으로 평가는 *대상 영역(Target Region)*과 *배경 영역(Background Region)*으로 분리하며, 전자는 편집 성공 여부를, 후자는 보존 능력을 측정한다. 또한 CLIPScore를 사용하여 전반적인 이미지 품질과 의미적 정렬을 평가하고, 미적 품질도 함께 평가한다.

**MLLM 기반 지표**는 “고스팅” 아티팩트, 조명 불일치, 부분적인 삭제와 같은 시각적 미묘함을 더 잘 포착하기 위해 추가로 도입한다. 전문가 수준의 포렌식 분석을 모사하기 위해 가장 강력한 멀티모달 이해 모델인 Gemini-3-Pro를 심사 모델로 사용하여 국소적 사실성과 장면 무결성 등의 차원에 세분화된 점수를 부여하며, 이를 통해 인간의 선호에 더욱 부합하는 평가를 제공한다.

아래에서는 표~표 benchmark_metrics의 구조에 따라 각 평가 지표의 구체적인 구현을 설명한다.




<!-- source: sections/appendix.tex:51-100 -->
### (a) 고전적 지표(텍스트 중심)

먼저 레벤슈타인 거리 <code>D_lev(cdot, cdot)</code>에 기반한 정규화 유사도 함수 <code>S(s_1, s_2)</code>를 정의한다. 이 함수는 텍스트 중심 지표의 토대가 된다.


<pre class="equation">S(s_1, s_2) = 1 - fracD_lev(s_1, s_2)max(|s_1|, |s_2|, 1)</pre>


여기서 <code>s_1</code>과 <code>s_2</code>는 비교할 두 문자열을 나타내고, <code>|s_1|</code>과 <code>|s_2|</code>는 각각의 길이를 나타낸다. <code>max(|s_1|, |s_2|, 1)</code> 항은 분모가 0이 되지 않도록 하는 정규화 인자로 사용되며, 유사도 점수 <code>S</code>를 <code>[0, 1]</code> 범위로 제한한다. 이때 1은 완전한 일치를 의미한다.

#### (i) OCR 정확도

이 지표는 대상 텍스트가 편집 영역에 올바르게 렌더링되었는지를 평가한다. <code>mathcalT_gen</code>을 생성 이미지에서 검출된 문자열 가운데 대상 편집 영역과 크게 겹치는 문자열의 집합(Intersection over Union, <code>textIoU &gt; 0.5</code>)이라고 하자. 정확도는 검출된 텍스트와 정답 대상 텍스트 <code>t_tgt</code> 사이의 최대 유사도에 페널티 계수를 적용하여 다음과 같이 정의한다.


<pre class="equation">textAcc = max_t in mathcalT_gen S(t, t_tgt) times mathbbP_fail</pre>


여기서 <code>t</code>는 집합 <code>mathcalT_gen</code>에 속하는 후보 문자열을 나타낸다. <code>mathbbP_fail</code> 항은 편집 실패를 불이익 처리하기 위한 페널티 계수이다. 구체적으로, 원본 출발 텍스트 <code>t_src</code>가 해당 영역에서 여전히 검출되는 반면 대상 텍스트 <code>t_tgt</code>는 검출되지 않으면 <code>mathbbP_fail</code>을 0.2로 설정하고, 그렇지 않으면 <code>mathbbP_fail = 1.0</code>으로 설정한다.

#### (ii) OCR 정밀도

이 지표는 배경 텍스트 보존의 정확성을 측정하며, 환각으로 생성되거나 잘못된 배경 텍스트에 페널티를 부여한다. 배경 영역에서 검출된 각 텍스트 항목 <code>t_i</code>(대상 영역과의 <code>textIoU &lt; 0.5</code>인 항목)에 대해, 원본 이미지의 배경 텍스트 집합 <code>mathcalT_bg^orig</code>에서 가장 잘 일치하는 항목을 찾는다.


<pre class="equation">textPrecision = frac1|mathcalT_bg^gen| sum_t in mathcalT_bg^gen max_t&#x27; in mathcalT_bg^orig S(t, t&#x27;)</pre>


여기서 <code>mathcalT_bg^gen</code>은 생성 이미지에서 검출된 배경 텍스트의 집합을 나타내고, <code>|mathcalT_bg^gen|</code>은 그 집합의 크기이다. 검출된 모든 배경 텍스트가 원본의 배경 텍스트와 매우 유사하여 무관한 텍스트가 생성되지 않을 때 이 지표는 높은 점수를 얻는다.

#### (iii) OCR 재현율

이 지표는 배경 텍스트 보존의 완전성을 평가하며, 누락된 배경 텍스트에 페널티를 부여한다. <code>mathcalT_bg^orig</code>에 속하는 각 원본 배경 텍스트 <code>t&#x27;</code>에 대해, 생성 이미지에서 해당 텍스트가 얼마나 잘 보존되었는지를 측정한다.


<pre class="equation">textRecall = frac1|mathcalT_bg^orig| sum_t&#x27; in mathcalT_bg^orig max_t in mathcalT_bg^gen S(t, t&#x27;)</pre>


재현율이 높다는 것은 원본 배경 텍스트 대부분이 실수로 삭제되거나 변경되지 않고 편집 이미지에 성공적으로 유지되었음을 의미한다.

#### (iv) OCR F1 점수

F1 점수는 OCR 정밀도와 OCR 재현율의 조화 평균을 계산하여 두 측면이 균형을 이루는 지표를 제공한다.


<pre class="equation">textF1 = 2 times fractextPrecision times textRecalltextPrecision + textRecall</pre>


이 통합 지표는 배경 텍스트 보존의 정확성과 완전성을 모두 포착하여 텍스트 수준 편집 품질을 종합적으로 평가한다.

#### (v) ROI 인식 NED

이 지표는 원본 출발 텍스트의 경계 상자로 정의되는 특정 관심 영역(Region of Interest, ROI) 내부의 편집 품질만을 엄격하게 평가한다. ROI에서 추출한 예측 텍스트 문자열 <code>t_pred</code>와 대상 문자열 <code>t_tgt</code> 사이의 유사도를 계산한다. 원본 텍스트와의 잔여 유사도가 여전히 높으면 *삭제 실패 페널티*를 적용한다.


<pre class="equation">textNED = S(t_pred, t_tgt) times mathbbI_resid</pre>


여기서 <code>t_pred</code>는 ROI를 직접 잘라내어 얻은 OCR 인식 결과를 나타낸다. <code>mathbbI_resid</code>는 페널티 항으로 작용하는 잔여 지시 함수이다. <code>S(t_pred, t_src) &gt; 0.9</code>이면(즉, 출발 텍스트 <code>t_src</code>가 효과적으로 삭제되지 않았음을 의미하면) <code>mathbbI_resid = 0.2</code>이고, 그렇지 않으면 <code>mathbbI_resid = 1.0</code>이다. 이 지표는 대상 영역에 올바른 새 텍스트가 포함되는 동시에 원본 텍스트가 완전히 제거되도록 한다.

### (b) 고전적 지표(일반)

#### (i) CLIPScore

예측된 편집 이미지와 캡션 텍스트 사이의 의미적 정렬 정도를 측정하기 위해 CLIPScore [Hessel et al., 2021]를 사용한다. 먼저 Qwen3-VL을 사용해 레이블이 지정된 정답(GT) 이미지에 대한 간결한 캡션 텍스트를 생성하되, 그 길이가 CLIP 텍스트 인코더의 입력 제약을 충족하도록 한다. <code>mathbfv_img</code>는 예측된 편집 이미지의 CLIP 시각 임베딩을 나타내고, <code>mathbfv_text</code>는 생성된 캡션의 CLIP 텍스트 임베딩을 나타낸다고 하자. CLIPScore는 코사인 유사도로 계산한다.


<!-- source: sections/appendix.tex:101-104 -->

<pre class="equation">textCLIPScore = fracmathbfv_img cdot mathbfv_text|mathbfv_img| cdot |mathbfv_text|</pre>


CLIPScore가 높을수록 시각적 콘텐츠와 텍스트 설명 간의 의미적 일관성이 우수함을 나타내며, 편집된 텍스트가 장면 문맥에 성공적으로 통합되었음을 의미한다.

<!-- source: sections/appendix.tex:106-111 -->
#### (ii) 미적 점수

생성 이미지의 전반적인 시각적 매력을 평가하기 위해 CLIP 기반 미학 예측기를 사용한다. <code>f_textaes(cdot)</code>를 CLIP 이미지 임베딩을 미적 품질 점수로 매핑하는 미학 예측 모델이라고 하자.


<pre class="equation">textAesScore = f_textaes(mathbfv_img)</pre>


미적 점수의 범위는 일반적으로 1부터 5까지이며, 정규화한 경우에는 0부터 1까지이다. 값이 높을수록 시각적 품질, 구도 및 지각적 매력이 우수함을 나타낸다. 이 지표는 텍스트 편집으로 인해 이미지의 전반적인 품질이 저하되지 않았는지 확인하는 데 도움이 된다.

<!-- source: sections/appendix.tex:113-117 -->
### (c) MLLM 기반 지표

강력한 상용 MLLM(즉, Gemini-3-Pro-Preview)을 활용하여 <code>N=5</code>개 차원(<code>D_1</code>부터 <code>D_5</code>까지)에 걸친 전문가 수준의 포렌식 분석을 모사한다. 각 차원은 1점부터 5점까지의 리커트 척도로 평가하며, 점수가 높을수록 품질이 우수함을 나타낸다. 그런 다음 원시 점수를 다음과 같이 정규화하고 집계한다.

<!-- source: sections/appendix.tex:119-127 -->
#### (i) 대상 정확도(<code>D_1</code>)

이 차원은 편집 영역에서 대상 텍스트의 철자 정확성과 삭제 품질을 평가한다. MLLM은 다음 기준에 따라 <code>s_1 in [1, 5]</code>의 점수를 부여한다.

- 대상 텍스트의 철자가 정확하게 렌더링되었는지 여부
- 원본 소스 텍스트가 완전히 삭제되었는지 여부
- 새 텍스트의 시각적 선명도와 가독성

5점은 소스 텍스트의 잔여 아티팩트가 전혀 없는 완벽한 텍스트 교체를 의미한다.

<!-- source: sections/appendix.tex:129-136 -->
#### (ii) 텍스트 보존(<code>D_2</code>)

이 차원은 편집 대상이 아닌 배경 텍스트가 편집 작업의 영향을 받지 않고 온전히 유지되는지 평가한다. MLLM은 다음을 평가한다.

- 배경 텍스트가 빠짐없이 유지되었는지 여부
- 주변 텍스트에 의도하지 않은 변경이 없는지 여부
- 텍스트 레이아웃과 위치의 보존

점수 <code>s_2 in [1, 5]</code>는 모델이 원본 배경 텍스트 요소를 성공적으로 보존한 정도를 나타낸다.

<!-- source: sections/appendix.tex:138-145 -->
#### (iii) 장면 무결성(<code>D_3</code>)

이 차원은 배경의 기하 구조와 객체가 얼마나 안정적으로 유지되는지 측정하며, 편집 과정에서 발생한 구조적 왜곡이나 아티팩트가 있는지 확인한다. 평가 기준은 다음과 같다.

- 건축 요소, 객체 경계 및 공간적 관계의 보존
- 기하학적 왜곡이나 뒤틀림 효과가 없는지 여부
- 장면의 원근감과 깊이 단서의 유지

점수 <code>s_3 in [1, 5]</code>는 장면의 전반적인 구조가 얼마나 잘 유지되는지를 나타낸다.

<!-- source: sections/appendix.tex:147-150 -->
#### (iv) 국소 사실성(<code>D_4</code>)

이 차원은 편집 영역의 인페인팅 품질을 평가하며, 다음 사항에 중점을 둔다.

- 편집 영역과 원본 영역 사이 경계의 깔끔함과 이음새 없는 연결


<!-- source: sections/appendix.tex:151-154 -->
- 흐림, 잔상 또는 이음매 같은 눈에 띄는 아티팩트가 없음
- 새 텍스트가 바로 인접한 주변 영역과 자연스럽게 통합됨

점수 <code>s_4 in [1, 5]</code>는 국소 편집 영역의 포토리얼리스틱 품질을 나타낸다.

<!-- source: sections/appendix.tex:156-163 -->
#### (v) 시각적 일관성(<code>D_5</code>)

이 차원은 글꼴 스타일, 조명 및 텍스처가 원본 장면의 문맥과 얼마나 조화를 이루는지 평가한다. MLLM은 다음을 평가한다.

- 주변 텍스트 또는 장면의 미학과 글꼴 스타일이 일관되는지 여부
- 조명의 방향, 강도 및 색온도가 일치하는지 여부
- 그림자 투영 및 텍스처 패턴이 배경과 자연스럽게 어우러지는지 여부

점수 <code>s_5 in [1, 5]</code>는 편집된 텍스트가 이미지의 전반적인 시각적 스타일에 얼마나 잘 통합되는지를 측정한다.

<!-- source: sections/appendix.tex:165-177 -->
#### (vi) 점수 정규화 및 컷오프 메커니즘

각 차원 <code>i</code>의 원시 리커트 점수 <code>s_i in [1, 5]</code>는 먼저 다음 매핑을 사용하여 <code>s&#x27;_i in [0, 1]</code>로 정규화한다: <code>s&#x27;_i = (s_i - 1) / 4</code>. 평가의 타당성을 보장하기 위해 **컷오프 메커니즘**을 구현한다. 즉, 주된 편집 과제(대상 텍스트 정확도, <code>D_1</code>)에서 현저히 실패하면(즉, <code>s_1 &lt; 4</code>), 텍스트 편집 실패 시 다른 품질 평가가 무의미해지므로 부차적 차원의 점수를 0으로 감점한다. 최종 가중 점수 <code>V_score</code>는 다음과 같이 정의한다.


<pre class="equation">V_score = w_1 s&#x27;_1 + mathbbI_(s_1 ge 4) cdot sum_i=2^5 w_i s&#x27;_i</pre>


이 식에서 각 기호의 의미는 다음과 같다.

- <code>s&#x27;_i</code>는 <code>i</code>번째 차원의 정규화 점수를 나타낸다.
- <code>w_i</code>는 <code>i</code>번째 차원에 부여한 가중치이며, <code>sum_i=1^5 w_i = 1</code>을 만족한다. 기본적으로 <code>w_1 = 0.4</code>, <code>w_2 = 0.3</code>, <code>w_3 = 0.1</code>, <code>w_4 = 0.1</code>, <code>w_5 = 0.1</code>을 사용한다.
- <code>s_1</code>은 주된 텍스트 정확도 차원의 원시 점수이다.
- <code>mathbbI_(s_1 ge 4)</code>는 조건 <code>s_1 ge 4</code>가 충족되면 1, 그렇지 않으면 0이 되는 지시 함수이다. 따라서 텍스트 내용이 부정확하면(점수 <code>&lt;4</code>) 배경의 시각적 품질(<code>D_2</code>부터 <code>D_5</code>까지의 차원)은 최종 점수에 기여하지 않는다.

<!-- source: sections/appendix.tex:179-185 -->
#### (vii) MLLM 전체 평균

전체 MLLM 기반 지표는 컷오프 메커니즘을 적용한 다섯 차원의 가중 평균으로 다음과 같이 정의한다.


<pre class="equation">textMLLM Overall Avg = V_score = w_1 s&#x27;_1 + mathbbI_(s_1 ge 4) cdot sum_i=2^5 w_i s&#x27;_i</pre>


이 종합 지표는 주된 텍스트 편집의 성공 여부와 부차적인 시각적 품질 요인을 모두 포착하는 하나의 스칼라 값을 제공하며, 근본적인 편집 실패에는 적절한 페널티를 부여한다. 장면 유형별 성능을 세밀하게 분석할 수 있도록 이 지표는 벤치마크의 **Virtual**(합성 장면, 범주 1.x.x) 하위 집합과 **Real**(실세계 장면, 범주 2.x) 하위 집합에 대해 각각 계산한다.

<!-- source: sections/appendix.tex:187-212 -->
**그림. T2I 과제용 시스템 프롬프트**

“`text
You are an expert Forensic Image Analyst and Design QA Specialist.

Your task is to evaluate the quality of an AI-edited image by comparing three images.

Images Provided (in order):
1. Original Image: The unedited source image containing the text "{raw_text}".
2. Ground Truth Image: A human-created reference showing the ideal result with text "{target_text}".
3. Edited Image: The AI-generated result to be evaluated.

Editing Task Information:
- Text to Remove: "{raw_text}"
- Text to Add: "{target_text}"

EVALUATION RUBRIC (1-5 SCORING SYSTEM)

Please evaluate the Edited Image based on the following 5 dimensions. Use the strict criteria below to assign a score from 1 to 5.
“`

<!-- source: sections/appendix.tex:214-226 -->
**텍스트 정확도**

**Q1. [대상 텍스트 정확도]**

*중점: `{target_text}`의 철자, 삭제의 정확성 및 가독성.*

- **5 (완벽함)**: 철자가 정확히 일치한다(대소문자 구분). 이전 텍스트가 완전히 삭제되었다. 잔상이 없다.
- **4 (사소한 결함)**: 텍스트는 정확하지만 문자 오류/오타가 1개 있거나, 대소문자 문제가 경미하거나, 자세히 살펴보아야만 보이는 극히 희미한 잔상이 있다.
- **3 (읽을 수 있으나 결함 있음)**: 문자 오류가 2--3개 있지만 단어를 알아볼 수 있다. 또는 이전 텍스트의 잔상/흔적이 눈에 띄어 깔끔함을 해친다.
- **2 (중대한 오류)**: 문자 오류가 3개를 초과한다(철자가 크게 틀림). 또는 이전 텍스트가 여전히 명확히 읽힌다(삭제 실패).
- **1 (실패)**: 텍스트가 누락되었거나, 무의미한 문자열이거나, 완전히 잘못된 단어이다. 이전 텍스트가 온전히 남아 있다.

<!-- source: sections/appendix.tex:228-240 -->
**텍스트 보존**

**Q2. [비대상 텍스트 보존]**

*중점: 편집 대상 이외의 배경 텍스트가 보존되고 읽을 수 있는지 여부.*

- **5 (완벽함)**: 모든 비대상 텍스트가 100% 보존되어 읽을 수 있으며 원본/GT와 동일하다.
- **4 (양호함)**: 주요 배경 텍스트가 보존되었다. 멀리 있는 부차적인 텍스트가 약간 부드러워지거나 흐려졌지만 여전히 읽을 수 있다.
- **3 (보통)**: 부차적인 텍스트 요소 한두 개가 흐려지거나 손상되거나 누락되었다.
- **2 (미흡함)**: 대상에 바로 인접한 핵심 텍스트가 손상, 삭제 또는 환각되었다.
- **1 (파괴적임)**: 배경 텍스트가 광범위하게 파괴되거나 환각되었다.

<!-- source: sections/appendix.tex:242-254 -->
**장면 무결성**

**Q3. [전역 장면 무결성]**

*중점: 편집하지 않은 영역(배경, 객체, 사람)의 기하학적 안정성.*

- **5 (완벽함)**: 배경의 기하 구조가 픽셀 단위로 완벽하게 보존되었다. 왜곡이 없다.
- **4 (양호함)**: 거의 완벽하지만 배경의 선이나 원근에 매우 미세한 이동(<code>&lt;1%</code>)이 있다.
- **3 (눈에 띔)**: 직선에 눈에 띄는 왜곡(물결 모양)이 있거나 객체/얼굴이 약간 뒤틀렸다.
- **2 (심각함)**: 구조가 크게 손상되었다(예: 사람의 얼굴이 녹아내리거나 건물이 무너짐).
- **1 (혼돈)**: 원본과 비교해 장면 구조가 완전히 바뀌었거나 이치에 맞지 않는다.

<!-- source: sections/appendix.tex:256-268 -->
**국소 사실성**

**Q4. [국소 사실성 및 아티팩트]**

*중점: 인페인팅 품질, 가장자리의 깔끔함 및 편집 영역 주변의 매끄러운 연결.*

- **5 (탁월함)**: 편집 흔적이 보이지 않는다. 가장자리가 깔끔하고 후광이나 얼룩이 없다. 전문가 수준의 품질이다.
- **4 (양호함)**: 매우 사소한 아티팩트(예: 확대했을 때 약간의 픽셀화)가 있지만, 언뜻 보기에는 자연스럽다.
- **3 (보통)**: 이음매, 흐릿한 직사각형 패치 또는 텍스트 주변의 "문질러 번진 듯한" 모습이 눈에 띈다.
- **2 (미흡함)**: 명백한 아티팩트, 지저분한 가장자리 또는 흰색/검은색 상자 아티팩트가 있다.
- **1 (폐기물 수준)**: 편집 영역이 손상된 파일이나 순수 노이즈처럼 보인다.

<!-- source: sections/appendix.tex:269-271 -->
**그림 28. MLLM 기반 자동 평가에 사용한 시스템 프롬프트 템플릿.**

<figure data-figure="28"><img src="source/figures/generated/figure28_prompt.png" alt="그림 28"></figure> 분석가 페르소나, 과제 정의 및 처음 네 가지 점수 차원(Q1--Q4)을 다룬다.  
<span id="fig:eval_prompt_part1"></span>

<!-- source: sections/appendix.tex:273-286 -->
**시각적 일관성**

**Q5. [미학 및 조명의 조화]**

*중점: 스타일(글꼴), 조명, 그림자 및 텍스처의 조화로운 일치.*

- **5 (매끄러움)**: 글꼴 스타일이 GT/문맥과 완벽히 일치한다. 조명/그림자가 물리적으로 정확하다. 텍스처(입자감)가 사진과 일치한다.
- **4 (통합됨)**: 스타일이 잘 일치한다. 조명이 대부분 정확하다. 텍스처가 약간 지나치게 매끄럽지만 허용할 만하다.
- **3 (인위적임)**: 텍스트가 "붙여 넣은" 것처럼 보인다(디지털 스티커 같은 모습). 글꼴 스타일이 일반적이며(예: Arial) 장면과 어울리지 않는다.
- **2 (부조화)**: 색상이나 원근이 잘못되었거나, 필요한 곳에 음영이 없다.
- **1 (불일치)**: 텍스트가 어색하게 떠 있으며 장면의 물리 법칙과 스타일을 완전히 무시한다.

<!-- source: sections/appendix.tex:289-300 -->
**최종 출력 형식**

### 최종 출력 형식(JSON만 허용)

두 개의 딕셔너리 `score`(정수)와 `reason`(문자열)을 포함하는 유효한 JSON 객체를 출력해야 한다.

**출력 예시:**

**지시:** *"텍스트 'MUSIC'을 'PARTY'로 바꾸시오."*


<!-- source: sections/appendix.tex:301-337 -->

“`json
{
  "score": {
    "Q1": 5,
    "Q2": 1,
    "Q3": 2,
    "Q4": 5,
    "Q5": 4
  },
  "reason": {
    "Q1": "대상 텍스트 'PARTY'의 철자가 정확하고 명확하게 읽힌다. 제거하도록 지정된 대상 텍스트('MUSIC')는 잔상 없이 완전히 사라졌다.",
    "Q2": "모델이 대상이 아닌 텍스트를 광범위하게 훼손했다. 'NIGHT CLUB', '31 OCT', 'FREE DRINKS', 'LIVE', 'PRICE'가 모두 잘못 삭제되었으며, '10$'는 환각으로 생성된 텍스트 '1TY'로 변형되었다.",
    "Q3": "전체 장면의 무결성이 심각하게 훼손되었다. 마라카스를 들고 있던 해골의 팔이 지워져 마라카스가 공중에 떠 있는 모습이 되었으며, 이로 인해 삽화의 물리적 논리가 무너졌다.",
    "Q4": "의미적 실패에도 불구하고 이미지의 기술적 품질은 매우 뛰어나다. 경계가 선명하고 배경 인페인팅이 매끄러우며, 눈에 띄는 픽셀 아티팩트나 흐림, 노이즈가 없다.",
    "Q5": "'PARTY'에 선택된 글꼴 스타일은 포스터의 손으로 그린 듯한 벡터 미학과 잘 어우러진다. 다만 색상은 원본 텍스트의 선명한 빨간색보다 더 어두운 적갈색이다."
  }
}
“`

<figure data-figure="29"><img src="source/figures/appendix/eval_example_vertical.pdf" alt="세로형 평가 예시"></figure>

JSON 블록 외부에는 어떠한 마크다운이나 대화형 텍스트도 출력하지 않는다.

<!-- source: sections/appendix.tex:339-341 -->

**그림: 평가 프롬프트의 후속 부분.** 마지막 평가 차원(Q5)과 결과 파싱에 필요한 엄격한 JSON 출력 스키마를 자세히 보여준다.

<!-- source: sections/appendix.tex:344-347 -->

### MiniSet-500 결과

오픈 소스 커뮤니티에 가볍고 표준화된 평가 하위 집합을 제공하기 위해 전체 TextEdit 벤치마크에서 **MiniSet-500**을 구축한다. 시나리오 유형 전반에 걸쳐 균형 잡힌 분포를 보장하도록 18개 하위 범주 각각에서 인스턴스를 무작위로 샘플링해 구성한다. MiniSet-500은 총 **500개의 이미지 편집 쌍**을 포함하며, 과제의 다양성은 유지하면서 평가 비용을 크게 줄인다. 이는 신속한 벤치마킹과 절제 연구를 위한 효율적인 프로토콜로 활용되며, 종합 평가에는 전체 벤치마크가 여전히 표준으로 사용된다. 표 `exp_textedit_rule_miniset`과 표 `miniset-textedit-mllm`에는 MiniSet-500 TextEdit 벤치마크에서 여러 모델이 보인 성능을 보고한다.

<!-- table source: tables/final/textedit-rule-miniset -->
<!-- table source: tables/final/textedit-mllm-miniset -->

<!-- source: sections/appendix.tex:349-350 -->

<div style="page-break-after: always;"></div>

## 데이터 구축 세부 사항


### 표 23. TextEdit MiniSet-500 — Classic Metrics

“A+B”는 이해(A)와 생성(B) 매개변수를 나타낸다. OA=OCR Accuracy, OP=OCR Precision, OR=OCR Recall, F1=OCR F1-Score, NED=ROI-Aware NED, CLIP=CLIPScore, AES=Aesthetic Score.

| Model | # Params | Real OA | OP | OR | F1 | NED | CLIP | AES | Virtual OA | OP | OR | F1 | NED | CLIP | AES |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen-Image-Edit | 20B | 0.76 | 0.69 | 0.67 | 0.67 | 0.70 | 0.75 | 5.81 | 0.74 | 0.71 | 0.70 | 0.70 | 0.70 | 0.80 | 5.27 |
| GPT-Image-1.5 | – | 0.72 | 0.68 | 0.66 | 0.67 | 0.67 | 0.75 | 5.85 | 0.68 | 0.69 | 0.68 | 0.68 | 0.65 | 0.80 | 5.32 |
| Nano Banana Pro | – | 0.76 | 0.71 | 0.69 | 0.70 | 0.70 | 0.75 | 5.86 | 0.77 | 0.76 | 0.75 | 0.75 | 0.76 | 0.81 | 5.32 |
| Lumina-DiMOO | 8B | 0.20 | 0.22 | 0.18 | 0.19 | 0.19 | 0.70 | 5.58 | 0.22 | 0.25 | 0.21 | 0.22 | 0.19 | 0.73 | 4.87 |
| Ovis-U1 | 2.4B+1.2B | 0.37 | 0.34 | 0.32 | 0.32 | 0.33 | 0.72 | 5.39 | 0.39 | 0.41 | 0.38 | 0.39 | 0.33 | 0.74 | 4.75 |
| BAGEL | 7B+7B | 0.61 | 0.59 | 0.52 | 0.54 | 0.54 | 0.74 | 5.79 | 0.53 | 0.58 | 0.53 | 0.55 | 0.51 | 0.78 | 5.25 |
| **InternVL-U** | **2B+1.7B** | **0.77** | **0.74** | **0.70** | **0.71** | **0.71** | **0.76** | **5.79** | **0.74** | **0.72** | **0.69** | **0.70** | **0.72** | **0.79** | **5.14** |

### 표 24. TextEdit MiniSet-500 — MLLM-based Metrics

TA=Target Accuracy, TP=Text Preservation, SI=Scene Integrity, LR=Local Realism, VC=Visual Coherence, Avg=MLLM Overall Average.

| Model | # Params | Real TA | TP | SI | LR | VC | Avg | Virtual TA | TP | SI | LR | VC | Avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen-Image-Edit | 20B | 0.93 | 0.85 | 0.77 | 0.55 | 0.78 | 0.80 | 0.60 | 0.82 | 0.91 | 0.81 | 0.74 | 0.76 |
| GPT-Image-1.5 | – | 0.97 | 0.94 | 0.86 | 0.79 | 0.92 | 0.91 | 0.85 | 0.93 | 0.95 | 0.92 | 0.83 | 0.88 |
| Nano Banana Pro | – | 0.96 | 0.95 | 0.85 | 0.86 | 0.92 | 0.91 | 0.87 | 0.92 | 0.96 | 0.93 | 0.87 | 0.92 |
| Lumina-DiMOO | 8B | 0.16 | 0.04 | 0.04 | 0.02 | 0.06 | 0.08 | 0.02 | 0.05 | 0.19 | 0.07 | 0.03 | 0.10 |
| Ovis-U1 | 2.4B+1.2B | 0.29 | 0.11 | 0.11 | 0.08 | 0.20 | 0.17 | 0.04 | 0.16 | 0.35 | 0.18 | 0.15 | 0.22 |
| BAGEL | 7B+7B | 0.68 | 0.61 | 0.38 | 0.34 | 0.59 | 0.53 | 0.36 | 0.52 | 0.69 | 0.64 | 0.40 | 0.54 |
| **InternVL-U** | **2B+1.7B** | **0.94** | **0.91** | **0.72** | **0.73** | **0.75** | **0.89** | **0.88** | **0.87** | **0.90** | **0.78** | **0.57** | **0.79** |


<!-- source: sections/appendix.tex:351-400 -->

이 절에서는 데이터 구축 과정의 세부 사항을 설명한다.

## 일반 과학 이미지 생성을 위한 필터링 세부 사항

2단계 필터링은 다음 차원을 기준으로 수행한다.

1. **이미지 유형:** 이미지를 MMMU [MMMU]에서 정의한 30개 이미지 유형 중 하나로 분류한다. 예를 들면 `Posters`, `Diagrams`, `Screenshots` 등이 있다. 생물학 분야의 `Microscopic_Images`나 모든 주제 분야의 `Tables`처럼, 주제에 따라 특정 이미지 유형을 제거한다.

2. **주제:** 이미지를 미리 정의된 주제 목록에 따라 분류하며, 문학, 미술, 디자인 등에 속하는 이미지는 대개 회화나 사진과 같은 자연 이미지이므로 제거한다.

3. **텍스트 길이:** 이미지 내 모든 텍스트를 추출한다. 텍스트가 200자를 초과하는 이미지는 제거한다.

4. **이미지 복잡도:** 구성 요소, 객체 및 텍스트의 개수와 복잡도를 고려하여 이미지가 그리기에 지나치게 복잡한지를 기준으로, 복잡도를 1점(매우 복잡함)부터 10점(매우 단순함)까지 평가한다. 주제별로 서로 다른 범위(예: 5~7점)를 설정하여 중간 수준의 복잡도를 가진 이미지를 선별한다.

5. **주제 지식 밀도:** 이미지 복잡도와 유사하게, 모델이 이미지를 생성하는 데 주제 지식과 추론을 얼마나 필요로 하는지에 따라 이미지를 1점(필요한 지식이 가장 적음)부터 10점(지식 밀도가 매우 높음)까지 평가한다. 각 주제에는 서로 다른 범위(예: 7~8점)를 적용한다.

## 화학 텍스트-이미지 데이터 합성

기존 데이터셋과 인터넷에서 수집하고 필터링한 일반 과학 텍스트-이미지 데이터에 더해, 화학 이미지용 대규모 복합 유기 화합물 데이터를 확보하기 위한 자동화 파이프라인도 설계했다. 초기 단계에서는 공개적으로 접근할 수 있는 권위 있는 화학 저장소인 PubChem에서 자동 수집 프로토콜을 통해 원시 항목 800,000개를 확보했다. 이 원시 코퍼스에는 고유 화합물 ID(CID), 화학 명명법에 따른 명칭, 분자식, SMILES 표현 및 2D 구조도와 같은 필수 물리화학적 기술 정보가 포함된다. 이어서 잘못되었거나 불완전한 항목을 제거하는 엄격한 필터링 메커니즘으로 데이터셋을 정제하여, 충실도가 높은 화학 인스턴스 600,000개로 구성된 선별 데이터셋을 구축했다. 두 번째 단계에서는 지시 이행 데이터 구축에 중점을 두었다. 화학명, SMILES 문자열 및 이에 대응하는 2D 시각화를 통합한 다양한 질의응답 템플릿을 수립하여, 화학 이미지 생성 과제에 특화된 시각-텍스트 질의응답 쌍 600,000개를 성공적으로 합성했다.

## 컴퓨터 과학 편집

각 과제의 정의는 다음과 같다.

1. **트리 토폴로지 편집 및 노드 조작:** 트리에 대해 완성(완전한 이진 트리로 완성), 삽입(특정 위치에 새 노드 삽입) 또는 가지치기(노드와 그 하위 트리 또는 특정 영역 내 노드 삭제)를 수행한다.

2. **트리 순회 시각화:** 전위, 중위 및 후위 순회를 포함하여 이진 트리의 순회 경로를 시각화하거나 순회 순서를 표시한다.

3. **이진 탐색 트리(BST) 연산:** BST에 노드를 삽입하거나, BST의 유효성을 검증하고 서로 뒤바뀐 노드를 수정한다.

4. **힙 연산 및 이중 뷰:** 힙에서 삽입 또는 루트 추출 연산을 1~3단계 수행하고 메모리 배열을 시각화한다. 위로 올리기(sift-up)와 아래로 내리기(sift-down) 과정을 포함해야 한다.

5. **허프만 부호화 트리:** 문자 빈도가 주어지면 허프만 부호화 트리를 구축하거나 노드 병합을 수행한다.

6. **트리 최소 공통 조상(LCA) 및 경로 강조:** 두 노드가 주어지면 최소 공통 조상을 강조하거나 두 노드를 잇는 경로를 그린다.

7. **그래프 <code>k</code>-홉 이웃:** 중심 노드가 주어지면 거리가 정확히 <code>k</code>인 모든 노드를 시각적으로 표시한다.

8. **그래프 차수 식별:** 차수가 특정 값과 같은 모든 노드를 식별하고 상자로 표시한다.

9. **그래프 사이클 검출:** 그래프에서 유일한 단순 사이클을 표시한다.

10. **이분 그래프 색칠:** 인접 노드가 서로 다른 색이어야 한다는 제약 아래, 색칠되지 않은 이분 그래프를 두 가지 색으로 칠한다.


<!-- source: sections/appendix.tex:401-414 -->
11. **그래프 최단 경로:** 시작 노드와 종료 노드가 주어지면 두 노드를 잇는 최단 경로를 그린다.

12. **유향 그래프 도달 가능성:** 유향 그래프에서 출발 노드로부터 순방향으로 도달 가능한 모든 하류 노드의 집합을 상자로 표시한다.

13. **FSM 문자열 추적:** 입력 문자열이 주어지면 FSM의 전체 상태 전이 경로를 그린다.

14. **FSM 상태 역할 식별:** FSM의 시작 상태와 수락 상태를 식별하여 색칠한다.

15. **FSM 전이 논리 완성:** 불완전한 FSM에서 누락된 화살표 간선과 그 입력 레이블을 완성한다.

<!-- source: sections/appendix.tex:417-435 -->
## 입체기하

각 과제의 구현 방식은 다음과 같다.

1. **회전체:** 먼저 GeoGebra를 사용하여 회전축을 *x*, *y*, *z*축 중 하나로 매개변수화한 다양한 3차원 회전체를 구성한다. *z*축을 예로 들면, 한 변이 회전축 위에 놓이는 평면 다각형을 *xoz* 평면에 생성한다. 구체적으로 *y*좌표를 0으로 고정하고, 단조 증가하는 정수 *z*좌표를 갖는 꼭짓점들의 수열을 표본 추출한다. *x*좌표는 모두 엄격하게 양수(다각형이 양의 *x* 반축에 놓임)이거나 모두 엄격하게 음수(다각형이 음의 *x* 반축에 놓임)인 임의의 정수로 표본 추출한다. 첫 번째와 마지막 꼭짓점은 정확히 *z*축 위(*x* = 0)에 놓이도록 제약하여 다각형의 한 변이 회전축과 일치하게 한다. 다각형의 꼭짓점 수는 [3, 6] 범위에서 무작위로 선택한다. 이후 이 다각형은 생성 곡선(자오선) 역할을 하며, 지정된 축을 중심으로 회전할 때 회전면을 정의한다.

2. **평면대칭:** 평면대칭 역시 GeoGebra로 구현한다. 시각적으로 보기 좋은 배치를 유지하기 위해 대칭면이 *xoy* 평면에 수직이 되도록 제한하고, 반사하기 전에 원래 입체가 이 평면의 한쪽에 완전히 놓이도록 한다. 데이터셋의 다양성을 높이기 위해 정각기둥, 정각뿔, 원기둥, 원뿔, 구를 비롯한 여러 구성 가능한 기하 기본도형을 지원한다. 각기둥과 각뿔의 경우 정다각형 밑면의 변 수를 [3, 6] 범위에서 표본 추출하며, 변의 길이도 설정할 수 있다. 또한 입체의 색상과 대칭면의 색상을 모두 매개변수화하여, 기하학적 명료성과 시각적 심미성을 유지하면서도 다양한 외형의 샘플을 생성할 수 있다.

3. **점대칭:** 점대칭의 경우 GeoGebra와 matplotlib에 각각 기반한 두 개의 병렬 샘플 생성 파이프라인을 구현한다. 두 파이프라인 모두에서 기하 기본도형의 유형(예: 각기둥, 각뿔, 원기둥, 원뿔, 구)과 색상을 무작위로 설정할 수 있어 매우 다양한 외형의 인스턴스를 생성할 수 있다. 데이터셋의 다양성을 한층 더 높이기 위해 각 기본 입체에 무작위 초기 회전을 적용하고 샘플마다 카메라 시점을 달리할 수 있게 한다.

4. **입체 평행이동:** 평행이동 과제는 matplotlib 기반 렌더링 파이프라인으로 구현하며, 3차원 입체의 유형과 색상을 모두 설정할 수 있다. 시각적 결과를 심미적이면서도 제어 가능하게 유지하기 위해 평행이동 벡터를 *x*축, *y*축, *z*축을 따르는 세 가지 표준 구성으로 제한한다. 각 샘플의 평행이동 크기는 [4, 10] 범위의 정수로 무작위 선택한다. 이는 원래 입체와 평행이동된 입체의 상대적 위치에 충분한 변화를 부여하면서도 두 입체가 동일한 뷰 안에서 모두 선명하게 보이도록 한다.

5. **입체 투영:** 투영 과제는 matplotlib로 구현하며, 3차원 입체의 유형과 색상을 무작위로 표본 추출한다. 먼저 축 정렬로 인한 퇴화를 피하기 위해 각 입체를 설정 가능한 각도만큼 회전한 다음, *xoy* 평면에 직교 투영한다.


# 참고문헌 요약

원문 참고문헌 340개의 제목을 원문 표기로 유지했다.

1. Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (2017).
2. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (2022).
3. Learning to reason with LLMs (2024).
4. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement
                  Learning (2025).
5. Language Models are Few-Shot Learners (2020).
6. Transformers Learn to Achieve Second-Order Convergence Rates for In-Context
                  Linear Regression (2024).
7. Can Looped Transformers Learn to Implement Multi-step Gradient Descent
                  for In-context Learning? (2024).
8. Transformers Learn to Implement Multi-step Gradient Descent with Chain
                  of Thought (2025).
9. Transformers as Statisticians: Provable In-Context Learning with In-Context
                  Algorithm Selection (2023).
10. Meta-Learning in Neural Networks: A Survey (2022).
11. Evolutionary principles in self-referential learning, or on learning
                  how to learn: The meta-meta-. hook (1987).
12. Learning to learn by gradient descent by gradient descent (2016).
13. Optimization as a Model for Few-Shot Learning (2017).
14. Attention is All you Need (2017).
15. Improving language understanding by generative pre-training (2018).
16. Universal Language Model Fine-tuning for Text Classification (2018).
17. BERT: Pre-training of Deep Bidirectional Transformers for Language
                  Understanding (2019).
18. Playing Atari with Deep Reinforcement Learning (2013).
19. Training language models to follow instructions with human feedback (2022).
20. Looped Transformers as Programmable Computers (2023).
21. On the reciprocal of the general algebraic matrix (1920).
22. Application of calculus of matrices to method of least squares: with special reference to geodetic calculations (1951).
23. A generalized inverse for matrices (1955).
24. Approximations by superpositions of a sigmoidal function (1989).
25. Approximation capabilities of multilayer feedforward networks (1991).
26. A List of Writings Relating to the Method of Least Squares: With Historical and Critical Notes (1877).
27. Direct Preference Optimization: Your Language Model is Secretly a
                  Reward Model (2023).
28. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open
                  Language Models (2024).
29. Back to Basics: Revisiting REINFORCE-Style Optimization for Learning
                  from Human Feedback in LLMs (2024).
30. Proximal Policy Optimization Algorithms (2017).
31. Meta-Dataset: A Dataset of Datasets for Learning to Learn from Few
                  Examples (2020).
32. Learning a Universal Template for Few-shot Dataset Generalization (2021).
33. All Roads Lead to Likelihood: The Value of Reinforcement Learning
                  in Fine-Tuning (2025).
34. Adaptive Task Sampling for Meta-learning (2020).
35. On sensitivity of meta-learning to support data (2021).
36. How to Train Your MAML to Excel in Few-Shot Classification (2022).
37. Task-Robust Model-Agnostic Meta-Learning (2020).
38. ST-MAML : A stochastic-task based method for task-heterogeneous
                  meta-learning (2022).
39. Meta-Learning With Differentiable Convex Optimization (2019).
40. How Does the Task Landscape Affect MAML Performance? (2022).
41. How to train your MAML (2019).
42. Qwen2.5 Technical Report (2024).
43. Open-Reasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model (2025).
44. Qwen2.5-Math Technical Report: Toward Mathematical Expert Model via
                  Self-Improvement (2024).
45. Let's Verify Step by Step (2024).
46. Are Your LLMs Capable of Stable Reasoning? (2024).
47. Scaling Relationship on Learning Mathematical Reasoning with Large
                  Language Models (2023).
48. Beyond Human Data: Scaling Self-Training for Problem-Solving with
                  Language Models (2024).
49. Automatic Combination of Sample Selection Strategies for Few-Shot
                  Learning (2024).
50. Light-R1: Curriculum SFT, DPO and RL for Long COT from Scratch
                  and Beyond (2025).
51. Iterative Preference Learning from Human Feedback: Bridging Theory
                  and Practice for RLHF under KL-constraint (2024).
52. Gemini 2.5: Our most intelligent AI model (2025).
53. Evaluating Large Language Models Trained on Code (2021).
54. GPQA: A Graduate-Level Google-Proof Q&A Benchmark (2023).
55. Speculative Thinking: Enhancing Small-Model Reasoning with Large Model Guidance at Inference Time (2025).
56. Towards Thinking-Optimal Scaling of Test-Time Compute for LLM Reasoning (2025).
57. Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification (2025).
58. A Survey of Efficient Reasoning for Large Reasoning Models: Language,
                  Multimodality, and Beyond (2025).
59. Reasoning Models Can Be Effective Without Thinking (2025).
60. MathCoder: Seamless Code Integration in LLMs for Enhanced Mathematical
                  Reasoning (2024).
61. Qwen2.5-Coder Technical Report (2024).
62. DeepSeek-Coder: When the Large Language Model Meets Programming -
                  The Rise of Code Intelligence (2024).
63. Measuring Mathematical Problem Solving With the MATH Dataset (2021).
64. Kimi k1.5: Scaling Reinforcement Learning with LLMs (2025).
65. LiveCodeBench: Holistic and Contamination Free Evaluation of Large
                  Language Models for Code (2024).
66. Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning
                  Large Language Models (2025).
67. Rethinking Reflection in Pre-Training (2025).
68. Route Sparse Autoencoder to Interpret Large Language Models (2025).
69. The Llama 3 Herd of Models (2024).
70. GPT-4 Technical Report (2023).
71. DeepSeek-V3 Technical Report (2024).
72. How Can We Know What Language Models Know (2020).
73. Towards Revealing the Mystery behind Chain of Thought: A Theoretical
                  Perspective (2023).
74. SFT or RL? An Early Investigation into Training R1-Like Reasoning Large Vision-Language Models (2025).
75. SFT Memorizes, RL Generalizes: A Comparative Study of Foundation
                  Model Post-training (2025).
76. A Survey on In-context Learning (2024).
77. Rethinking the Role of Demonstrations: What Makes In-Context Learning
                  Work? (2022).
78. Learning To Retrieve Prompts for In-Context Learning (2022).
79. MetaICL: Learning to Learn In Context (2022).
80. In-Context Learning with Long-Context Models: An In-Depth Exploration (2024).
81. Tree of Thoughts: Deliberate Problem Solving with Large Language Models (2023).
82. Graph of Thoughts: Solving Elaborate Problems with Large Language
                  Models (2024).
83. Open Thoughts (2025).
84. Sky-T1: Train your own O1 preview model within \$450 (2025).
85. LIMO: Less is More for Reasoning (2025).
86. NuminaMath 72B CoT (2024).
87. QwQ-32B: Embracing the Power of Reinforcement Learning (2025).
88. Are Transformers universal approximators of sequence-to-sequence functions? (2020).
89. What learning algorithm is in-context learning? Investigations with
                  linear models (2023).
90. In-context Learning and Induction Heads (2022).
91. An Explanation of In-context Learning as Implicit Bayesian Inference (2022).
92. Why Can GPT Learn In-Context? Language Models Secretly Perform Gradient Descent as Meta-Optimizers (2023).
93. On the Ability and Limitations of Transformers to Recognize Formal
                  Languages (2020).
94. Tighter Bounds on the Expressivity of Transformer Encoders (2023).
95. Universal Transformers (2019).
96. RNNs can generate bounded hierarchical languages with optimal memory (2020).
97. Transformers Learn Shortcuts to Automata (2023).
98. Saturated Transformers are Constant-Depth Threshold Circuits (2022).
99. Thinking Like Transformers (2021).
100. Self-Attention Networks Can Process Bounded Hierarchical Languages (2021).
101. O(n) Connections are Expressive Enough: Universal Approximability
                  of Sparse Transformers (2020).
102. On the optimization of a synaptic learning
rule (1992).
103. Learning to Learn: Introduction and Overview (1998).
104. Prototypical Networks for Few-shot Learning (2017).
105. One-shot Learning with Memory-Augmented Neural Networks (2016).
106. Bespoke-Stratos: The unreasonable effectiveness of reasoning distillation (2025).
107. s1: Simple test-time scaling (2025).
108. DAPO: An Open-Source LLM Reinforcement Learning System at Scale (2025).
109. VAPO: Efficient and Reliable Reinforcement Learning for Advanced Reasoning Tasks (2025).
110. Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? (2025).
111. Variational Metric Scaling for Metric-Based Meta-Learning (2020).
112. BlockMix: Meta Regularization and Self-Calibrated Inference for Metric-Based
                  Meta-Learning (2020).
113. Adversarial gradient-based meta learning with metric-based test (2023).
114. Memory Networks (2015).
115. End-To-End Memory Networks (2015).
116. Meta-Learning with Implicit Gradients (2019).
117. Multi-Objective Meta Learning (2021).
118. Meta-learning with an Adaptive Task Scheduler (2021).
119. Transformers Learn Higher-Order Optimization Methods for In-Context
                  Learning: A Study with Linear Models (2023).
120. A Survey on LLM Test-Time Compute via Search: Tasks, LLM Profiling,
                  Search Algorithms, and Relevant Frameworks (2025).
121. Atom of Thoughts for Markov LLM Test-Time Scaling (2025).
122. O1 Replication Journey: A Strategic Progress Report - Part 1 (2024).
123. Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking
                  Reasoning Systems (2024).
124. Qwen3: Think Deeper, Act Faster (2025).
125. GMMSampling: a new model-based, data difficulty-driven resampling
                  method for multi-class imbalanced data (2024).
126. Visualizing the Loss Landscape of Neural Nets (2018).
127. Llama-Nemotron: Efficient Reasoning Models (2025).
128. GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning (2025).
129. Learning to Optimize (2017).
130. Learning to Optimize Neural Nets (2017).
131. Learning to Optimize for Reinforcement Learning (2024).
132. A Simple Guard for Learned Optimizers (2022).
133. \(μ\)LO: Compute-Efficient Meta-Generalization of Learned Optimizers (2024).
134. A Closer Look at the Training Strategy for Modern Meta-Learning (2020).
135. HybridFlow: A Flexible and Efficient RLHF Framework (2025).
136. PyTorch: An Imperative Style, High-Performance Deep Learning Library (2019).
137. Transformers: State-of-the-Art Natural Language Processing (2020).
138. Efficient Memory Management for Large Language Model Serving with
                  PagedAttention (2023).
139. A Survey of Scientific Large Language Models: From Data Foundations to Agent Frontiers (2025).
140. Scientists' First Exam: Probing Cognitive Abilities of MLLM via Perception, Understanding, and Reasoning (2025).
141. GenExam: A Multidisciplinary Text-to-Image Exam (2025).
142. Probing Scientific General Intelligence of LLMs with Scientist-Aligned Workflows (2025).
143. Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi (2024).
144. SridBench: Benchmark of Scientific Research Illustration Drawing of Image Generation Model (2025).
145. Qwen3-VL Technical Report (2025).
146. Emerging Properties in Unified Multimodal Pretraining (2025).
147. TokensGen: Harnessing Condensed Tokens for Long Video Generation (2025).
148. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling (2024).
149. Gemini: a family of highly capable multimodal models (2023).
150. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context (2024).
151. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities (2025).
152. Gpt-4 technical report (2023).
153. How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites (2024).
154. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks (2024).
155. InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency (2025).
156. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models (2025).
157. Qwen2.5-VL Technical Report (2025).
158. Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution (2024).
159. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond (2023).
160. Visual Instruction Tuning (2023).
161. LLaVA-NeXT: Improved reasoning, OCR, and world knowledge (2024).
162. Improved Baselines with Visual Instruction Tuning (2023).
163. Qwen-Image Technical Report (2025).
164. PaddleOCR 3.0 Technical Report (2025).
165. Flux-text: A simple and advanced diffusion transformer baseline for scene text editing (2025).
166. AnyText: Multilingual Visual Text Generation And Editing (2023).
167. MemeMind: A Large-Scale Multimodal Dataset with Chain-of-Thought Reasoning for Harmful Meme Detection (2025).
168. Towards comprehensive detection of chinese harmful memes (2024).
169. What makes a meme a meme? identifying memes for memetics-aware dataset creation (2025).
170. Large Vision-Language Models for Knowledge-Grounded Data Annotation of Memes (2025).
171. Multi-Granular Multimodal Clue Fusion for Meme Understanding (2025).
172. Met-meme: A multimodal meme dataset rich in metaphors (2022).
173. Learning transferable visual models from natural language supervision (2021).
174. An image is worth 16x16 words: Transformers for image recognition at scale (2020).
175. Qwen3 technical report (2025).
176. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation (2022).
177. Llama: Open and efficient foundation language models (2023).
178. Internlm: A multilingual language model with progressively enhanced capabilities (2023).
179. Palm 2 technical report (2023).
180. Lisa: Reasoning segmentation via large language model (2024).
181. Mineru2. 5: A decoupled vision-language model for efficient high-resolution document parsing (2025).
182. Paddleocr-vl: Boosting multilingual document parsing via a 0.9 b ultra-compact vision-language model (2025).
183. High-resolution image synthesis with latent diffusion models (2022).
184. Instructpix2pix: Learning to follow image editing instructions (2023).
185. Adding conditional control to text-to-image diffusion models (2023).
186. Generative adversarial networks (2020).
187. A style-based generator architecture for generative adversarial networks (2019).
188. FLUX (2024).
189. Score-Based Generative Modeling through Stochastic Differential Equations (2021).
190. Denoising Diffusion Probabilistic Models (2020).
191. MM-Interleaved: Interleaved Image-Text Generative Modeling via Multi-modal Feature Synchronizer (2024).
192. Video-LLaVA: Learning United Visual Representation by Alignment Before Projection (2023).
193. VideoChat: Chat-Centric Video Understanding (2023).
194. Video-ChatGPT: Towards Detailed Video Understanding via Large Vision and Language Models (2024).
195. Vlm-r1: A stable and generalizable r1-style large vision-language model (2025).
196. R1-V: Reinforcing Super Generalization Ability in Vision-Language Models with Less Than \$3 (2025).
197. Vision Model Pre-training on Interleaved Image-Text Data via Latent Compression Learning (2024).
198. Flow Matching Guide and Code (2024).
199. Flow straight and fast: Learning to generate and transfer data with rectified flow (2022).
200. Visual autoregressive modeling: Scalable image generation via next-scale prediction (2024).
201. MaskGIT: Masked Generative Image Transformer (2022).
202. Zero-shot text-to-image generation (2021).
203. Taming transformers for high-resolution image synthesis (2021).
204. Neural discrete representation learning (2017).
205. HunyuanImage 3.0 Technical Report (2025).
206. Omnigen: Unified image generation (2024).
207. OmniGen2: Exploration to Advanced Multimodal Generation (2025).
208. FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space (2025).
209. Step1X-Edit: A Practical Framework for General Image Editing (2025).
210. FLUX.2: Frontier Visual Intelligence (2025).
211. Ovis-Image Technical Report (2025).
212. LongCat-Image Technical Report (2025).
213. Qwen-image technical report (2025).
214. Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion Transformer (2025).
215. Query-kontext: An unified multimodal model for image generation and editing (2025).
216. Sana: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformer (2024).
217. SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer (2025).
218. Dreamomni2: Multimodal instruction-based editing and generation (2025).
219. Onecat: Decoder-only auto-regressive model for unified understanding and generation (2025).
220. Janus-pro: Unified multimodal understanding and generation with data and model scaling (2025).
221. Show-o2: Improved Native Unified Multimodal Models (2025).
222. Lumina-dimoo: An omni diffusion large language model for multi-modal generation and understanding (2025).
223. Emu3. 5: Native multimodal models are world learners (2025).
224. Ovis-U1 Technical Report (2025).
225. Uniworld-v2: Reinforce image editing with diffusion negative-aware finetuning and mllm implicit feedback (2025).
226. Blip3-o: A family of fully open unified multimodal models-architecture, training and dataset (2025).
227. Blip3o-next: Next frontier of native image generation (2025).
228. Lavida-O: Elastic Large Masked Diffusion Models for Unified Multimodal Understanding and Generation (2025).
229. Mogao: An omni foundation model for interleaved multi-modal generation (2025).
230. Ming-univision: Joint image understanding and generation with a unified continuous tokenizer (2025).
231. MANZANO: ASIMPLE AND SCALABLE UNIFIED MUL-TIMODAL MODEL WITH A HYBRID VISION TOKENIZER ().
232. EMMA: Efficient Multimodal Understanding, Generation, and Editing with a Unified Architecture (2025).
233. MammothModa2: A Unified AR-Diffusion Framework for Multimodal Understanding and Generation (2025).
234. TUNA: Taming Unified Visual Representations for Native Unified Multimodal Models (2025).
235. UniGen-1.5: Enhancing Image Generation and Editing through Reward Unification in Reinforcement Learning (2025).
236. Unilip: Adapting clip for unified multimodal understanding, generation and editing (2025).
237. OpenUni: A Simple Baseline for Unified Multimodal Understanding and Generation (2025).
238. Skywork unipic: Unified autoregressive modeling for visual understanding and generation (2025).
239. Mono-internvl: Pushing the boundaries of monolithic multimodal large language models with endogenous visual pre-training (2024).
240. Mono-InternVL-1.5: Towards Cheaper and Faster Monolithic Multimodal Large Language Models (2025).
241. A diagram is worth a dozen images (2016).
242. Are you smarter than a sixth grader? textbook question answering for multimodal machine comprehension (2017).
243. Mv-math: Evaluating multimodal math reasoning in multi-visual contexts (2025).
244. Mavis: Mathematical visual instruction tuning (2024).
245. CMM-Math: A Chinese Multimodal Math Dataset To Evaluate and Enhance the Mathematics Reasoning of Large Multimodal Models (2024).
246. ChemEval: A Comprehensive Multi-Level Chemical Evaluation for Large Language Models (2024).
247. ChEBI in 2016: Improved services and an expanding collection of metabolites (2016).
248. ChemQA: a Multimodal Question-and-Answering Dataset on Chemistry Reasoning (2024).
249. GeoGebra: Dynamic Mathematics Software (2024).
250. InternSVG: Towards Unified SVG Tasks with Multimodal Large Language Models (2025).
251. Can large language models understand symbolic graphics programs? (2024).
252. Gemini 3 Flash: frontier intelligence built for speed (2025).
253. Gemini 3 Pro: Best for complex tasks and bringing creative concepts to life (2025).
254. GPT-5 System Card (2025).
255. PaddleOCR 3.0 Technical Report (2025).
256. Scaling rectified flow transformers for high-resolution image synthesis (2024).
257. Internvideo2. 5: Empowering video mllms with long and rich context modeling (2025).
258. Cambrian-s: Towards spatial supersensing in video (2025).
259. Kwai keye-vl 1.5 technical report (2025).
260. Seedream 4.0: Toward next-generation multimodal image generation (2025).
261. Mmada: Multimodal large diffusion language models (2025).
262. Chameleon: Mixed-modal early-fusion foundation models (2024).
263. Transfusion: Predict the next token and diffuse images with one multi-modal model (2024).
264. Synergen-vl: Towards synergistic image understanding and generation with vision experts and token folding (2025).
265. Show-o: One single transformer to unify multimodal understanding and generation (2024).
266. Vila-u: a unified foundation model integrating visual understanding and generation (2024).
267. Gemini\,3\,Pro Image Model Card (2025).
268. GPT-Image-1.5 (2025).
269. Emu3.5: Native Multimodal Models are World Learners (2025).
270. Objaverse: A universe of annotated 3d objects (2023).
271. SAM 3D: 3Dfy Anything in Images (2025).
272. Laion-5b: An open large-scale dataset for training next generation image-text models (2022).
273. Microsoft coco: Common objects in context (2014).
274. The open images dataset v4: Unified image classification, object detection, and visual relationship detection at scale (2020).
275. Segment anything (2023).
276. 15m multimodal facial image-text dataset (2024).
277. HumanVLM: Foundation for Human-Scene Vision-Language Model (2024).
278. Textpainter: Multimodal text image generation with visual-harmony and text-comprehension for poster design (2023).
279. AutoPoster: A Highly Automatic and Content-aware Design System for Advertising Poster Generation (2023).
280. A Large Chinese Text Dataset in the Wild (2019).
281. ABC: A Big CAD Model Dataset for Geometric Deep Learning. In 2019 IEEE (2018).
282. Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free (2025).
283. Mono-internvl-1.5: Towards cheaper and faster monolithic multimodal large language models (2025).
284. NaViL: Rethinking Scaling Properties of Native Multimodal Large Language Models under Data Constraints (2025).
285. X-omni: Reinforcement learning makes discrete autoregressive image generative models great again (2025).
286. Textcrafter: Accurately rendering multiple texts in complex visual scenes (2025).
287. Anytrans: Translate anytext in the image with large scale models (2024).
288. Mme: A comprehensive evaluation benchmark for multimodal large language models (2025).
289. OCRBench: On the Hidden Mystery of OCR in Large Multimodal Models (2023).
290. Geneval: An object-focused framework for evaluating text-to-image alignment (2023).
291. Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation models (2024).
292. Ella: Equip diffusion models with llm for enhanced semantic alignment (2024).
293. TIIF-Bench: How Does Your T2I Model Follow Your Instructions? (2025).
294. OneIG-Bench: Omni-dimensional Nuanced Evaluation for Image Generation (2025).
295. Wise: A world knowledge-informed semantic evaluation for text-to-image generation (2025).
296. Imgedit: A unified image editing dataset and benchmark (2025).
297. Seed-bench: Benchmarking multimodal llms with generative comprehension (2023).
298. Chartqa: A benchmark for question answering about charts with visual and logical reasoning (2022).
299. Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems? (2024).
300. Logicvista: Multimodal llm logical reasoning benchmark in visual contexts (2024).
301. Envisioning beyond the pixels: Benchmarking reasoning-informed visual editing (2025).
302. Image-to-image translation with conditional adversarial networks (2017).
303. Seedream 3.0 technical report (2025).
304. Uniworld: High-resolution semantic encoders for unified visual understanding and generation (2025).
305. Gpt-4o system card (2024).
306. Introducing our latest image generation model in the API (2025).
307. Introducing Gemini 2.5 Flash Image, our state-of-the-art image model (2025).
308. Janusflow: Harmonizing autoregression and rectified flow for unified multimodal understanding and generation (2025).
309. Transfer between modalities with metaqueries (2025).
310. Skywork unipic 2.0: Building kontext model with online rl for unified multimodal model (2025).
311. LightFusion: A Light-weighted, Double Fusion Framework for Unified Multimodal Understanding and Generation (2025).
312. Next-omni: Towards any-to-any omnimodal foundation models with discrete flow matching (2025).
313. Mammoth2: Scaling instructions from the web (2024).
314. Mmbench: Is your multi-modal model an all-around player? (2024).
315. Mm-vet: Evaluating large multimodal models for integrated capabilities (2023).
316. Mathvista: Evaluating math reasoning in visual contexts with gpt-4v, bard, and other large multimodal models (2023).
317. Measuring multimodal mathematical reasoning with math-vision dataset (2024).
318. Dynamath: A dynamic visual benchmark for evaluating mathematical reasoning robustness of vision language models (2024).
319. We-math: Does your large multimodal model achieve human-like mathematical reasoning? (2025).
320. ShareGPT-4o-Image: Aligning Multimodal Models with GPT-4o-Level Image Generation (2025).
321. Open-Sora Plan: Open-Source Large Video Generation Model (2024).
322. Echo-4o: Harnessing the Power of GPT-4o Synthetic Images for Improved Image Generation (2025).
323. OpenGPT-4o-Image: A Comprehensive Dataset for Advanced Image Generation and Editing (2025).
324. FLUX-Reason-6M & PRISM-Bench: A Million-Scale Text-to-Image Reasoning Dataset and Comprehensive Benchmark (2025).
325. AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea (2024).
326. Paint by Inpaint: Learning to Add Image Objects by Removing Them First (2024).
327. SEED-X: Multimodal Models with Unified Multi-granularity Comprehension and Generation (2024).
328. OmniEdit: Building Image Editing Generalist Models Through Specialist Supervision (2024).
329. UltraEdit: Instruction-based Fine-Grained Image Editing at Scale (2024).
330. HQ-Edit: A High-Quality Dataset for Instruction-based Image Editing (2024).
331. X2Edit: Revisiting Arbitrary-Instruction Image Editing through Self-Constructed Data and Task-Aware Representation Learning (2025).
332. NoHumansRequired: Autonomous High-Quality Image Editing Triplet Mining (2025).
333. Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing (2025).
334. GPT-IMAGE-EDIT-1.5M: A Million-Scale, GPT-Generated Image Dataset (2025).
335. Seedream 4.5 (2025).
336. Vlmevalkit: An open-source toolkit for evaluating large multi-modality models (2024).
337. Clipscore: A reference-free evaluation metric for image captioning (2021).
338. GenEditEvalKit ().
339. TextEdit ().
340. Implementation and benchmarking of perceptual image hash functions (2010).
