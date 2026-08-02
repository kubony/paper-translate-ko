[P1B-001 | 원문 249–249행]
## 4. π0.7 개요

[P1B-002 | 원문 251–257행]
**그림 2. 아키텍처 개요.** π0.7 모델은 4B VLM backbone, `MEM` 스타일 video history encoder, 860M parameter action expert로 구성된 5B-parameter VLA이다. 모델의 context에는 언어 명령, 데이터 품질과 전략을 기술하는 episode metadata, subgoal image와 같은 multimodal input을 비롯한 서로 구별되는 여러 modality가 포함된다. 실행 시 언어 명령은 동일한 아키텍처에 기반한 high-level semantic policy가 생성하며, subgoal image는 BAGEL image generation model에 기반한 lightweight world model이 생성한다.

[P1B-003 | 원문 259–260행]
π0.7은 기존 π0.6의 VLA 아키텍처와 `MEM` memory system을 토대로 구축하고 이를 multi-modal context conditioning으로 확장한 최신 로봇 파운데이션 모델이다. 모델은 Gemma3 4B-parameter VLM으로 초기화한 VLM backbone과 860M parameter의 flow matching action expert로 구성되며, VLM backbone에는 400M-parameter vision encoder가 포함된다. 모델의 전체 parameter 수는 약 5B이다. Vision encoder 역시 Gemma3로 초기화하며 `MEM` video history encoder의 설계를 따른다. 즉, history observation에 temporal compression과 spatial compression을 모두 적용하고 history frame 수와 무관하게 고정된 수의 token을 출력한다. 모델 아키텍처의 개요는 그림 2에 제시하며, 아키텍처는 4장의 아키텍처 절에서 더 자세히 설명한다.

[P1B-004 | 원문 262–262행]
이전 모델인 π0, π0.5, π0.6은 task에 대한 짧은 텍스트 설명을 context로 사용한다. π0.7을 학습할 때는 context를 더 표현력 있는 언어 명령, episode metadata, subgoal image 등 추가 정보와 modality까지 포함하도록 확장하며, 이에 따라 다양하고 잠재적으로 suboptimal한 데이터로 학습할 수 있다.

[P1B-005 | 원문 265–266행]
## 5. Prompt 다양화

[P1B-006 | 원문 268–268행]
이 절에서는 π0.7이 사용하는 context Cₜ에 포함된 prompt의 각 부분을 설명한다. 모델은 각 component가 포함된 prompt를 처리하도록 학습하지만, 각 component를 무작위로 dropout하면서 학습하므로 어떤 subset도 처리할 수 있으며 test time에 유연성을 제공한다.

[P1B-007 | 원문 270–271행]
### 5.1 Subtask instruction

[P1B-008 | 원문 272–273행]
π0.5를 따라, 전체 텍스트 task 설명 ℓₜ(예: “주방을 청소하라”)에 더해 **다음 semantic subtask**를 포착하는 중간 단계의 더 high-level인 텍스트를 prompt의 일부로 포함한다. 이 중간 텍스트를 ℓ̂ₜ(예: “냉장고 문을 열어라”)로 나타낸다. inference 중 ℓ̂ₜ는 학습된 high-level policy 또는 사람이 생성할 수 있고 생략할 수도 있으며, 시간에 따라 바뀔 수 있다. 다양한 task와 scenario로부터 데이터를 수집한 다음, segment에 상세한 텍스트 설명을 annotation한다.

[P1B-009 | 원문 275–275행]
모델을 semantic subtask에 conditioning하면 모델을 단계별로 **말로 coaching**할 수도 있다. 모델은 다양한 언어 instruction을 따르도록 학습되므로, 예를 들어 고구마를 air fryer에 넣는 새로운 task에서 사람의 실시간 instruction을 따를 수 있다(그림 4 참조). Coaching 후에는 verbal coaching 데이터를 사용해 π0.7을 새로운 subtask instruction에 robot observation, task specification, 과거 subtask instruction의 history를 mapping하는 high-level policy로 finetuning할 수 있다(그림 2 왼쪽 아래). 그러면 이 high-level policy가 로봇을 안내해 task를 완전 자율적으로 수행하게 한다.

