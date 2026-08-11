수신 2025년 10월 6일, 게재 승인 2025년 10월 14일, 출판일 2025년 10월 16일, 현 버전 발행일 2025년 10월 27일.

디지털 객체 식별자(DOI) 10.1109/ACCESS.2025.3622535

# 휠 로더를 위한 데이터 효율적 굴착력 추정

**ARMIN ABDOLMOHAMMADI, NAVID MOJAHED, SHIMA NAZARI, BAHRAM RAVANI**

미국 캘리포니아주 데이비스 95616, 캘리포니아 대학교 데이비스 캠퍼스 기계항공우주공학과

교신저자: Armin Abdolmohammadi (abdolmohammadi@ucdavis.edu)

본 연구는 Komatsu Ltd.의 부분 지원을 받았다.

## 초록

정확한 굴착력 예측은 토공 기계의 자율 운전을 구현하고 제어 전략을 최적화하는 데 매우 중요하다. 기존 접근법은 여러 토양 유형에 걸쳐 광범위한 데이터를 수집하거나 계산 비용이 큰 시뮬레이션을 수행해야 하는 경우가 많으며, 이는 확장성과 적응성을 제한한다. 본 연구는 직전 버킷 적재 사이클의 힘 측정값을 이용해 토양 parameter를 보정하는 데이터 효율적 프레임워크를 제시한다. 제안 방법은 fundamental earthmoving equation으로 정식화된 해석적 soil-tool interaction model을 기반으로 하며, 적재 단계에서 다단계 최적화 절차를 사용해 관련 토양 parameter를 식별한다. 이어서 추정된 parameter를 이용해 다음 사이클의 굴착력을 예측하므로, 대규모 데이터셋이나 machine learning model 훈련에 의존하지 않고도 시스템이 control input을 조정할 수 있다. 서로 다른 토양 유형과 굴착 궤적 조건에서 Algoryx Dynamics 엔진의 고충실도 시뮬레이션을 통해 프레임워크를 검증했으며, 10%에서 15% 사이의 root-mean-square 예측 오차를 달성했다. 이러한 사이클 간 적응은 휠 로더 작업에서 확장 가능한 온라인 힘 추정과 효율적인 경로 계획에 강한 잠재력이 있음을 보여준다.

**색인어—** 굴착력 추정, soil–tool interaction, 휠 로더 운용, fundamental earthmoving equation, 자율 굴착.

본 원고의 심사를 조정하고 게재를 승인한 associate editor는 Mostafa M. Fouda이다.

© 2025 저자. 본 연구는 Creative Commons Attribution 4.0 License에 따라 이용이 허가된다. 자세한 내용은 https://creativecommons.org/licenses/by/4.0/ 에서 확인할 수 있다.

# I. 서론

토공 기계의 자율 운전은 로봇공학, 자동화 및 제어 기술의 발전과 건설 산업의 심화되는 인력 부족으로 인해 현대 공학 및 연구에서 주목받는 분야이다 [1]. 휠 로더는 자율 기계의 한 형태로서, 다양한 환경에서 빈번하게 반복되는 적재 작업을 통해 재료를 운반하고 투하하는 데 널리 사용된다. 버킷 적재 단계는 에너지 수요가 최고에 이르는 구간이며, 토양의 변동성과 예측하기 어려운 tool-material interaction으로 인해 상당한 어려움을 초래한다 [2]. 이 단계의 에너지 사용을 최적화하면 휠 로더 작업의 효율을 크게 향상할 수 있다.

토양 속에서 버킷의 운동을 계획하고 제어할 수 있는 프레임워크를 구현하려면 굴착 중 버킷에 작용하는 힘을 정확히 추정하는 것이 필수적이다. 힘 추정 방법은 일반적으로 reactive 방식과 predictive 방식의 두 범주로 구분된다. Reactive 방식은 유압과 관절 운동 같은 센서 데이터로부터 inverse dynamics, observer 또는 data-driven model을 이용해 힘을 실시간으로 추정한다. 이러한 모델에는 실시간 센서 데이터로 훈련한 Radial Basis Function(RBF) neural network와 같은 순수 data-driven 접근법 [3], 그리고 Gaussian Process Regression을 rigid body dynamics 및 disturbance Kalman filter와 결합한 hybrid 방식 [4]이 포함된다. Inverse dynamics와 observer 설계를 이용하는 model-based 기법도 제안되어 왔다. 그러나 이러한 모델은 시스템 모델링 복잡성이 증가하는 대신 더 높은 안정성과 정밀도를 제공하며 [5], [6], feedback control에는 효과적이지만 task planning에는 적합하지 않다.

