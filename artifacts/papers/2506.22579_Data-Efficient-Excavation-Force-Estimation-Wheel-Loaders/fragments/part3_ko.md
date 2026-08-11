## IV-B. 다중 경로

현재 결과에서 포착하지 못한 한 가지 측면은 이전 굴착 패스로 인해 토사 더미 형상이 변하는 효과이며, 이는 후속 궤적에 대한 모델의 예측 정확도에 영향을 미칠 수 있다. 이 효과를 평가하기 위해 2사이클 굴착 시나리오를 고려한다. 첫 번째 사이클에서 버킷은 토사 더미에 진입한 뒤 빠져나오며, 이에 대응하는 힘 데이터를 매개변수 추정에 사용한다. 이 시나리오는 그림 9에 시각화되어 있으며, 토사 더미는 갈색으로, 버킷 끝단의 궤적은 첫 번째 사이클에서 빨간색으로, 두 번째 사이클에서 녹색으로 표시되어 있다. 이 실행 결과는 매개변수 최적화 방법이 식별된 매개변수, 즉 토양 밀도 $\gamma=1855\ \mathrm{kg/m^3}$, 점착력 $C=194.25\ \mathrm{N/m^2}$, 부착력 $C_a=0\ \mathrm{N/m^2}$, 내부 마찰각 $\phi=45^\circ$, 외부 마찰각 $\delta=35.37^\circ$, 다짐 매개변수 $k_c=1298\ \mathrm{N/m^{n+1}}$, $k_\phi=250\ \mathrm{N/m^{n+2}}$, $n=1.50$을 사용하여 사이클 1에서 7.5%의 RMSE를 달성함을 보여준다.

그런 다음 식별된 매개변수를 사용하여 그림 9의 오른쪽 패널에 나타낸 것처럼 두 번째 사이클의 힘을 예측한다. 그러나 첫 번째 굴착 사이클이 끝난 뒤에는 재료 변위와 중력 침하로 인해 토양 표면의 형상이 바뀐다. 대부분의 경우 이렇게 형성된 표면은 재료의 안식각으로 정의되는 선형 경사면에 근사한다. 따라서 후속 굴착 사이클에서는 토사 더미 표면을 경사진 직선으로 모델링하는 것이 일반적이다. 그러나 이 시뮬레이션과 같은 일부 경우에는 토양이 균일한 경사면으로 무너지지 않고 최초 굴착에서 파낸 형상을 유지한다. 선형 표면 가정에서 벗어나는 이러한 현상은 후속 계산, 특히 관입 깊이 추정에 오차를 유발할 수 있다.

이 문제를 해결하기 위해 관입 깊이 계산 방법을 수정한다. 삼각형 토사 더미를 가정하고 버킷 끝단에서 이상화된 경사면까지의 거리 $BD$를 깊이로 측정하는 대신(그림 2 참조), 사이클 1에서 실제로 굴착된 표면까지의 거리를 직접 측정한다. 그림 9에 제시한 2사이클 시나리오에서는 첫 번째 사이클의 빨간색 궤적을 기준으로 깊이를 측정하는 것에 해당한다. 이 조정을 통해 모델은 토사 더미의 실제 형상을 더 잘 반영하며 후속 사이클의 힘 예측 정확도를 개선한다.

사이클 2에서 모델은 적응형 굴착 깊이 추정을 도입하여 17.3%의 RMSE를 달성한다. 고정된 삼각형 쐐기를 가정하지 않고 실제 굴착 표면을 기준으로 깊이를 추정함으로써 모델은 실제 상호작용 형상을 더 잘 포착하고 힘 예측 정확도를 높인다. 더 강건한 해법은 쐐기 형상을 일정한 토사 더미 각도나 고정된 삼각형 형태로 제한하지 않는 적응형 토양 모델링 프레임워크를 도입하는 것이다. 이 프레임워크에서는 굴착 전 과정에 걸쳐 변화하는 실제 토양 표면의 형상에 쐐기가 동적으로 일치한다. 이처럼 형상을 인식하며 적응하는 토양–도구 상호작용 모델의 설계는 향후 연구의 유망한 방향이다.

**[그림 10]** 주어진 굴착 경로에서 서로 다른 세 토양 유형에 대한 합력 $F_R$ 비교. 서로 다른 토양과 매개변수 및 찾아낸 매개변수는 표 4에 제시한다.

## IV-C. 단일 경로에서 서로 다른 토양의 비교