[P1B-010 | 원문 277–277행]
### 5.2 Subgoal image

[P1B-011 | 원문 279–279행]
Subtask instruction은 task의 high-level intent를 전달하는 데 효과적이지만 실행에 중요한 세부 사항이 부족할 수 있다. 예를 들어 “냉장고 문을 열어라”는 로봇 팔이 손잡이를 어떻게 잡아야 하는지 명시하지 않는다. Subgoal image는 장면에서 바라는 가까운 미래 상태를 image로 묘사하여 이 문제를 해결하며, task가 성공적으로 진행된 뒤 *세계가 어떤 모습이어야 하는지*를 더 풍부하게 명세한다.

[P1B-012 | 원문 281–281행]
**Multi-view subgoal** 𝐠ₜ = [Gₜ¹, …, Gₜⁿ]을 고려하며, 여기서 Gₜⁱ는 camera i에 대해 바라는 가까운 미래 image이다. Multi-view subgoal은 environment 및 object 중심 결과(대개 base view에서 가장 쉽게 확인 가능)와 arm/gripper 결과(대개 wrist view에서 가장 쉽게 확인 가능)를 동시에 명세하여 control을 위한 spatial grounding을 개선한다.

[P1B-013 | 원문 283–284행]
실행 시 subgoal image는 **lightweight world model**이 생성한다. 이 모델은 main model과 동일한 subtask instruction ℓ̂ₜ를 입력으로 받지만, web-scale video 및 image editing task에 대한 pre-training의 이점을 활용하므로 다양한 task와 scenario로 generalization할 수 있다. 로봇의 현재 observation에 grounding된 생성 subgoal image는 언어 instruction보다 policy의 objective를 더 명확하게 식별하는 경우가 많으며, 그 결과 언어 instruction 준수와 generalization이 향상된다. 이 모델을 gψ로 나타내며 다음 objective로 학습한다.

[P1B-014 | 원문 285–294행]
max_ψ E_{𝒟_g}[L_CFM(𝐠ₜ★, gψ(𝐨ₜ, ℓ̂ₜ, m))]

[P1B-015 | 원문 295–296행]
여기서 L_CFM은 표준 flow matching loss이고, 𝐠ₜ★는 미래 subgoal image이며, m은 episode metadata 절의 episode metadata이다. Dataset 𝒟_g는 subtask instruction 절의 segment 가운데 특히 고품질의 subtask label ℓ̂ₜ가 annotation된 subset이다. Segment 끝의 image frame을 ground-truth subgoal로 사용한다. 즉, 𝐠ₜ★ = 𝐨_{t_end}이다.

[P1B-016 | 원문 298–299행]
SuSIE를 따라, world model은 web-scale pre-training을 거친 off-the-shelf image generation 및 editing model을 사용해 초기화한다. Image understanding, editing, generation이 가능한 14B mixture-of-transformers model인 BAGEL로 초기화한다. World model 학습에 web data, egocentric human video와 같은 non-robot data source, 기타 video data를 추가하면 이러한 다른 data source에서 semantic concept과 physical concept을 습득한 뒤 subgoal image를 통해 π0.7로 transfer할 수 있다. 구현 세부 사항은 부록의 world model 구현 절에 제시한다.

[P1B-017 | 원문 302–308행]
**그림 3. Prompt 개요.** π0.7은 prompt에서 subtask instruction, subgoal image, episode metadata를 비롯한 다양한 context modality를 사용한다. 각 component에 dropout을 적용하여 모델을 학습한 다음, modality를 유연하게 조합하여 모델에 prompt를 제공한다. 예를 들어 UR5e bimanual manipulator로 셔츠를 접을 때는 subgoal image와 metadata prompting을 사용한다.

[P1B-018 | 원문 310–311행]
### 5.3 Episode metadata