Predictive model은 geometry, 토양 및 운동 정보로부터 저항력을 추정하여 실행 전에 경로와 작업을 계획할 수 있게 한다. 이러한 모델링은 주로 시뮬레이션에서 Finite Element Analysis(FEA) 또는 Discrete Element Method(DEM) 등을 통해 수치적으로 수행할 수 있고 [7], [8], task planning과 control에 효과적인 더 빠른 추정을 위해 해석적으로 수행할 수도 있다. 해석 모델은 cutting tool 전방에 삼각형 파괴 영역이 형성된다고 가정하는 soil wedge theory와 같은 물리 메커니즘을 포함하여 굴착 저항력을 직접 추정한다. 이들 모델은 저항력을 토양 특성 및 tool geometry(예: rake angle, tool depth)와 연계한다 [9].

서로 다른 수준의 물리적 세부 묘사와 계산 복잡도로 이러한 저항 상호작용을 포착하기 위해 다양한 해석적 정식화가 개발되었다. Swick and Perumpral model [10]은 경계면 마찰, rake angle의 영향 및 가변 토양 깊이를 포함한다. Gill and Vanden Berg 정식화 [11]는 tool geometry, 속도 및 토양 변형을 고려한다. Hemami [12]는 토양 저항을 동적 arm control과 결합하여 해석 모델링을 robotic manipulator까지 확장하며, Hettiaratchi and Reece model [13]은 cutting force를 passive earth pressure 성분과 friction 성분으로 분해하여 토양 저항 추정을 개선하므로 특히 가변 깊이 시나리오에 적합하다.

[FIGURE 1. 제안 프레임워크의 개요: 사전 정의된 굴착 경로를 실행하고, 토양 parameter 최적화를 위해 버킷 궤적과 stockpile geometry를 기록한다. 추정된 parameter는 다음 굴착 사이클의 계획 및 제어에 활용된다.]

널리 채택된 또 다른 힘 모델은 Reece [14]가 처음 제안하고 이후 McKyes [15]가 단순화한 Fundamental Earthmoving Equation(FEE)이다. FEE는 다른 방법에 비해 단순하고 해석적으로 다루기 쉬우며 요구 입력이 적으므로 힘 예측 모델에서 널리 사용되고, control, parameter identification 및 embedded implementation에 매력적이다. 이 모델은 자동 굴착 제어 [16], 실시간 토양 parameter 추정 [17], [18], hybrid neural-physics resistance model [19], reinforcement learning 기반 controller [20], 휠 로더의 multibody simulation [21]을 비롯한 다양한 굴착 맥락에 적용되어 왔다. 이들 모델과 관련 모델에 대한 종합적인 검토는 [9]와 [22]에 제시되어 있다.

이러한 모든 해석적 힘 예측 모델은 cohesion, internal friction angle, adhesion 및 sinkage 특성과 같은 토양 parameter에 의존한다. 이러한 parameter는 일반적으로 현장 probe 시험(예: Cone Penetration Test(CPT), Pressuremeter Test(PMT), Dilatometer Test(DMT) [23]) 또는 통제된 실험실 시험 [24]과 같은 parameter identification 방법으로 얻는다. 이러한 절차는 건설 환경에서 비현실적이므로, 차량 탑재 센서를 사용하여 운전 중 parameter를 추론할 수 있는 on-machine 추정 방법이 등장했다.

