## 추론 비용

flow matching에 내재한 효율성을 활용하여, A2A policy가 달성할 수 있는 극단적인 추론 속도를 추가로 조사한다. 먼저 sampling step이 학습 성능에 미치는 영향을 평가한다. [[XREF:inference_cost]](왼쪽)에 나타난 것처럼, inference step 수를 늘리면 성공률이 빠르게 향상되지만 4 step을 넘어서면 한계 이득이 크게 감소한다. [[XREF:inference_cost]](가운데)와 관련하여, 추론 예산을 단 1 step으로 제한할 경우 성공률은 32 training epoch 이후 90%를 크게 넘어선다.

[[FIGURE:inference_cost]]

**추론 비용 테스트.** 설정: *Close Box*. **왼쪽:** 30 epoch으로 고정했을 때 inference step에 따른 성공률. **가운데:** 단 1-step inference에서 training epoch에 따른 성공률. **오른쪽:** 평가한 모든 모델의 sampling step당 평균 추론 시간으로, 공정성을 보장하기 위해 동일한 하드웨어에서 benchmark했다.

[[XREF:latent_space]]는 학습 중 one-step inference에서 latent space 표현이 수렴하는 과정을 시각화한다. history latent와 future action latent를 함께 embedding하기 위해 t-SNE를 사용하며, 학습된 flow를 나타내도록 쌍을 이루는 sample을 선으로 연결한다. 학습이 진행됨에 따라 history chunk와 future action chunk 사이의 평균 거리가 크게 감소했다. 또한 이 쌍들을 연결하는 trajectory가 점점 더 평행한 경로로 정렬된다. 이러한 현상은 history latent에서 future latent로의 single-step flow mapping이 실현 가능하다는 강력한 실증적 근거를 제공하며, 새롭게 나타나는 평행성은 학습된 flow의 직선성을 뒷받침한다.

또한 [[XREF:inference_cost]](오른쪽)에 나타낸 것처럼, 동일한 하드웨어(NVIDIA GeForce RTX 5090 GPU, 32GB VRAM)에서 다양한 알고리즘의 sampling step당 평균 추론 시간을 benchmark한다. sampling step을 극단적으로 압축할 수 있다는 점과 효율적인 MLP 기반 architecture 덕분에 A2A의 추론 latency는 1 ms 미만으로 유지된다. 특히 single-step inference 설정에서는 latency가 인상적인 0.56 ms에 이르며, 이는 고주파 의사결정이 필요한 task에 상당한 잠재력이 있음을 보여준다.

[[FIGURE:latent_space]]

**A2A 학습 중 latent space 표현의 수렴.** 설정: *Close Box*, one-step inference. history latent와 future action latent를 함께 embedding하기 위해 t-SNE를 적용하며, 쌍을 이루는 sample을 선으로 연결한다. 선의 색은 512차원 latent space에서 계산한 거리를 나타낸다.

A2A와 VITA [[CITE:gao2025vita]]는 regression 기반 ACT [[CITE:zhao2023learning]]보다 우수한 추론 속도를 보인다는 점에 주목한다. 이러한 효율성은 sampling epoch 수가 줄어든 것뿐만 아니라 latent space에서 순수 MLP 연산을 수행하는 데서도 비롯된다. 반대로 본 연구의 ACT는 self-attention 및 cross-attention mechanism을 갖춘 고비용 Transformer architecture를 사용한다.

서로 다른 4가지 randomization scene에서의 성공률 비교. 모든 모델은 Level 0에서 100개의 demonstration으로 200 epoch 동안 학습한다. 최고 결과는 **굵게** 표시하고, 두 번째로 좋은 결과는 <u>밑줄</u>로 표시한다.

[[TABLE:tab-generalization]]

| Methods | Level 0 (%) | Level 1 (%) | Level 2 (%) | Level 3 (%) |
|---|---:|---:|---:|---:|
| **A2A (1 step)** | **100** | <u>20</u> | <u>16</u> | <u>22</u> |
| **A2A (6 steps)** | **100** | **38** | **42** | **38** |
| VITA | **100** | 4 | 2 | 2 |
| FM-UNet | <u>96</u> | 6 | 6 | 4 |
| DDPM-UNet | 92 | 2 | 4 | 2 |
| Score-UNet | 94 | 0 | 2 | 0 |
| ACT | 86 | 8 | 2 | 0 |

## 일반화 성능