제안한 힘 추정 방법이 서로 다른 토양 유형에 적응하는 능력을 평가하기 위해 표 2에 요약한 자갈, 모래, 흙을 포함하여 Algoryx [37]의 여러 토양 구성을 시험한다. 자갈과 모래는 밀도($1474\ \mathrm{kg/m^3}$)가 동일하고 점착력이 0으로 서로 유사하므로, 점토질 모래를 나타내는 수정 모래 프로파일을 도입한다. 이 새로운 프로파일은 평균 밀도 $1874.5\ \mathrm{kg/m^3}$와 감소된 내부 마찰각 $0.59\ \mathrm{rad}$을 사용하며, 이는 표 A1에 보고된 점토질 모래의 값과 일치한다.

자갈, 수정 모래, 흙에 대해 매개변수 최적화로 얻은 합력 추세를 그림 10에서 비교한다. 표 4는 추정한 토양 매개변수와 Algoryx 기준값을 비교한다. 밀도의 경우 모든 추정값, 즉 자갈의 1513.4, 수정 모래의 1802.3, 흙의 $1833.2\ \mathrm{kg/m^3}$는 문헌에 보고된 $1297$–$2345\ \mathrm{kg/m^3}$ 범위 안에 있으며, Algoryx 값에 대한 편차는 각각 3.7%, 6.9%, 34.3%이다.

점착력과 부착력의 경우 문헌은 연약한 점성토부터 단단한 점성토까지 최대 $50000\ \mathrm{N/m^2}$의 값을 허용하지만, Algoryx 라이브러리는 제시된 매개변수 범위에 대해 $0$–$2500\ \mathrm{N/m^2}$ 범위를 사용한다. Algoryx와의 일관성을 유지하기 위해 추정 결과를 평가할 때 $0$–$2500\ \mathrm{N/m^2}$의 경계를 채택한다. 자갈($143.8\ \mathrm{N/m^2}$)과 수정 모래($216\ \mathrm{N/m^2}$)의 추정 점착력은 이 Algoryx 일관 범위 안에 있으나, 흙은 Algoryx 값 $2100\ \mathrm{N/m^2}$에 비해 $C=0$을 반환한다. 이 차이는 더 높은 부착력($3039.5\ \mathrm{N/m^2}$)으로 보상된다. 이 값은 Algoryx의 $2500\ \mathrm{N/m^2}$ 한계를 21.6% 초과하지만 문헌에 보고된 범위 안에 있다. 자갈($184\ \mathrm{N/m^2}$)과 수정 모래($72.4\ \mathrm{N/m^2}$)의 부착력 값은 각각 오차 7.36%와 2.9%로 범위 안에 충분히 들어간다.

내부 마찰각 추정값(자갈과 수정 모래는 $0.78\ \mathrm{rad}$, 흙은 $0.37\ \mathrm{rad}$)은 문헌 범위 $0.37$–$0.69\ \mathrm{rad}$에 해당한다. 자갈과 수정 모래의 값은 Algoryx 기준값($0.76\ \mathrm{rad}$ 및 $0.59\ \mathrm{rad}$)을 약간 초과하지만, 흙의 값은 하한과 일치하며 물리적으로도 타당하다. 나머지 매개변수는 Algoryx에서 실측 참값을 제공하지 않으므로 직접 비교할 수 없다.

현재의 최적화 프레임워크는 간소화한 비용함수로 관측 힘과 모델링한 힘 사이의 차이를 최소화하여 정확한 힘 예측을 우선하도록 설계되었다는 점이 중요하다. 이 접근법은 굴착 힘 추정에 맞춘 강건하고 데이터 효율적인 매개변수 피팅을 가능하게 한다. 식별된 매개변수는 물리적으로 측정한 토양 값과 완벽히 일치하도록 제약되지 않지만 현실적인 경계 안에 있으며 예측 모델링에 효과적이다. 향후에는 추가적인 물리적 제약이나 정규화 기법을 모델에 도입하여 매개변수의 해석 가능성을 높이고 힘 모델링과 토양 특성화의 연계를 더욱 강화할 수 있다.

# V. 결론

본 연구에서는 실시간 토양 매개변수 최적화와 수정된 해석적 힘 모델을 이용하여 휠 로더의 굴착 힘을 추정하는 데이터 효율적 프레임워크를 제시하였다. 제안한 방법은 힘 예측에서 최저 8.6%의 RMSE를 달성했으며, 다단계 제약 최적화 전략을 통해 계산 시간을 45% 이상 줄였다.

이 프레임워크는 이전 버킷 적재 사이클의 힘 데이터를 활용하여 밀도, 점착력, 부착력, 내부 및 외부 마찰각, 다짐과 같은 토양 매개변수를 보정하고, 이를 다음 사이클의 저항력 예측에 사용한다. 이 과정은 대규모 데이터셋이나 오프라인 훈련 없이 사이클마다 적응하는 굴착 계획을 가능하게 한다. 이 방법론은 수정된 기본 토공 방정식(Fundamental Earthmoving Equation)에 연속성 제약과 Bekker의 하중–침하 공식을 통합하여 수치적 안정성과 물리적 타당성을 모두 개선한다.