On-machine parameter identification 방법 가운데 learning-based 접근법은 사전 데이터를 이용해 재료 유형을 분류하거나 토양 특성을 회귀하는 모델을 훈련한다. 그 예로는 proprioceptive force signal 분류 [25]와 kinematic 및 control 데이터로부터 특성을 추론하는 physics-informed neural network [26]가 있다. 이러한 방법은 효과적이지만 일반적으로 대규모의 labeled dataset과 상당한 offline training을 요구한다.

반면 non-learning-based 방법은 실시간 힘 측정값과 model-based optimization을 이용해 parameter를 직접 추정한다. Tan et al. [18]은 토양 밀도와 internal friction angle을 추정하기 위해 Newton-Raphson 방법을 적용했으며, 이후 Althoefer et al. [27]은 이를 추가 parameter까지 포함하도록 확장했다. Zhao et al. [28]은 parameter와 힘을 동시에 예측하기 위해 fuzzy logic을 향상된 FEE model과 통합하여 모델을 더욱 개선했다. 그러나 이러한 방법은 일부 값을 알려진 것으로 가정하여 추정하는 parameter 수를 제한하거나, 모든 parameter를 한 번에 추정하려 시도하여 수렴 문제와 계산 비효율에 취약한 고차원 최적화를 초래한다.

## A. 연구 공백과 기여

문헌에서는 세 가지 공백이 드러난다. 첫째 (1), learning-based 접근법은 광범위한 labeled dataset 또는 시뮬레이션을 필요로 하며, 여러 굴착 사이클에 걸쳐 집계한 parameter에 의존하는 경우가 많다 [19], [26]. 둘째 (2), non-learning-based model은 수렴을 저해하는 고차원 최적화의 문제를 겪는다. 셋째 (3), FEE 기반 모델은 삼각함수 특이점으로 인해 힘의 불연속이 나타나며, [29]와 같은 기존 해결책은 추가적인 계산 비용과 지형 민감도를 초래했다.

본 연구는 연속된 굴착 사이클 사이의 짧은 시간 간격 내에 실행되도록 설계된 데이터 효율적인 사이클 기반 parameter optimization 프레임워크를 제시하며, 이를 통해 변하는 토양 조건에 맞추어 작업을 적시에 조정할 수 있다. 공백 (1)을 해결하기 위해 non-learning-based 접근법을 채택하며, 경사진 지형을 고려하고 토양 다짐을 위한 Bekker의 load-sinkage theory [31]를 포함한 [30] 기반의 수정 FEE model을 사용한다. 공백 (2)를 해결하기 위해 parameter fitting 작업을 순차적인 하위 문제로 분해하는 다단계 최적화 전략을 제안하며, 이를 통해 parameter coupling을 줄이고 수렴성과 계산 효율을 향상한다. 마지막으로 공백 (3)을 해결하기 위해 failure surface geometry의 삼각함수 관계에서 유도한 연속성 제약조건을 failure surface 식별에 사용되는 최소화 절차에 직접 포함하여 힘의 불연속을 제거한다.

[TABLE 1. 본 연구에서 사용한 기호, parameter 및 변수 목록.

| 구분 | 기호 | 설명 | 단위 |
|---|---|---|---|
| Soil Parameters | γ | 토양 밀도 | kg/m³ |
| Soil Parameters | C | 토양 cohesion | N/m² |
| Soil Parameters | Cₐ | 토양과 버킷 사이의 adhesion coefficient | N/m² |
| Soil Parameters | φ | internal friction angle | rad |
| Soil Parameters | δ | external friction angle | rad |
| Soil Parameters | k_c | cohesive modulus of deformation | N/m^(n+1) |
| Soil Parameters | k_φ | frictional modulus of deformation | N/m^(n+2) |
| Soil Parameters | n | 토양 변형 지수 | — |
| FEE dimensionless coefficients | N_γ | 토양 단위중량에 대한 bearing capacity factor | — |
| FEE dimensionless coefficients | N_c | cohesion에 대한 bearing capacity factor | — |
| FEE dimensionless coefficients | N_a | adhesion에 대한 bearing capacity factor | — |
| FEE dimensionless coefficients | N_q | surcharge에 대한 bearing capacity factor | — |
| Environment Parameters | α | stockpile slope angle | rad |
| Environment Parameters | β | failure wedge angle | rad |
| Loader Parameters | w | 버킷 폭 | m |
| Loader Parameters | b | 버킷 두께 | m |
| Loader Parameters | W_b | 버킷 중량 | kg |
| Forces and Pressures | F_T | 버킷에 작용하는 tangential cutting force | N |
| Forces and Pressures | F_N | 버킷에 작용하는 normal force | N |
| Forces and Pressures | F_R | 버킷에 작용하는 resultant excavation force | N |
| Forces and Pressures | P | penetration pressure(Bekker load–sinkage model) | Pa |
| Parameter Sets | θ | 전체 토양 parameter vector, [γ, C, Cₐ, φ, δ, k_c, k_φ, n]ᵀ | — |
| Parameter Sets | θ₁ | Stage 1 parameter set, [Cₐ, δ, k_c, k_φ, n]ᵀ | — |
| Parameter Sets | θ₂ | Stage 2 parameter set, [γ, C, φ]ᵀ | — |
| Parameter Sets | θ₃ | Stage 3 parameter set, [k_c, k_φ, n]ᵀ | — |
]

