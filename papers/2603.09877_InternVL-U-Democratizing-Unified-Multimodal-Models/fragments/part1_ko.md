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

<!-- figure: fig:teaser2; src: sections/1.introduction.tex:L11-L18 -->
**그림 2. 공간 중심, 지각, 과학 중심, 유머 중심, 추론 중심 text-to-image 생성 또는 editing 과제에 대한 InternVL-U의 사례.** InternVL-U는 다양한 시각 도메인에 걸쳐 이러한 핵심 multimodal 능력을 보여준다.

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

### 3.1.2 Visual Generation Head

<!-- src: sections/3.methodology.tex:L66-L68 -->
제안한 원칙을 바탕으로 이 절에서는 그림 4에 나타낸 custom-developed visual generation head의 구현을 더 자세히 설명한다.

#### Context 및 Target Input을 위한 Dual Projector

<!-- src: sections/3.methodology.tex:L70-L70 -->
Multimodal hidden state(*context*)와 VAE image latent(*target*)의 feature distribution은 서로 크게 다르다. 이러한 이질성을 연결하기 위해 독립적인 linear projector를 사용하여 둘을 visual generation module의 conditioning space로 mapping한다. 특히 multimodal context embedding은 VAE latent보다 magnitude가 더 크고 outlier가 더 두드러지는 경향이 있음을 관찰한다. 이러한 scale mismatch를 줄이고 학습 안정성을 개선하기 위해 projection 전 VLM branch에 normalization layer를 추가하여 context feature의 variance를 명시적으로 1로 정규화한다.

#### Gated Attention을 적용한 Dual-Stream MMDiT Block

<!-- src: sections/3.methodology.tex:L72-L78 -->
Multimodal context와 generative target의 서로 다른 통계적 특성을 고려하기 위해 완전한 Dual-Stream architecture를 채택한다. 두 stream은 token-level dependency를 포착하기 위해 joint self-attention으로 상호작용하지만 QKVO projection과 Feed-Forward Network(FFN)에는 분리된 parameter를 사용한다. 또한 high-resolution, long-context 시나리오에서 non-linearity를 높이고 “attention-sink” 현상을 완화하기 위해 element-wise Gating Mechanism [qiu2025gated]을 attention block에 통합한다. 형식적으로 attention layer의 modulated output **O′**는 다음과 같다.

<!-- equation: eq-1; src: sections/3.methodology.tex:L75-L77 -->
**O′ = O ⊙ σ(XW_g)**

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

<!-- equation: eq-2; src: sections/3.methodology.tex:L94-L96 -->
**L_NTP = −(1/T) Σ_(t=1)^T log p_θ(x_t | x_<t, c)**

여기서 x_t는 길이 T인 text sequence의 t번째 token이고, x_<t는 preceding token이며, θ는 unified model을 parameterize한다. 이 objective는 MLLM backbone에 내재한 reasoning 및 instruction-following 능력을 모델이 유지하도록 보장한다.

#### Image Generation을 위한 Flow Matching

<!-- src: sections/3.methodology.tex:L100-L108 -->
Visual 구성 요소에는 image latent의 continuous distribution을 modeling하기 위해 velocity parameterization을 사용하는 Flow Matching 프레임워크를 채택한다. Noise ε을 예측하는 diffusion model과 달리, Gaussian noise distribution에서 data distribution으로 probability density를 운반하는 velocity vector field v_θ를 regression한다. Flow Matching에서 흔히 사용하는 formulation과 Optimal Transport에서 영감을 받은 transport path를 따라, noise **z₀ ∼ N(0, I)**와 ground-truth image latent **z₁** 사이의 표준 linear interpolation path를 가정한다. 시간 **t ∈ [0, 1]**에서 intermediate state는 **z_t = tz₁ + (1−t)z₀**로 정의한다. Objective는 predicted velocity와 target drift 사이의 mean squared error를 최소화하는 것이다.

<!-- equation: eq-3; src: sections/3.methodology.tex:L104-L106 -->
**L_FM = E_(t ∼ U[0,1], z₀ ∼ N(0,I), z₁ ∼ p_data) [ ‖v_θ(z_t, t, c) − (z₁ − z₀)‖² ]**

여기서 **v_θ(z_t, t, c)**는 context **c**를 조건으로 시간 **t**의 velocity vector를 예측하는 model output이고, **(z₁ − z₀)**는 linear trajectory를 따르는 ground-truth instantaneous velocity를 나타낸다.

#### Unified Training Objective

<!-- src: sections/3.methodology.tex:L110-L116 -->
최종 training objective는 discrete loss와 continuous loss의 weighted sum이다.

<!-- equation: eq-4; src: sections/3.methodology.tex:L112-L114 -->
**L_Total = α · L_NTP + β · L_FM**

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