고충실도 Algoryx Dynamics 시뮬레이션으로 검증한 결과, 이 접근법은 서로 다른 궤적과 토양 유형 전반에 효과적으로 일반화할 수 있다. 적은 데이터 요구량과 높은 계산 효율성 덕분에 굴착 사이클 사이의 시간 간격 안에 실행하기에 적합하며, 자율 굴착 시스템의 적시 적응을 지원한다.

향후 연구에서는 속도, 가속도, 관성 효과를 포착하도록 동적 힘 모델링을 도입해 프레임워크를 확장하고, 굴착 중 토양 변위와 형상 표현을 개선하며, 초기화 민감도를 다루는 더 체계적인 전략을 포함하고, 시뮬레이션을 넘어 실험 플랫폼에서 성능을 검증할 것이다. 이러한 노력은 준정적 공식, 단순화한 토사 더미 가정, 초기화 의존성, 시뮬레이션 기반 검증 의존이라는 현재의 한계를 해결하는 것을 목표로 한다. 또한 향후 연구에서는 비전과 깊이 감지 같은 지각 기반 기법을 탐구하여 토양 유형과 표면 특성을 추론하고, 이를 통해 토양 매개변수 정확도를 개선할 수 있는 보완 정보를 제공할 것이다.

# 감사의 글

저자들은 시뮬레이션 소프트웨어 사용 권한을 제공한 스웨덴의 Algoryx Simulation에 감사를 표한다. 또한 원고 문장의 명료성을 다듬는 데 AI 기반 도구를 사용했음을 밝힌다. 본 연구는 Komatsu Ltd.의 부분 지원을 받았다. 저자들은 이 재정 지원에 깊이 감사한다.

# 부록 A. 문헌에 보고된 토양 매개변수 값과 범위

현실적인 매개변수 경계를 설정하기 위해 여러 문헌 자료와 공학 데이터베이스에서 값을 수집하였다. 공학 데이터 온라인 플랫폼인 StructX [41]에서 토양 상관계, 밀도, 탄성계수, 푸아송비, 안식각, 점성토와 비점성토의 특성을 확보하였다. 토양 밀도 범위는 [42]를 포함한 과거 및 현대 문헌에서 가져왔으며, 점착 및 마찰 특성은 [43]과 같은 편람에서 수집하였다. 추가적인 점착력 및 내부 마찰각 값은 통일토질분류법(Unified Soil Classification System, USCS) [45]에 따른 토양 매개변수를 보고하는 EcorisQ [44]에서 얻었다. 부착계수 범위는 지반공학 실무에서 널리 사용하는 도구 모음인 GEO5 지반공학 소프트웨어 자료 [46]와 교차 확인하였다.

위 자료들은 토양 유형 또는 토양 상태에 따른 토양 밀도 $\gamma$, 점착력 $C$, 부착력 $C_a$, 내부 마찰각 $\phi$와 같은 매개변수를 제공하며, 이를 표 A1에 요약한다. 토양–구조물 상호작용을 지배하는 외부 마찰각 $\delta$는 내부 마찰각 $\phi$와 접촉면 재료(예: 강철, 콘크리트, 목재)의 물성에 모두 좌우된다. Delft Sand, Clay, and Rock Cutting Model [47]은 $\delta$와 $\phi$ 사이의 전형적인 관계를 보고하며, 흔히 $\delta$를 $\phi$의 일정 비율로 표현한다. 대표적인 외부 마찰값은 표 A1의 끝부분에 포함한다. 일반적인 건설 장비와의 일관성을 위해 휠 로더 버킷은 강철로 제작된다고 가정한다.

위에서 요약한 매개변수 외에도 Bekker의 하중–침하 공식은 $k_c$(점착 변형계수), $k_\phi$(마찰 변형계수), $n$(변형 지수)이라는 세 가지 추가 수량을 도입한다. 이 매개변수들은 하중을 받는 토양의 비선형 압력–침하 관계를 특성화하며, 굴착 과정에서 절삭 및 관입 저항을 모델링하는 데 특히 중요하다. 지형역학에서 널리 적용되는 Bekker 공식은 행성 표면, 농경지, 비포장 건설 현장과 같은 연약하고 변형 가능한 지형에서 운행하는 바퀴와 궤도의 토양 침하를 예측할 수 있게 한다. 여러 자료에 보고된 이 매개변수 값을 표 A2에 정리한다.