이 프레임워크는 완전한 굴착 계획 및 제어 시스템에 통합되도록 설계되어, 휠 로더가 사이클마다 환경에 대한 인식을 자율적으로 개선할 수 있게 한다. Fig. 1과 같이 전체 과정은 로더에 탑재되었다고 가정한 perception system을 이용해 토양 더미의 초기 geometry를 포착하는 것으로 시작한다. 그런 다음 예비 굴착 사이클을 실행하며, 이 과정에서 kinematic model을 통해 버킷 궤적을 추적하고 로더의 hinge joint에 내장된 load cell로 굴착력을 측정한다. 수집된 궤적, 힘 데이터 및 토양 더미 geometry는 해석적 FEE model의 토양 parameter를 최적화하는 데 사용된다. 이어서 이러한 parameter를 사용해 저항력을 예측하고 다음 사이클의 굴착 전략을 정한다. 각 굴착 사이클 후 이 과정을 반복함으로써 시스템은 토양에 대한 이해를 지속적으로 개선한다. 본 논문은 이 전체 사이클 가운데 굴착력 추정에 초점을 둔다.

본 논문의 Section II에서는 해석적 토양 모델, bucket-soil interaction 및 힘 정식화를 포함하여 본 연구에서 사용한 방법론을 제시한다. Section III에서는 제안한 토양 parameter의 다단계 최적화를 설명한다. Section IV에서는 방법 구현을 통해 얻은 결과를 제시한다. Section V에서는 핵심 시사점과 향후 연구에 대한 함의를 제시한다.

# II. 방법론

본 절에서는 굴착 중 soil-tool interaction을 모델링하기 위한 프레임워크를 제시한다. 이 프레임워크의 토대는 수정된 FEE [15]이며, 물리적 정확성과 계산 효율 사이의 균형 때문에 이를 선택했다 [32]. 이어서 토양 다짐 효과를 고려하기 위해 Bekker의 load-sinkage 정식화 [31]를 포함하는 방법과 토양 failure surface geometry의 연속성을 강제하는 데 사용되는 삼각함수 유도를 상세히 설명한다.

## A. FUNDAMENTAL EARTHMOVING EQUATION(FEE)

FEE는 절삭 및 굴착 중 토양 저항력을 추정하기 위한 physics-based 프레임워크를 제공한다. Reece가 1964년에 처음 제안한 이 모델 [14]은 토양에 관입하는 cutting blade에 작용하는 힘을 설명하기 위해 토질역학 원리를 적용한다. 이후 McKyes는 직선 failure surface와 균일한 surcharge pressure를 가정하여 경운 장비에 작용하는 힘을 추정하는 trial wedges method를 사용해 이 프레임워크를 단순화했다 [15]. 그 후 FEE는 경사진 지형으로 확장되어 굴착기 [33]와 휠 로더 [30]의 구조 설계 및 하중 해석에 적용되었다. 더 최근에는 Yao가 model predictive 프레임워크에서 수정 FEE를 사용하여 버킷 적재 궤적을 최적화했다 [32]. 이 모델은 blade가 지형에 관입할 때 soil wedge에 작용하는 전체 저항력을 포착한다.