[P1B-019 | 원문 313–313행]
모델에 제공하는 context를 확장하는 핵심 목표는 더 광범위하고 다양한 trajectory dataset으로 학습하는 것이다. π0.7은 고품질 demonstration data만 사용하는 대신 저품질 demonstration(실패 포함)은 물론 이전 모델의 autonomous data까지 활용한다. Test time에도 π0.7이 task를 최대한 잘 수행하기를 바라므로, 모델이 이러한 다양한 trajectory를 올바르게 contextualize할 수 있도록 task가 *어떻게* 수행되었는지에 관한 정보로 trajectory를 적절히 label해야 한다. 이를 위해 해당 training episode의 attribute를 담은 여러 “episode metadata” 정보를 context에 추가한다. Metadata의 집합을 m으로 나타내며, 여기에는 다음과 같은 다양한 label이 포함될 수 있다.

[P1B-020 | 원문 317–321행]
- **전체 속도(Overall speed):** timestep으로 측정한 episode 길이이다. 값을 500 step 간격으로 discretization한다. 즉, 1750에서 2250 사이의 값은 “2000 steps” bin으로 묶는다. 속도가 빠를수록 품질도 더 높은 경우가 많다. 예를 들어 episode에 실수가 더 적다.
- **전체 품질(Overall quality):** 1에서 5 사이의 score로 표현한 task 실행 품질이며, 5가 가장 높은 품질이다.
- **실수(Mistake):** 주어진 action segment 안에서 로봇이 실수했는지 나타내는 label이다(예: object grasp 실패 또는 잘못된 subtask 수행). 이 label은 사람이 데이터를 coarse하게 annotation하여 제공한다.

[P1B-021 | 원문 323–324행]
따라서 π0.7 모델은 다양한 data mixture에서 얻은 ground-truth episode speed와 episode quality 및 mistake segment에 대한 수동 annotation을 사용해 학습한다. 다양한 속도의 episode와 같은 데이터 다양성은 모델이 이러한 metadata와 target action의 상관관계를 학습하는 데 필요한 signal을 제공한다. 실행 시에는 metadata prompting을 통해 빠른 속도와 높은 품질로, 실수 없이 task를 수행하라고 모델에 instruction할 수 있다.

[P1B-022 | 원문 326–326행]
### 5.4 Control mode

[P1B-023 | 원문 328–328행]
Low-level action 실행에 서로 다른 control mode를 사용하는 것도 고려한다. 구체적으로 학습 중 **joint-level action과 end-effector action**을 모두 포함하고, prompt에서 control mode를 지정하기 위해 텍스트 identifier c ∈ {`joint`, `ee`}를 사용한다. 그러면 실행 시 task에 따라 control mode를 선택할 수 있다.

[P1B-024 | 원문 330–330행]
### 5.5 전체 prompt 및 학습 세부 사항

[P1B-025 | 원문 332–335행]
`<Multi-view observation><Multi-view subgoal> Task: 채소 껍질을 벗겨라. Subtask: peeler를 집어라. Speed: 8000. Quality: 5. Mistake: false. Control Mode: joint.<Proprioception>`

[P1B-026 | 원문 336–336행]
위 예시는 모든 context 정보를 결합하여 모델에 제공할 수 있는 하나의 prompt를 보여준다.

[P1B-027 | 원문 338–339행]
학습 중에는 prompt의 각 부분을 무작위로 dropout하며, 이에 따라 π0.7은 test time에 prompt component의 임의 subset을 사용할 수 있는 유연성을 갖는다(예: subgoal image를 사용하거나 사용하지 않고 실행). 먼저, subgoal image를 제공하면 모델 학습이 상당히 빨라진다는 사실을 확인했다. Action prediction task가 본질적으로 현재 frame과 미래 frame 사이의 robot action을 추론하는 “inverse dynamics” 문제가 되기 때문이다. 따라서 학습 중 각 batch의 example 중 25%에만 visual subgoal image를 추가한다. Subgoal image가 있는 example 중에서도 visual subgoal이 동등한 텍스트 subtask 설명을 더 풍부한 세부 정보로 대체할 수 있는 경우가 많으므로, subtask instruction ℓ̂ₜ를 30%의 확률로 dropout한다. Episode metadata는 15%의 확률로 전체를 dropout하며, 이에 더해 각 component(전체 속도, 전체 품질, mistake label)를 각각 5%의 확률로 dropout한다. Control mode에는 dropout을 적용하지 않는다.