**[표 A1] 여러 자료에서 수집한 토양 매개변수 요약.** 매개변수는 토양 유형(USCS 분류 사용), 토양 상태 또는 토양과 접촉하는 재료를 기준으로 분류한다. 가능한 경우 밀도 $\gamma$, 점착력 $C$, 부착력 $C_a$, 내부 마찰각 $\phi$를 제시한다. 외부 마찰각 $\delta$ 값은 [47]에서 정리한 관계에 따라 토양과 접촉하는 재료를 기준으로 한다. 대시(–)는 해당 토양 분류에서 값이 보고되지 않았거나 적용되지 않음을 나타낸다.

| 토양 설명 | USCS 분류 | 밀도 $\gamma$ ($\mathrm{kg/m^3}$) | 점착력 $C$ (kPa) | 부착력 $C_a$ (kPa) | 내부 마찰각 $\phi$ (°) | 외부 마찰각 $\delta$ (°) |
|---|---:|---:|---:|---:|---:|---:|
| **토양 유형별 분류. [41], [42], [43]에서 인용** | | | | | | |
| 입도 분포가 양호한 자갈, 세립~조립 자갈 | GW | 1631–1937 | 0 | – | 40 | – |
| 입도 분포가 불량한 자갈 | GP | 1631–1937 | 0 | – | 38 | – |
| 실트질 자갈 | GM | 1297–1500 | 0 | – | 36 | – |
| 점토질 자갈 | GC | 1297–1500 | 0 | – | 34 | – |
| 세립분을 함유한 점토질 자갈 | GC-CL | 1297–1500 | 3 | – | 29 | – |
| 입도 분포가 양호한 모래, 세립~조립 모래 | SW | 1410–2279 | 0 | – | 38 | – |
| 입도 분포가 불량한 모래 | SP | 1410–2279 | 0 | – | 36 | – |
| 실트질 모래 | SM | 1378–2371 | 0 | – | 34 | – |
| 점토질 모래 | SC | 1378–2371 | 0 | – | 32 | – |
| 실트 | ML | 1300–1380 | 0 | – | 33 | – |
| 저소성 점토, 빈배합 점토 | CL | 1330–1390 | 20 | – | 27 | – |
| 고소성 점토, 고배합 점토 | CH | 1330–1470 | 25 | – | 22 | – |
| 유기질 실트, 유기질 점토 | OL | 1330–1500 | 10 | – | 25 | – |
| 유기질 점토, 유기질 실트 | OH | 1330–1500 | 10 | – | 22 | – |
| 고소성 실트, 탄성 실트 | MH | 1300–1380 | 5 | – | 24 | – |
| **토양 상태별 분류. [44], [46]에서 인용** | | | | | | |
| 연약 및 매우 연약한 점성토 | – | – | 0–12 | 0–12 | – | – |
| 중간 연경도의 점성토 | – | – | 12–24 | 12–24 | – | – |
| 단단한 점성토 | – | – | 24–48 | 24–48 | – | – |
| 매우 단단한 점성토 | – | – | 48–96 | 48–96 | – | – |
| 매우 연약한 토양 | – | 1631–1937 | 0–10 | – | – | – |
| 연약한 토양 | – | 1733–2039 | 10–25 | – | – | – |
| 보통 토양 | – | 1784–2141 | 25–50 | – | – | – |
| 단단한 토양 | – | 1835–2243 | 50–100 | – | – | – |
| 매우 단단한 토양 | – | 2141–2243 | 100–200 | – | – | – |
| 경질 토양 | – | 2039–2345 | 200– | – | – | – |
| **접촉 재료별 외부 마찰각 분류. [47]에서 인용** | | | | | | |
| 강재 말뚝(NAVFAC) | – | – | – | – | – | $20^\circ$ |
| USACE | – | – | – | – | – | $0.67\phi$–$0.83\phi$ |
| 강철(Broms) | – | – | – | – | – | $20^\circ$ |
| 콘크리트(Broms) | – | – | – | – | – | $3/4\phi$ |
| 목재(Broms) | – | – | – | – | – | $2/3\phi$ |
| Lindeburg | – | – | – | – | – | $2/3\phi$ |
| 콘크리트 벽(Coulomb) | – | – | – | – | – | $2/3\phi$ |

**[표 A2] 서로 다른 토양 유형의 압력–침하 매개변수.** 여러 문헌에 보고된 값을 수집하였다. 표는 인용한 각 문헌에서 가져온 값에 따라 구분한다.