Blade가 토양에 관입한다고 가정하고, 굴착 경로를 시각 t = t_i의 N개 점으로 이산화하며, 여기서 i ∈ {1, ..., N}이다. 각 점에서 soil wedge의 free body diagram은 Fig. 2에 제시되어 있다. Stockpile 표면은 α의 각도로 기울어진 직선 OC로 나타내고, blade는 길이가 L_{t,i}이고 stockpile에 대한 각도가 ρ_i인 선분 AB로 모델링한다. Blade 끝단은 점 B이고, 선 BC로 표현되는 failure surface는 McKyes의 wedge theory [15]와 일관되게 직선이라고 가정한다.

[FIGURE 2. Blade 선분 A′B에 작용하는 soil wedge의 free body diagram으로, 특정 시점에 blade가 토양과 상호작용하는 순간을 나타낸다. 시간에 따라 변하며 t = t_i에서 포착된 모든 parameter는 아래첨자 i로 표기한다.]

Soil wedge에 작용하는 힘에는 external friction angle δ 방향으로 작용하는 blade와 wedge 사이의 순 frictional 및 normal force F_i, internal friction angle φ 방향으로 비교란 토양이 가하는 힘 R_i, failure surface를 따라 작용하는 cohesion force CwL_{f,i}, 그리고 blade를 따라 작용하는 adhesion force C_a wL_{t,i}가 포함된다. Blade가 전진함에 따라 L_{t,i}와 L_{f,i}는 모두 시간에 따라 변한다. 모든 토양, 환경 및 로더 parameter는 Table 1에 열거되어 있다.

C_a wL_{t,i}와 CwL_{f,i}는 blade와 토양의 geometry에서 유도할 수 있다. W_{load,i}는 [3]과 [5]에서 설명한 방법을 사용해 운전 중 추정한다. 힘 F_i와 R_i는 미지수이다. F_i를 계산하기 위해 평형 조건을 가정하고 x 및 z 방향으로 Newton의 힘 평형 방정식을 적용한다. 이들 방정식을 이용하면 F_i를 W_{load,i}, C_a wL_{t,i}, CwL_{f,i}의 함수로 나타낼 수 있으므로 미지의 힘 R_i를 제거할 수 있다. 그 결과 F_i는 다음과 같이 표현된다.

```text
F_i = d_i² wγgN_{γ,i} + Cwd_iN_{c,i}
      + C_a wd_iN_{a,i} + W_{load,i}N_{q,i}.                 (1)
```

여기서 d_i는 관입 깊이이며, 점 B에서 OC와 같은 stockpile 선까지의 거리로 구한다. N_{γ,i}, N_{c,i}, N_{a,i}, N_{q,i}는 다음과 같은 네 개의 bearing capacity factor이다.

```text
        (cot β_i − tan α)[cos α + sin α cot(β_i + φ)]
N_{γ,i} = -------------------------------------------------.  (2)
        2[cos(ρ_i + δ) + sin(ρ_i + δ) cot(β_i + φ)]
```

```text
                     1 + cot β_i cot(β_i + φ)
N_{c,i} = ------------------------------------------------.   (3)
          cos(ρ_i + δ) + sin(ρ_i + δ) cot(β_i + φ)
```

```text
                     1 − cot ρ_i cot(β_i + φ)
N_{a,i} = ------------------------------------------------.   (4)
          cos(ρ_i + δ) + sin(ρ_i + δ) cot(β_i + φ)
```

```text
                     cos α + sin α cot(β_i + φ)
N_{q,i} = ------------------------------------------------.   (5)
          cos(ρ_i + δ) + sin(ρ_i + δ) cot(β_i + φ)
```

