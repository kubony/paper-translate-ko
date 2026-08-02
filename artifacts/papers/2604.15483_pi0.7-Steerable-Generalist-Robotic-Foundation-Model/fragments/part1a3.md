[P1A3-001 | 원문 228–229행]

## 3. Flow 기반 Vision-Language-Action 모델

[P1A3-002 | 원문 231행]

VLA는 사전 학습된 vision-language model(VLM) backbone에서 출발하여 이를 로봇 제어에 맞게 조정하는 방식으로 학습한다. 학습 데이터셋 𝒟에는 관측 𝐨_t와 action 𝐚_t의 시퀀스인 로봇 trajectory가 포함된다. 관측 𝐨_t = [𝐈_t^1, …, 𝐈_t^n, 𝐪_t]는 n개의 카메라 이미지 𝐈_t^i와 로봇의 관절 구성 𝐪_t로 이루어지며, action 𝐚_t는 관절 또는 end-effector 명령으로 이루어진다.

[P1A3-003 | 원문 233–234행]

VLA는 일반적으로 최근 관측 이력 𝐨_{t−T:t}에 기반하여 미래 action의 짧은 trajectory 𝐚_{t:t+H}에 해당하는 *action chunk*를 예측하도록 학습한다(흔히 Ĥ < H인 더 짧은 horizon의 action을 실행한다). action chunk는 VLM backbone을 attend하는 더 작은 transformer인 “action expert”가 생성할 수 있으며, 이를 통해 runtime에 빠르게 inference할 수 있다. action expert는 일반적으로 로봇 action의 multi-modality를 포착하는 flow matching(또는 diffusion) objective를 사용한다. 효과적인 representation을 학습하기 위해 우리 모델은 knowledge insulation(KI) 학습 recipe도 사용한다. VLM backbone은 FAST token으로 supervision되며, action expert는 VLM backbone의 모든 activation을 attend하지만 action expert의 gradient는 VLM backbone으로 flow하지 않는다. 따라서 VLM은 비교적 안정적인 discrete cross-entropy loss를 통해 학습된다.

[P1A3-004 | 원문 236–238행]

관측과 action에 더해, VLA의 각 학습 예시에는 𝒞_t로 나타내는 *prompt* 또는 *context*가 함께 제공된다. 관례적으로 이는 사람 annotator가 제공한 언어 지시 ℓ_t(예: “주방을 정리하라”)에 해당하며, 따라서 𝒞_t = (ℓ_t)이다.

[P1A3-005 | 원문 240–245행]

π_{0.7}을 설계하면서, 각 학습 예시의 context에 추가한 정보가 어떻게 다양하고 이질적인 데이터셋(준최적 행동과 실패 포함)으로부터의 학습을 가능하게 하는지 탐구한다. 뒤에서 보이듯이, 이러한 데이터로 학습하면 모델의 robustness와 dexterity가 향상되며 모델이 더 폭넓게 generalize할 수 있다. VLA π_θ의 학습 objective는 다음과 같은 근사 log-likelihood에 해당한다.

**max_θ E_{𝒟}[log π_θ(𝐚_{t:t+H} | 𝐨_{t−T:t}, 𝒞_t)].**

[P1A3-006 | 원문 246행]

flow matching action expert는 closed-form log-likelihood가 아니라 근사 lower bound를 최적화한다는 점에 유의한다. 데이터셋 𝒟는 일반적으로 고품질 사람 demonstration trajectory로 구성된다. 그러나 앞서 언급했듯이, 우리는 실패한 episode와 준최적 autonomous rollout뿐 아니라 egocentric human video data와 같은 다른 data source도 포함하는 더 광범위한 데이터셋을 사용한다. 충분히 상세하고 유용한 context 𝒞_t를 사용하면 이처럼 다양한 데이터를 통합할 수 있으며, 다소 놀랍게도 더 나은 policy 성능과 generalization까지 얻을 수 있음을 보일 것이다.