| 토양 유형 | $k_c$ ($\mathrm{kN/m^{n+1}}$) | $k_\phi$ ($\mathrm{kN/m^{n+2}}$) | $n$ |
|---|---:|---:|---:|
| **연약지반 궤도차량 거동 시뮬레이션 [48]에서 인용** | | | |
| 건조 느슨한 모래 | 0.00E+00 | 1.58E+03 | 1.01 |
| 건조 조밀한 모래 | 9.57E+01 | 3.27E+03 | 1.15 |
| 건조 모래 LLL¹ | 0.99E+00 | 1.52E+03 | 1.10 |
| 중점토 WES² 40 | 1.84E+00 | 1.03E+02 | 0.11 |
| 빈배합 점토 WES² 32 | 1.52E+00 | 1.19E+02 | 0.15 |
| LETE³ 모래 | 1.02E+02 | 5.30E+03 | 0.79 |
| LETE³ 모래 2nd | 6.94E+00 | 5.06E+02 | 0.71 |
| 사질 양토 | 1.19E+01 | 6.74E+02 | 0.81 |
| 연설(Soft Snow) | 6.16E+00 | 1.49E+02 | 1.53 |
| IIT 건조 모래⁴ [49] | -1.12E+02 | 3.101E+03 | 0.75 |
| **Carrier의 달 매개변수⁵ [50]에서 인용** | | | |
| 토양 유형 A | 0.00E+00 | 8.20E+02 | 1.00 |
| 토양 유형 B | 1.40E+00 | 8.20E+02 | 1.00 |
| 토양 유형 C | 2.80E+00 | 8.20E+02 | 1.00 |
| **행성 토양의 변형 [51]에서 인용** | | | |
| 달 | 0.14E+00 | 8.20E+02 | 1.00 |
| 화성(MSS-A⁶) | 1.87E+01 | 7.63E+02 | 0.63 |
| 지구(건조 모래) | 0.99E+00 | 1.52E+03 | 1.10 |
| 지구(점토) | 1.31E+01 | 6.92E+02 | 0.50 |

¹ LLL: Lunar Logistics Load 모사 토양.  
² WES: Waterways Experiment Station 토양 분류.  
³ LETE: 캐나다 국방부 Land Engineering Test Establishment.  
⁴ IIT: Illinois Institute of Technology에서 시험한 토양.  
⁵ 토양 유형 A, B, C는 달 탐사차 설계 단계에서 예상되는 달 표면 조건을 포괄하기 위해 개발한 이론적 토양 모델을 의미한다. 유형 A는 최소 토양 강도 특성, 유형 B는 중앙값(공칭) 조건, 유형 C는 최대 토양 강도 특성을 나타낸다.  
⁶ MSS-A: Mars Soil Simulant A.

# 참고문헌

[1] Associated General Contractors of America and Arcoro. (2024). *2024 Workforce Survey Analysis*. [Online]. Available: https://www.agc.org/sites/default/files/Files/Communications/2024WorkforceSurveyAnalysis.pdf

[2] M. Gottschalk, G. Jacobs, and A. Kramer, “Test method for evaluating the energy efficiency of wheel loaders,” *ATZoffhighway Worldwide*, vol. 11, no. 1, pp. 44–49, Mar. 2018, doi: 10.1007/s41321-018-0008-0.

[3] D. Huo, J. Chen, H. Zhang, Y. Shi, and T. Wang, “Intelligent prediction for digging load of hydraulic excavators based on RBF neural network,” *Measurement*, vol. 206, Jan. 2023, Art. no. 112210.

[4] Y. Shen, J. Wang, C. Feng, Q. Wang, and J. Fan, “Data-physics hybrid-driven external forces estimation method on excavators,” *Mech. Syst. Signal Process.*, vol. 223, Jan. 2025, Art. no. 111902.

[5] R. Madau, D. Colombara, A. Alexander, A. Vacca, and L. Mazza, “An online estimation algorithm to predict external forces acting on a front-end loader,” *Proc. Inst. Mech. Eng., I, J. Syst. Control Eng.*, vol. 235, no. 9, pp. 1678–1697, Oct. 2021, doi: 10.1177/09596518211005583.

[6] I. Palomba, D. Richiedei, A. Trevisani, E. Sanjurjo, A. Luaces, and J. Cuadrado, “Estimation of the digging and payload forces in excavators by means of state observers,” *Mech. Syst. Signal Process.*, vol. 134, Dec. 2019, Art. no. 106356.

[7] C. J. Coetzee and D. N. J. Els, “The numerical modelling of excavator bucket filling using DEM,” *J. Terramechanics*, vol. 46, no. 5, pp. 217–227, Oct. 2009.