이 무차원 계수들은 서로 다른 토양 특성이 cutting force에 미치는 영향을 나타낸다. Unit weight factor로 알려진 N_{γ,i}는 토양 중량이 전체 힘에 기여하는 정도를 나타낸다. Cohesion factor N_{c,i}는 토양 cohesion의 영향을 고려하고, adhesion factor N_{a,i}는 토양과 버킷 사이 adhesion force의 기여도를 정량화한다. 마지막으로 surcharge factor N_{q,i}는 굴착 중 토양에 가해지는 overburden pressure 또는 외부 하중의 영향을 나타낸다. 각도 β_i는 N_{γ,i}를 최소화하여 결정한다.

현재 형태의 FEE는 특정 geometry 구성에서 불연속 문제가 발생한다. 식 (2)–(5)의 bearing capacity factor 분모에는 cotangent 항이 포함되어 있으며, 이 항은 무한대로 발산하여 수치 불안정성을 유발할 수 있다. 이러한 한계를 극복하기 위해 일련의 삼각함수 조작을 도입하여 bearing capacity factor를 표준적인 sine-cosine 형태로 재정식화한다. 이 재정식화를 통해 불연속이 발생하는 조건을 명시적으로 식별하고 이를 회피할 수 있다. β에 대해 안정적이고 물리적으로 타당한 해를 보장하기 위해 N_γ의 최소화 단계에서 유계 제약조건을 부과한다.

이 과정을 시작하기 위해 N_γ의 표현식을 살펴보면 다음과 같이 쓸 수 있다.

```text
                                      sin(α + β_i + φ)
cos α + sin α cot(β_i + φ) = ----------------------------.    (6)
                                         sin(β_i + φ)
```

```text
cos(ρ_i + δ) + sin(ρ_i + δ) cot(β_i + φ)
                     sin(ρ_i + δ + β_i + φ)
                   = ----------------------------.             (7)
                            sin(β_i + φ)
```

sin(β_i + φ)를 약분하고 이 항이 0이 아니어야 함을 인식하면 N_γ를 다음과 같이 다시 쓸 수 있다.

```text
      (cot β_i − tan α) sin(α + β_i + φ)
N_γ = -------------------------------------.                  (8)
        2 sin(ρ_i + δ + β_i + φ)
```

또한 다음 관계를 사용하면

```text
                    cos(α + β_i)
cot β_i − tan α = ----------------,                           (9)
                    cos α cos β_i
```

N_γ는 다음과 같이 된다.

```text
             cos(α + β_i) sin(α + β_i + φ)
N_{γ,i} = ---------------------------------------------.      (10)
          2 cos α sin β_i sin(ρ_i + δ + β_i + φ)
```

마찬가지로 N_c, N_a, N_q는 다음과 같이 다시 쓸 수 있다.

```text
                        cos φ
N_{c,i} = ------------------------------------,               (11)
          sin β_i sin(ρ_i + δ + β_i + φ)
```

```text
          cos(ρ_i + β_i + φ) sin(β_i + φ)
N_{a,i} = − ------------------------------------------------, (12)
          sin ρ_i sin(β_i + φ) sin(ρ_i + δ + β_i + φ)
```

```text
                  sin(α + β_i + φ)
N_{q,i} = ------------------------------------.               (13)
          sin(ρ_i + δ + β_i + φ)
```

FEE 기반 모델에서 연속적인 힘 출력을 보장하려면 식 (10)–(13)의 분모에 있는 특정 삼각함수 항이 0이 아니어야 한다. 따라서 sin(β_i) ≠ 0, sin(ρ_i) ≠ 0, cos(α) ≠ 0, sin(β_i + φ) ≠ 0 및 sin(ρ_i + δ + β_i + φ) ≠ 0의 조건을 만족해야 한다. 그러나 실제로는 이러한 조건만으로 충분하지 않다. 시간 이산화로 인해 time step 사이에서 zero-crossing이 발생하더라도 명시적으로 포착되지 않을 수 있으며, 이는 계산된 힘의 불연속이나 수치적 불안정성으로 이어질 수 있다. 이러한 가능성을 완화하기 위해 각 삼각함수 항이 |·| > ε을 만족하도록 강제하며, 여기서 ε은 양의 threshold이다.