[8] E. G. Nezami, Y. M. A. Hashash, D. Zhao, and J. Ghaboussi, “Simulation of front end loader bucket–soil interaction using discrete element method,” *Int. J. for Numer. Anal. Methods Geomechanics*, vol. 31, no. 9, pp. 1147–1162, Aug. 2007.

[9] S. Blouin, A. Hemami, and M. Lipsett, “Review of resistive force models for earthmoving processes,” *J. Aerosp. Eng.*, vol. 14, no. 3, pp. 102–111, Jul. 2001.

[10] W. C. Swick and J. V. Perumpral, “A model for predicting soil-tool interaction,” *J. Terramechanics*, vol. 25, no. 1, pp. 43–56, Jan. 1988.

[11] W. R. Gill and G. E. Vanden Berg, *Soil Dynamics in Tillage and Traction*, no. 316. Washington, DC, USA: Agricultural Research Service, U.S. Department of Agriculture, 1967.

[12] A. Hemami, “Motion trajectory study in the scooping operation of an LHD-loader,” *IEEE Trans. Ind. Appl.*, vol. 30, no. 5, pp. 1333–1338, Jun. 1994.

[13] D. R. P. Hettiaratchi, B. D. Witney, and A. R. Reece, “The calculation of passive pressure in two-dimensional soil failure,” *J. Agricult. Eng. Res.*, vol. 11, no. 2, pp. 89–107, Jun. 1966.

[14] A. R. Reece, “Paper 2: The fundamental equation of Earth-moving mechanics,” in *Proc. Inst. Mech. Eng., Conf.*, Jun. 1964, vol. 179, no. 6, pp. 16–22, doi: 10.1243/pime_conf_1964_179_134_02.

[15] E. McKyes, *Soil Cutting and Tillage*. Amsterdam, The Netherlands: Elsevier, 1985.

[16] H. Cannon, “Extended earthmoving with an autonomous excavator,” Robot. Inst., Carnegie Mellon Univ., Pittsburgh, PA, USA, Tech. Rep. CMU-RI-TR-99-10, May 1999. [Online]. Available: https://www.ri.cmu.edu/publications/extended-earthmoving-with-an-autonomousexcavator/

[17] O. Luengo, S. Singh, and H. Cannon, “Modeling and identification of soil-tool interaction in automated excavation,” in *Proc. IEEE/RSJ Int. Conf. Intell. Robots Systems. Innov. Theory, Pract. Appl.*, vol. 3, Mar. 1998, pp. 1900–1906.

[18] C. P. Tan, Y. H. Zweiri, K. Althoefer, and L. D. Seneviratne, “Online soil parameter estimation scheme based on Newton–Raphson method for autonomous excavation,” *IEEE/ASME Trans. Mechatronics*, vol. 10, no. 2, pp. 221–229, Apr. 2005.

[19] S. Yu, X. Song, and Z. Sun, “On-line prediction of resistant force during soil–tool interaction,” *J. Dyn. Syst., Meas., Control*, vol. 145, no. 8, Aug. 2023, Art. no. 081004, doi: 10.1115/1.4062513.

[20] P. Egli, D. Gaschen, S. Kerscher, D. Jud, and M. Hutter, “Soil-adaptive excavation using reinforcement learning,” *IEEE Robot. Autom. Lett.*, vol. 7, no. 4, pp. 9778–9785, Oct. 2022.

[21] N. Bennett, A. Walawalkar, M. Heck, and C. Schindler, “Integration of digging forces in a multi-body-system model of an excavator,” *Proc. Inst. Mech. Eng., K, J. Multi-body Dyn.*, vol. 230, no. 2, pp. 159–177, Jun. 2016, doi: 10.1177/1464419315592081.

[22] M. Lipsett and R. Y. Moghaddam, “Modeling excavator-soil interaction,” in *Bifurcations, Instabilities and Degradations in Geomaterials*, 2011, pp. 347–366.

[23] F. Schnaid, *Situ Testing in Geomechanics: The Main Tests*. Boca Raton, FL, USA: CRC Press, 2008.

[24] R. Yousefi Moghaddam, A. Kotchon, and M. G. Lipsett, “Method and apparatus for on-line estimation of soil parameters during excavation,” *J. Terramechanics*, vol. 49, nos. 3–4, pp. 173–181, Jun. 2012. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0022489812000262

[25] H. Fernando and J. Marshall, “What lies beneath: Material classification for autonomous excavators using proprioceptive force sensing and machine learning,” *Autom. Construction*, vol. 119, Nov. 2020, Art. no. 103374. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0926580520309547

[26] W. J. Wagner, A. Soylemezoglu, D. Nottage, and K. Driggs-Campbell, “In situ soil property estimation for autonomous earthmoving using physics-infused neural networks,” in *Proc. 16th Eur.-Afr. Regional Conf.*, 2023, pp. 84–93, doi: 10.56884/jdxp2382. [Online]. Available: https://www.proceedings.com/content/072/072716webtoc.pdf

[27] K. Althoefer, C. P. Tan, Y. H. Zweiri, and L. D. Seneviratne, “Hybrid soil parameter measurement and estimation scheme for excavation automation,” *IEEE Trans. Instrum. Meas.*, vol. 58, no. 10, pp. 3633–3641, Oct. 2009.

[28] Y. Zhao, J. Wang, Y. Zhang, and C. Luo, “A novel method of soil parameter identification and force prediction for automatic excavation,” *IEEE Access*, vol. 8, pp. 11197–11207, 2020.

[29] H. Lee, M. Kim, and W. Yoo, “Force-balancing algorithm to remove the discontinuity in soil force during wheel loader excavation,” *J. Mech. Sci. Technol.*, vol. 32, no. 10, pp. 4951–4957, Oct. 2018, doi: 10.1007/s12206-018-0943-9.

[30] M. D. Worley and V. La Saponara, “A simplified dynamic model for front-end loader design,” *Proc. Inst. Mech. Eng., C, J. Mech. Eng. Sci.*, vol. 222, no. 11, pp. 2231–2249, Nov. 2008, doi: 10.1243/09544062jmes688.

[31] M. G. Bekker, “Mechanics of locomotion and lunar surface vehicle concepts,” *SAE Trans.*, vol. 72, pp. 549–569, Mar. 1964. [Online]. Available: http://www.jstor.org/stable/44562978

[32] J. Yao, C. P. Edson, S. Yu, G. Zhao, Z. Sun, X. Song, and K. A. Stelson, “Bucket loading trajectory optimization for the automated wheel loader,” *IEEE Trans. Veh. Technol.*, vol. 72, no. 6, pp. 6948–6958, Jun. 2023.

[33] H. Cannon and S. Singh, “Models for automated earthmoving,” in *Experimental Robotics VI*. London, U.K.: Springer, 2000, pp. 163–172, doi: 10.1007/BFb0119395.

[34] G. Liang, L. Liu, Y. Meng, and G. Bai, “Shoveling trajectory tracking control of loader working mechanism,” in *Proc. 5th World Conf. Mech. Eng. Intell. Manuf. (WCMEIM)*, Nov. 2022, pp. 668–673.

[35] C. Zhu, R. H. Byrd, P. Lu, and J. Nocedal, “Algorithm 778: L-BFGS-B: Fortran subroutines for large-scale bound-constrained optimization,” *ACM Trans. Math. Softw.*, vol. 23, no. 4, pp. 550–560, Dec. 1997, doi: 10.1145/279232.279236.

[36] D. Karanfil, “Developing scalable digital twins of construction vehicles,” Ph.D. dissertation, Dept. Mech. Aerosp. Eng., Univ. California, Berkeley, CA, USA, 2025. [Online]. Available: https://www.proquest.com/docview/3201332906?pqorigsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses

[37] (Sep. 2024). *AGX Dynamics*. [Online]. Available: https://www.algoryx.se/products/agx-dynamics/

[38] M. Servin, T. Berglund, and S. Nystedt, “A multiscale model of terrain dynamics for real-time earthmoving simulation,” *Adv. Model. Simul. Eng. Sci.*, vol. 8, no. 1, Dec. 2021, doi: 10.1186/s40323-021-00196-3.

[39] L. Jing and O. Stephansson, “Discrete element methods for granular materials,” in *Fundamentals of Discrete Element Methods for Rock Engineering (Developments in Geotechnical Engineering)*, vol. 85. Amsterdam, The Netherlands: Elsevier, 2007, ch. 11, pp. 399–444. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0165125007850115

[40] C. Santos, V. Urdaneta, X. García, and E. Medina, “Compression and shear-wave velocities in discrete particle simulations of quartz granular packings: Improved hertz-mindlin contact model,” *Geophysics*, vol. 76, no. 5, pp. E165–E174, Sep. 2011, doi: 10.1190/geo2010-0376.1.

[41] StructX. (2025). *Soil Properties*. [Online]. Available: https://structx.com/SoilProperties.html

[42] I. Langmuir, “The constitution and fundamental properties of solids and liquids. Part I. Solids,” *J. Amer. Chem. Soc.*, vol. 38, no. 11, pp. 2221–2295, Nov. 1916, doi: 10.1021/ja02268a002.

[43] B. G. Look, *Handbook of Geotechnical Investigation and Design Tables*. New York, NY, USA: Taylor & Francis, 2007.