위 조건 중 일부는 환경 제약조건으로 인해 본질적으로 충족된다. Stockpile angle α는 재료의 angle of repose에 의해 제한되며 일반적으로 45°보다 작으므로 cos α > 0.7이 보장된다. Blade penetration angle ρ도 최소 threshold보다 커야 하는데, 0에 가까운 값에서는 blade가 표면과 거의 평행해져 FEE model의 soil wedge 가정이 성립하지 않기 때문이다(Fig. 2 참조). 이 시뮬레이션에서는 ρ가 10°보다 크게 유지되도록 제한한다.

나머지 조건은 sin(β_i), sin(β_i + φ), sin(ρ_i + δ + β_i + φ) 항과 관련된다. 앞서 언급했듯이 N_γ를 최소화하는 동안 β_i에 유계 제약조건을 부과한다. 유효한 soil wedge에서는 β_i가 엄격히 양수여야 한다. 일반적인 internal friction angle φ가 22°에서 40° 사이임을 고려하면(Table A1 참조), sin(β_i + φ) 항은 안정적인 값을 유지한다. 그러나 sin(ρ_i + δ + β_i + φ)는 π 부근에서 0에 가까워질 수 있어 수치 불안정성을 초래한다. N_γ 최소화에 적용할 제약조건 집합은 다음과 같다.

```text
β_i > ε₁,    |ρ_i + δ + β_i + φ − π| > ε₂,                  (14)
```

여기서 ε₁과 ε₂는 작은 양의 margin이며, 둘 다 5°의 상수값으로 설정한다. 이 ε 값의 선택은 데이터 수집 빈도와 식 (14)의 각도 변화에 근거한다.

FEE model 사용에는 추가적인 가정이 수반된다는 점에 유의해야 한다. 대부분의 quasi-static 토양 모델과 마찬가지로 FEE 기반 힘 저항 모델은 버킷이 느리고 일정하게 운동한다고 가정한다. 이 가정은 실시간 구현을 단순화하지만 동적인 토양 변위 효과는 고려하지 않는다. 굴착 중 동적 geometry update를 포함하는 것은 향후 모델 개선을 위한 중요한 방향으로 남아 있다.

## B. 버킷 적재 중 버킷에 작용하는 힘

다음 단계에서는 Fig. 2의 cutting blade처럼 버킷 blade를 모델링하며, soil wedge는 버킷을 따라 그리고 버킷 내부에 형성된다. 버킷에 작용하는 힘을 해석하며, 여기에는 FEE에서 유도한 resultant force와 Bekker의 load–sinkage 정식화 [31]로 모델링한 normal compaction force가 포함된다.

[29]와 [30]에서 착안하여 버킷 적재 과정에서 버킷 blade에 작용하는 모든 힘을 Fig. 3에 나타냈다. 전체 힘에는 본 연구에서 FEE force라 지칭하는 reaction force F_i, 토양과 blade 사이의 adhesion force C_a wL_{t,i}, 그리고 penetration pressure P_i가 포함된다. Penetration pressure P_i는 다음과 같다.

```text
      k_c
P_i = (--- + k_φ)d_iⁿ.                                      (15)
       b
```

여기서 b는 cutting edge의 두께이고, k_c와 k_φ는 각각 cohesive modulus of deformation과 frictional modulus of deformation이며, n은 토양 변형 지수이다. 버킷 blade에 작용하는 resultant force는 normal-tangential 좌표계에서 F_i^T와 F_i^N으로 다음과 같이 쓸 수 있다.

```text
F_i^T = wbP_i + F_i sin δ + C_a wL_{t,i},                    (16)
```

```text
F_i^N = F_i cos δ.                                            (17)
```

이 힘들은 Fig. 3과 같이 hinge의 load cell을 통해 측정되는 힘 F_{H1}, F_{H2}와 관련된다. 버킷에 적재된 토양의 중량은 버킷의 위치와 stockpile geometry를 이용해 추정하므로 버킷 중량 W_b를 알 수 있다.