[44] (2024). *Cohesion and Friction Angle Values for USCS Soil Classes*. [Online]. Available: https://www.ecorisq.org/docs/USCSsoilclasses.pdf

[45] A. Casagrande, “Classification and identification of soils,” *Trans. Amer. Soc. Civil Engineers*, vol. 113, no. 1, pp. 901–930, 1948. [Online]. Available: https://ascelibrary.org/doi/abs/10.1061/TACEAT.0006109

[46] Fine Software. (2024). *GEO5 Geotechnical Software–Adhesion of Soil*. Accessed: Mar. 16, 2025. [Online]. Available: https://www.finesoftware.eu/help/geo5/en/adhesion-of-soil-01/

[47] S. A. Miedema, *The Delft Sand, Clay and Rock Cutting Model*. Amsterdam, The Netherlands: IOS Press, 2014.

[48] G. Prezioso, “Simulation of the behaviour of tracked vehicles on soft soils using multibody software,” Ph.D. dissertation, Dept. Mech. Eng., Univ. Politecnico di Torino, Turin, Italy, 2023. [Online]. Available: https://webthesis.biblio.polito.it/28757/

[49] G. Meirion-Griffith and M. Spenko, “An empirical study of the terramechanics of small unmanned ground vehicles,” in *Proc. IEEE Aerosp. Conf.*, Mar. 2010, pp. 1–6.

[50] W. D. Carrier, *Lunar Soil Simulation and Trafficability Parameters*. Lunar Geotechnical Institute, 2006. [Online]. Available: https://www.lpi.usra.edu/lunar/surface/

[51] G. Scott, G. Meirion-Griffith, C. Saaj, and E. Moxey, “A comparative study of the deformation of planetary soils under tracked and legged rovers,” in *Proc. AIAA Space Conf. Expo.*, Sep. 2008, p. 7897, doi: 10.2514/6.2008-7897.

# 저자 약력

## Armin Abdolmohammadi

Armin Abdolmohammadi는 2019년 이란 테헤란의 Sharif University of Technology에서 기계공학 학사학위를, 2025년 University of California at Davis에서 석사학위를 받았으며, 현재 동 대학 Control, Optimization, Robotics, and Electrification(CORE) Laboratory에서 박사과정을 밟고 있다. 연구 관심 분야는 시스템 동역학, 제어 이론, 로보틱스이며, 특히 최적제어와 자동차 및 오프로드 기계 시스템에의 응용에 중점을 둔다.

## Navid Mojahed

Navid Mojahed는 이란 Isfahan University of Technology에서 기계공학 학사학위를, 이란 Amirkabir University of Technology에서 응용수학 석사학위를, 이란 University of Mazandaran에서 응용수학 박사학위를 받았다. 스페인 University of Santiago de Compostela에서 연구원으로 근무하였다. 현재 University of California at Davis의 박사후연구원이다. 연구 관심 분야는 분수 미분방정식, 수치해석법, 게임 이론, 최적제어, 자율주행차 시스템이다.

## Shima Nazari

Shima Nazari는 2009년과 2012년에 이란 테헤란의 Sharif University of Technology에서 각각 학사 및 석사학위를 받았으며, 2019년 University of Michigan에서 기계공학 박사학위를 받았다. 현재 University of California at Davis 기계공학과 조교수이다. 현 직책 이전에는 UC Berkeley의 Model Predictive Control Laboratory에서 박사후연구원으로 근무하였다. 연구 관심 분야는 자동화, 전기자동차, 교통 시스템에 응용되는 최적제어 및 데이터 기반 제어이다.

## Bahram Ravani

Bahram Ravani는 1976년 Louisiana State University에서 기계공학 학사학위를 최우등(magna cum laude)으로, 1978년 Columbia University에서 기계공학 석사학위를, 1982년 Stanford University에서 기계공학 박사학위를 받았다.

University of Wisconsin–Madison에서 종신교원으로 근무하였다. 1987년부터 UC Davis의 교수로 재직하면서 기계공학과 학과장과 전기·컴퓨터공학과 학과장을 역임하였다. 또한 Center for Information Technology Research in the Interest of Society의 캠퍼스 책임자를 맡았다. California Department of Transportation과 UC Davis의 협력기관인 Advanced Highway Maintenance and Construction Technology(AHMCT) Research Center의 창립 책임자이기도 하다. 2025년 7월까지 AHMCT를 공동 지휘하였다. 현재 UC Davis 기계항공우주공학과 석좌교수이다. 현재 연구 관심 분야는 건설 및 유지관리의 디지털 전환, 지능형 교통 시스템과 도로 안전, 운동학, 동역학 및 생체역학, 로보틱스와 메카트로닉스, 기계 설계, 제조이다.