[FIGURE 3. 버킷 적재 단계 중 버킷 및 버킷에 작용하는 모든 힘.]

# III. PARAMETER OPTIMIZATION 방법

Section II에서 bucket-soil interaction을 위한 FEE model을 정립한 뒤 토양 parameter 값을 최적화한다. Table 1에 열거했듯이 굴착력을 모델링하려면 8개의 토양 parameter θ를 최적화해야 한다.

```text
θ = [γ  C  C_a  φ  δ  k_c  k_φ  n]ᵀ.                         (18)
```

전체 parameter optimization 프레임워크는 Section II에서 설명한 해석 모델을 버킷에서 측정한 힘 데이터에 fitting하는 방식으로 작동한다. 첫 번째 필수 입력은 탑재 센서(예: 버킷에 장착된 inertial measurement unit(IMU))로 얻거나 front-end mechanism의 kinematic model [34]을 사용해 cylinder stroke로부터 추론한 버킷의 위치와 방향이다. 이 geometry 정보는 각 time step에서 soil wedge 구성을 정의한다. 두 번째 입력은 Fig. 3에 표시한 hinge force F_{H1}과 F_{H2}이다. 이 측정값을 각각 F_obs^N과 F_obs^T로 나타낸 normal 및 tangential component로 분해하며, 이들이 관측 힘으로 사용된다. 그런 다음 프레임워크는 관측된 버킷 힘과 해석적으로 예측한 버킷 힘 사이의 차이를 최소화하여 토양 parameter θ를 추정하는 optimization-based 접근법을 적용한다. Least squares 방법으로 충분한 선형 시스템과 달리 nonlinear soil-tool interaction model에는 nonlinear optimization이 필요하다. 이러한 최적화는 중첩된 삼각함수 표현식, 힘-각도 의존성, geometry 기반 항뿐 아니라 토양 parameter와 출력 힘 사이의 implicit하고 constrained된 관계로 인해 발생한다.

Parameter optimization 문제는 토양 관련 8개 양을 독립변수로 취급하여 정식화한다. 그러나 힘 모델의 높은 차원성과 비선형성 때문에 모든 parameter를 동시에 최적화하면 수렴이 나빠지고 비효율적이기 쉽다. 이러한 한계를 극복하기 위해 다단계 최적화 접근법을 도입한다. 모델 방정식의 수학적 분석을 통해 항들이 자연스럽게 분리됨을 알 수 있으며, 이에 따라 parameter를 서로 다른 subset으로 묶어 순차적으로 최적화할 수 있다.

제안 방법의 효과를 평가하고 비교 가능한 데이터 효율적 접근법이 없다는 점을 고려하여 baseline 전략을 도입한다. 이 baseline은 8개 토양 parameter를 모두 동시에 추정하는 단일 단계 최적화로 구성되며, 다단계 정식화를 평가하기 위한 기준으로 사용된다. 이 문제는 constrained nonlinear least squares optimization으로 정식화하고 유계 제약조건을 처리할 수 있는 gradient-based algorithm L-BFGS-B [35]로 해결한다. 모델이 non-convex이므로 최적화는 초기 parameter 값에 민감하며 local minimum으로 수렴할 수 있다. 이 문제를 완화하기 위해 warm-starting, randomized initialization 및 multiple starting point를 포함한 여러 전략을 시험했다. Warm-starting은 두 가지 형태로 검토했다. 문헌에 제시되고 Table A1과 Table A2에 요약된 범위를 사용했다. 밀도 γ의 범위는 1297–2345 kg/m³로 설정했다. Cohesion C와 adhesion C_a는 모두 0–50000 N/m²로 제한했으며, 이는 연질에서 견고한 토양 및 non-cohesive에서 cohesive 토양 유형까지 포괄한다. Internal 및 external friction angle은 0°에서 45°, 즉 0.0에서 0.785 rad 사이로 제한했다. Bekker의 pressure–sinkage parameter에 허용한 범위는 k_c = 0.00–10.0 kN/m^(n+1), k_φ = 0–5000 kN/m^(n+2), 그리고 지수 n = 0.11–1.53이다. 이러한 한계는
