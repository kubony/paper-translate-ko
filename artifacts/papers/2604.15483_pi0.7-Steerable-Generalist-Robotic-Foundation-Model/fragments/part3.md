# π0.7: 조종 가능한 범용 로봇 파운데이션 모델 — 제3부

> 번역 범위: `main.tex` 656–828행 및 `main.bbl`의 활성 참고문헌 전체. 본문 내 인라인 인용 번호는 제거했다.

## 10. 논의

**[P3-001 | source lines 656–658]**

우리는 별도의 조정 없이도 조합적 일반화와 효과적인 언어 지시 이행 능력을 보이며, 개별 고난도 정교 조작 과제에 맞춰 fine-tuning한 더 전문적인 모델과 경쟁할 만한 과제 성능을 내는 범용 로봇 파운데이션 모델 π0.7을 제시했다. π0.7의 핵심은 prompt expansion에서 영감을 받은 diverse prompting 전략이다. 이 전략에서는 학습 중에, 그리고 선택적으로는 테스트 시에도 episode에 관한 추가 정보를 모델에 제공한다. 이러한 추가 정보에는 더 상세한 언어, episode metadata, subgoal 이미지가 포함된다. 실험 결과, diverse prompting과 더 크고 다양한 데이터셋을 활용하면 π0.7이 서로 다른 여러 품질 수준의 policy를 표현하고 specialist의 성능을 다시 하나의 사전 학습 모델로 distill할 수 있음을 확인했다. π0.7은 로봇 간 skill 전이, 복잡한 언어 명령 이행, 그리고 skill을 새로운 방식으로 재조합하여 새로운 과제를 해결하는 조합적 일반화 등 여러 emergent capability를 습득한다.

**[P3-002 | source lines 660–660]**

π0.7은 폭넓게 일반화하지만, zero-shot 일반화의 성공률은 예상할 수 있듯 in-distribution 과제보다 낮다. 관측된 과제의 성공률은 흔히 90%를 넘지만, 미관측 과제 또는 미관측 과제-로봇 조합의 성공률은 60–80% 범위이다. 향후 연구의 흥미로운 방향은 π0.7의 높은 steerability를 활용하여 테스트 과제의 데이터로부터 효율적으로 학습하는 것이다. 예를 들어 더 상세한 언어 coaching이나 autonomous reinforcement learning까지 활용할 수 있다.

**[P3-003 | source lines 662–662]**

우리 실험의 다소 뜻밖인 한계는 이처럼 크고 다양한 데이터셋으로 학습할 때 어떤 과제가 진정으로 ‘관측’되었거나 ‘미관측’되었는지를 확정하기가 실질적으로 어렵다는 점이다. 일부 일반화 실험, 예컨대 조합적 일반화 절의 실험에서는 의도적으로 데이터를 수집하지 않은 과제를 사용했지만, 데이터셋에 포함된 장면과 행동이 매우 다양하므로 잠재적으로 관련된 skill이 다른 label로 또는 다른 과제를 수행하는 과정의 부수적 요소로 데이터 어딘가에 존재할 수 있다. 이는 여러 면에서 대규모 언어 모델의 일반화를 이해할 때 마주치는 난점과 닮았다. 무엇이 진정으로 새로운지 판별하기가 어려워지며, 모델은 주로 다른 상황의 skill과 행동을 ‘리믹스’하여 일반화를 달성하고 있을 수도 있다. 그러나 우리는 이것이 사실 조합적 일반화의 본질이라고 본다. 행동이 진정으로 새로운 것이든 관측된 구성요소의 새로운 조합에 불과하든 실질적 함의는 유사하다. 로봇이 해결하기를 원하는 새 과제마다 표적화된 데이터를 일부러 수집하는 대신, 조합적 일반화를 제공하는 모델이라면 사용자가 원하는 과제를 수행하도록 그저 prompt할 수 있다. 이러한 조합적 일반화를 대규모로 가능하게 하는 모델은 로봇 학습에 접근하는 방식을 바꿀 것이며, 추가 action 데이터를 수집할 필요 없이 로봇에 prompt를 주고, coaching하고, 설명할 수 있게 한다.

## 감사의 말

**[P3-004 | source lines 664–666]**

데이터 수집, 평가, 물류, 영상 녹화를 담당한 robot operator들과 로봇 유지보수 및 수리를 담당한 technician들에게 감사한다. 전체 기여 내역은 부록의 ‘기여’ 절에 제시한다.

## 부록

### 기여

**[P3-005 | source lines 679–682] 데이터 수집 및 운영.** Ashwin Balakrishna, George Bokinsky, Thomas Charbonnier, Grace Connors, Michael Equi, Chelsea Finn, Lachlan Groom, Hunter Hancock, Karol Hausman, Connor Jacobsen, Rowan Jen, Marinda Lamb, Vishnu Mano, Nandan Marwaha, Aikys Mongush, Tyler Patterson, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Will Stoeckle, Anna Walling, Jason Wang, Samuel Whitmore, Blake Williams.

**[P3-006 | source lines 684–684] Annotation 및 보충 데이터.** Ashwin Balakrishna, Karan Dhabalia, Danny Driess, Chelsea Finn, Haroun Habeeb, Rowan Jen, Chandra Kuchi, Karl Pertsch, Lucy Xiaoyang Shi, Will Stoeckle, Quan Vuong.

**[P3-007 | source lines 686–686] Policy 학습 및 연구.** Bo Ai, Ashwin Balakrishna, Kevin Black, Danny Driess, Michael Equi, Yunhao Fang, Chelsea Finn, Catherine Glossop, Haroun Habeeb, Karol Hausman, Gashon Hussein, Victor Hwang, Brian Ichter, Liyiming Ke, Sergey Levine, Xinyu Li, Yao Lu, Suraj Nair, Karl Pertsch, Allen Z. Ren, Baifeng Shi, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Jiaming Tang, Marcel Torne, Kyle Vedder, Quan Vuong, XuDong Wang, Charles Xu, Lili Yu, Wuming Zhang, Zhuoyang Zhang.

**[P3-008 | source lines 688–688] Policy infrastructure.** Kevin Black, Karan Dhabalia, Danny Driess, Mairbek Khadikov, Chandra Kuchi, Adrian Li-Bell, Vladislav Lialin, Wallace Lim, Yao Lu, Allen Z. Ren, Lucy Xiaoyang Shi, Kyle Stachowicz, Jiaming Tang, Quan Vuong, Haohuan Wang, Ury Zhilinsky.

**[P3-009 | source lines 690–690] 로봇 hardware.** Ali Amin, Raichelle Aniceto, Greg Balke, Vedant Choudhary, Foster Collins, Grace Connors, Maitrayee Dhaka, Adnan Esmail, Thomas Godden, Ivan Goryachev, Tim Jones, Gregg Kammerer, Ben Katz, Devin LeBlanc, Brendon LeCount, Zhonglin Liang, Enyu Luo, Liam Murphy, Gavin Schelske, Shalom Tekeste, Chris Whalen, Sukwon Yoo.

**[P3-010 | source lines 692–692] 로봇 infrastructure.** Greg Balke, Kevin Black, Shihao Cao, Ken Conley, James Darpinian, Jared DiCarlo, Hunter Hancock, Karol Hausman, Szymon Jakubczak, Jimmy Tanner.

**[P3-011 | source lines 694–694] 집필 및 도해.** Bo Ai, Ashwin Balakrishna, Kevin Black, Chelsea Finn, Sergey Levine, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Kyle Stachowicz.

### Attention pattern

**[P3-012 | source lines 696–702]**

**FIGURE app:attention_masks:** π0.7 모델과 그 world model(subgoal 이미지 생성용)은 학습 및 inference 중 서로 다른 여러 비자명한 attention pattern을 사용한다. 왼쪽 위부터 설명하면 다음과 같다. 이미지 goal이 없을 때는 π0.5와 동일한 attention pattern을 사용하며, memory-aware인 모든 이미지 view의 embedding 사이에 전역 양방향 attention을 적용한다. FAST token은 학습 시에만 이용할 수 있으며 flow action과 서로 attention하지 않는다는 점에 유의해야 한다. 이미지 goal이 있으면 text prompt 뒤에 block-causal 양방향 block을 하나 더 추가한다. classifier-free guidance를 inference 시 수행할 때는 효율적인 inference를 위해 positive example과 negative example을 동일한 sequence에 pack한다. 이를 위해 서로 attention하지 않는 두 branch(positive와 negative)를 가진 ‘attention tree’를 구성한다. BAGEL을 따라 학습 시 world model에는 이미지 사본 세 개가 입력되며, 각 사본은 multiview group 내부에서 block-bidirectional이다. 세 사본은 ViT로 encode한 현재 observation, VAE로 encode한 현재 observation, VAE로 encode한 노이지 이미지 goal이다. world model은 inference 시 이와 유사한 CFG 기법을 사용하지만 CFG group이 두 개가 아니라 세 개이므로 mask가 더 복잡하다.

**[P3-013 | source lines 704–704]**

π0.7과 경량 world model(subgoal 이미지 생성용)의 학습 및 inference 실행에 사용하는 attention pattern은 FIGURE app:attention_masks에 설명한다.

### World model 학습

**[P3-014 | source lines 706–708]**

world model은 BAGEL로 초기화하며 대체로 동일한 학습 recipe를 사용한다. label 품질, 특히 시간적 segmentation 품질이 subgoal 품질에 큰 영향을 미치는 것으로 나타났으므로, 고품질로 segmentation된 언어 label을 갖춘 로봇 데이터와 egocentric human video 데이터의 일부를 사용한다. 또한 모델의 semantic knowledge를 더 잘 보존하기 위해 여러 open-source 이미지 편집 데이터셋과 open-source 비디오 데이터셋을 혼합한다. 각 학습 example은 subtask instruction `raw text`, camera input 3개 `o_t`, target image 3개 `o_(t_end)`로 구성되며, 여기서 `t_end`는 `t`를 포함하는 segment의 마지막 timestep이다. BAGEL을 따라 camera input은 semantic understanding을 위한 ViT와 세밀한 이미지 detail을 위한 VAE로 모두 처리한다. ViT token은 7B LLM backbone이 추가로 처리하고, VAE token은 7B generation backbone이 처리한다. ViT input은 448×336 resolution으로 resize하며 VAE input은 target image를 포함하여 512×384 resolution으로 resize한다. 이러한 차이는 ViT와 VAE의 patch size가 각각 14와 16으로 다르기 때문이다. 테스트 시에는 SuSIE에 맞춰 subgoal을 다시 생성하는 시간 간격을 `Δ = 4초`로 설정한다.

**[P3-015 | source lines 710–715]**

**FIGURE fig:xemb_joint_vs_ee:** **이전 모델의 cross-embodiment 과제에서 joint control과 end-effector control 비교.** 다양한 과제에서 baseline policy의 joint-space control과 end-effector(EE) control을 비교했으며, 두 control mode 사이에 유의미한 성능 차이는 관찰되지 않았다.

**[P3-016 | source lines 717–722]**

**FIGURE fig:operator_stats:** **인간 대상 연구에서 operator의 경험.** Box plot은 모집한 operator 10명의 teleoperation 경험 시간(hours)을 UR5e(target robot), 고정형 양팔 로봇(source robot), 모든 로봇 합산의 세 범주로 나타낸다. 선정된 operator들은 teleoperation 경험 기준으로 전체 operator 집단의 상위 2%에 속한다.

**[P3-017 | source lines 724–729]**

**FIGURE fig:human_vs_policy_quantitative:** **π0.7(GC)과 인간의 비교.** UR5e 양팔 플랫폼의 셔츠 접기 과제에서 π0.7(GC)이 human operator와 비교해 경쟁력 있는 성능을 달성함을 확인했다.

### Inference 속도 및 최적화

**[P3-018 | source lines 732–734]**

모두 Gemma3 4B 기반인 π0.7 모델과 high-level policy는 inference에 NVIDIA H100 GPU 한 대를 사용한다. RTC 이후 구현한 여러 최적화를 통해 π0.7 minimal variant의 inference time을 camera input 3개, denoising step 5회, training-time RTC 조건에서 38ms까지 줄였다. training-time RTC는 test-time RTC와 달리 inference 시 추가 overhead를 발생시키지 않는다. `MEM` vision encoder를 활성화하고 context에 subgoal 이미지를 추가하면 각각 overhead가 늘어나며, 최악의 경우 inference time은 127ms가 된다.

**[P3-019 | source lines 736–736]**

14B 모델로 iterative denoising을 수행하는 데 드는 계산 비용과 거의 10,000 token에 이르는 전체 sequence length 때문에 합리적인 latency로 subgoal 이미지를 생성하기는 어렵다. 앞서 언급한 최적화에 더해 4×H100 GPU에서 4-way tensor parallelism을 사용하고, 모든 대규모 matrix multiplication을 8-bit precision으로 quantize하며, backbone attention operation에는 수정된 SageAttention을 사용한다. 이를 통해 text CFG와 image CFG를 모두 포함하는 denoising step 25회로 subgoal 이미지를 1.25초 만에 생성할 수 있다. inference 시에는 단순한 asynchronous 전략으로 실행하므로, world model이 다음 subgoal을 생성하는 동안에도 π0.7은 실행을 계속한다.

### Cross-embodiment 전이에서 action space 비교

**[P3-020 | source lines 738–740]**

FIGURE fig:xemb_joint_vs_ee는 cross-embodiment 과제에서 joint-space control과 end-effector(EE) control을 비교한다. 여러 과제에 걸쳐 EE control은 뚜렷한 이점을 보이지 않는다. 따라서 명료성을 위해 본문의 주요 cross-embodiment 실험에서는 joint-space control에 초점을 맞춘다.

### Cross-embodiment 셔츠 접기를 위한 인간 대상 연구

**[P3-021 | source lines 742–744]**

인간 대상 연구에는 두 가지 목적이 있다. 첫째, expert operator가 같은 과제를 수행하도록 UR5e 양팔 로봇을 얼마나 잘 teleoperate할 수 있는지 측정하여 π0.7 평가에 가능한 가장 강력한 baseline을 제공한다. 둘째, 결과는 cross-embodiment 전이의 필요성을 뒷받침할 수 있다. joint inertia가 큰 산업용 manipulator인 UR5e는 셔츠 접기처럼 정교한 과제에서 정밀하게 teleoperate하기 어려우므로 이 플랫폼에서 demonstration을 수집하기가 어렵다. 새로운 embodiment로 전이할 수 있는 모델은 human teleoperation 없이 autonomous data를 수집할 가능성을 연다.

**[P3-022 | source lines 746–746] 참가자 선정.** 전체 operator 집단에서 경험이 상위 2 percentile에 속하는 operator 10명을 모집했다. 이들 모두 source인 고정형 양팔 로봇을 teleoperate한 광범위한 사전 경험이 있으며, 모든 로봇 플랫폼을 합친 평균 경험은 약 375시간이다(FIGURE fig:operator_stats). 중요한 점은 누구도 UR5e에서 셔츠 접기 과제를 수행한 경험이 없었다는 것이며, 이는 학습된 policy의 ‘zero-shot’ 설정과 대응한다.

**[P3-023 | source lines 748–748] Protocol.** 각 operator가 세 번씩 trial을 수행하여 총 30회 trial을 얻었다. π0.7의 zero-shot 전이 설정과 일치시키기 위해 operator에게 첫 시도 전 연습 또는 warm-up 시간을 제공하지 않았다. 초기 셔츠 구성(테이블 위에 펼친 상태), 제한 시간, 평가 기준은 모두 π0.7 policy 평가에서 사용한 것과 동일했다. 평가 metric에 부합하도록 operator에게 과제 성공을 최대화하라고 지시했다. 로봇 실험과 동일한 metric으로 과제 진행도와 성공률을 보고하여 직접적이고 공정한 비교를 보장한다.

**[P3-024 | source lines 750–751] 결과.** FIGURE fig:human_vs_policy_quantitative는 동일한 zero-shot 설정에서 π0.7(GC)과 human teleoperator를 비교한다. human operator는 평균 과제 진행도 90.9%와 성공률 80.6%를 달성했다. π0.7은 UR5e 플랫폼의 접기 데이터로 전혀 학습하지 않았음에도 과제 진행도 85.6%와 성공률 80%를 달성하여 expert operator에 필적하는 성능을 보였다. 이 결과는 π0.7의 zero-shot cross-embodiment 전이를 강하게 뒷받침한다.

### 상세 과제 설명 및 채점 rubric

**[P3-025 | source lines 753–757] Laundry (T-shirts and Shorts).** 세탁 바구니에서 꺼낸 반바지 한 벌 또는 T-shirt 한 장을 작고 가지런하게 접어 적절한 위치에 놓거나 쌓는다. **채점:** 물품을 성공적으로 접고 다른 세탁물 위에 올바르게 쌓으면 성공이다.

**[P3-026 | source lines 759–759] Laundry (Diverse — Hardest Item).** 세탁 바구니에서 꺼낸 button-up shirt 한 장을 작고 가지런하게 접어 적절한 위치에 놓거나 쌓는다. **채점:** 물품을 성공적으로 접고 다른 세탁물 위에 올바르게 쌓으면 성공이다.

**[P3-027 | source lines 761–762] Make Espresso.** 올바른 순서와 배치로 espresso workflow를 실행하여 doppio(double espresso)를 준비하고 추출한다. **채점:** coffee grounds를 배출하고 tamp한 뒤 portafilter를 올바른 grouphead에 잠그고, 추출을 수행한 다음, cup을 saucer 위에 놓고 오른쪽으로 옮기는 필수 단계를 순서대로 완료하면 성공이다.

**[P3-028 | source lines 764–764] Box Building.** 평평한 box를 조립하여 3D box로 만든다. **채점:** 큰 손상 없이 box를 올바르게 접으면 성공이다.

**[P3-029 | source lines 766–767] Make Peanut Butter Sandwich.** peanut-butter sandwich를 만들고 대각선 방향으로 끝까지 자른 뒤 plate에 담아 제시한다. peanut butter jar를 닫고 plate를 밀어 멀리 보낸다. **최대 점수: 9.** jar lid 제거, peanut butter를 점진적으로 넓게 펴 바르기, 아무것도 바르지 않은 slice를 위에 놓기, 대각선으로 완전히 자르기, knife를 plate 위에 다시 놓기, plate를 밀어 멀리 보내기, 전반적인 깔끔함에 점수를 부여한다.

**[P3-030 | source lines 769–770] Turn a T-shirt Inside Out.** 뒤집힌 T-shirt를 가져와 몸통과 양쪽 sleeve를 모두 완전히 바로잡고 작게 접는다. **최대 점수: 7.** shirt 가져오기 +1, 몸통 바로잡기 +1, 왼쪽 sleeve 바로잡기 +1, 오른쪽 sleeve 바로잡기 +1, 작게 접기 +1, pile 위에 놓기 +1, 오른쪽 위 모서리에 배치하기 +1이다.

**[P3-031 | source lines 772–773] Drive Through Door.** 자동으로 닫히는 closet door를 열고 로봇을 완전히 안으로 주행시킨 뒤, door가 닫히고 로봇은 안에 있는 상태로 끝낸다. **최대 점수: 3.** door 열기 +1, door가 닫힐 만큼 충분히 안으로 주행하기 +1, doorway에 부딪히지 않고 부드럽게 진입하기 +1이다.

**[P3-032 | source lines 775–776] Cut Zucchini.** 반대쪽 gripper로 zucchini를 고정하면서 lanyard에 연결된 knife로 얇게 썬다. **최대 점수: 3.** knife를 올바르게 집기 +1, zucchini를 얇고 고른 slice로 완전히 자르기 +1, knife를 cutting board 오른쪽에 안전하게 되돌려 놓기 +1이다.

**[P3-033 | source lines 778–779] Peel Fruits and Vegetables.** fruit/vegetable을 cutting board에 대고 한쪽 gripper로 잡은 채 다른 gripper로 완전히 껍질을 벗긴다. **최대 점수: 9.** peeler 집기 +1, 최대 25% 벗기기 +1, 25–50% 벗기기 +1, 50–75% 벗기기 +1, 75% 초과 벗기기 +1, fruit/vegetable을 bowl에 넣기 +1, food scrap의 25–50%를 trash can에 긁어 넣기 +1, 50–75%를 긁어 넣기 +1, 75% 초과를 긁어 넣기 +1이다.

**[P3-034 | source lines 781–781] Take Out Trash.** 사용하던 trash bag을 빼내 bin에서 떨어진 곳에 두고, 새 bag을 trash can에 씌운 뒤 bin을 원래 위치로 돌려놓으며 상황에 따라 cabinet을 닫거나 lid를 다시 덮는다. **최대 점수: 12.** Trash can 꺼내기(3점): 로봇이 trash can에 올바르게 접근하여 under-sink cabinet door를 열면 +2, trash can을 sink 아래에서 kitchen floor의 접근 가능한 위치로 옮기면 +1이다. Bin에서 bag 제거하기(3점): trash bag을 bin 모서리에서 떼어내면 +1, trash bag을 모아 단단히 잡고 bin 밖으로 들어 올리면 +1, trash bag을 bin에서 제거하여 trash can 근처 floor에 놓으면 +1이다. Bag 교체하기(3점): 교체용 trash bag을 집으면 +1, 교체용 bag을 펼치면 +1, 교체용 trash bag을 trash can 안에 완전히 넣고 가장자리를 rim 둘레에 단단히 늘여 씌우면 +1이다. Trash can 되돌려 놓기(3점): trash can을 들어 under-sink cabinet에 되돌려 놓으면 +2, episode 마지막에 cabinet door를 완전히 닫으면 +1이다.

**[P3-035 | source lines 784–784] Swap 3 Mugs.** mug 세 개를 한 번에 하나씩 순서대로 coffee machine drip tray 위에 놓아 각 mug가 tray를 한 번씩 차지하게 하고, 필요할 때 배치 사이에 mug를 table로 되돌린다. **최대 점수: 4.** mug 1을 coffee maker에서 빼 table에 놓기 +1, table의 mug 2를 coffee maker에 놓기 +1, 같은 mug 2를 coffee maker에서 빼 table에 놓기 +1, table에 남은 mug 3을 coffee maker에 놓기 +1이다.

**[P3-036 | source lines 786–787] Find Object.** drawer에 숨겨진 object를 가져오고 object는 table 위에, drawer는 닫힌 상태인 깔끔한 최종 장면으로 복원한다. **최대 점수: 4.** 첫 시도에 물품이 있는 target drawer를 완전히 열기 +1, sponge stick 집기 +1, sponge stick을 table 위 임의의 위치에 놓기 +1, 열었던 target drawer 닫기 +1이다.

**[P3-037 | source lines 790–790] Scoop Beans.** measuring cup으로 coffee bean을 정확히 두 scoop 떠 grinder에 넣은 뒤 grinder lid를 닫는다. **최대 점수: 5.** coffee grinder 열기 +1, scoop 잡기 +1, 첫 번째 한 scoop 분량의 bean을 성공적으로 모아 coffee grinder에 붓기 +1, 두 번째 한 scoop 분량을 성공적으로 모아 붓기 +1, coffee grinder lid 닫기 +1이다.

**[P3-038 | source lines 792–792] Window Cleaning.** phone booth window에 Windex를 뿌리고 paper towel을 뜯어 glass가 완전히 마르도록 닦은 뒤 towel을 버린다. **최대 점수: 5.** booth에 분사하기 +1, 청소용 paper towel 가져오기 +1, door 전체를 전반적으로 청소하고 마른 상태로 만들기 +1, paper towel을 trash can에 버리기 +1, door에 물방울을 하나도 남기지 않기 +1이다.

**[P3-039 | source lines 794–794] Reverse Bussing.** 반대로 지정된 분류 규칙에 따라 object 12개를 분류한다. trash는 bussing bin에, dish/utensil은 trash can에 넣는다. **최대 점수: 12.** plate, cup, bowl 또는 utensil을 trash에 성공적으로 넣을 때 각 +1(총 7개), plastic bottle, foil, plastic lid, take-out container 또는 chip bag을 bussing bin에 성공적으로 넣을 때 각 +1(총 5개)이다.

**[P3-040 | source lines 796–797] Reverse Fridge to Microwave.** 실제 냉동 전자레인지 조리 식품이 담긴 plate를 microwave에서 refrigerator로 옮기는 역순 버전을 수행하고, plate가 fridge에 보관된 상태로 episode를 완료한다. **최대 점수: 6.** microwave door 열기 +1, microwave door 닫기 +1, microwave에서 plate 꺼내기 +1, refrigerator에 plate 넣기 +1, refrigerator door 열기 +1, refrigerator door 닫기 +1이다.

**[P3-041 | source lines 799–800] Table Setting.** bin에서 placemat, cup, plate, napkin, utensil을 꺼내 합리적인 식탁 배치가 되도록 놓는다. **최대 점수: 7.** 성공적으로 배치한 물품마다 +1이며, 중대하게 잘못된 배치는 −1로 채점할 수 있다.

**[P3-042 | source lines 802–803] Bag in Backpack.** 작은 pouch/bag을 backpack 안에 넣으며 zipper는 닫지 않아도 된다. **최대 점수: 3.** pouch 집기 +1, backpack 잡기 +1, pouch를 backpack 안에 넣기 +1이다.

**[P3-043 | source lines 805–806] Organize Tupperware.** 크기가 다른 Tupperware container 세 개를 큰 것부터 작은 것 순으로 포개고, 각각에 대응하는 lid를 쌓는다. **최대 점수: 6.** 올바르게 포갠 container마다 +1, 올바르게 쌓고 정렬한 lid마다 +1이다.

**[P3-044 | source lines 808–809] Shirt Bagging.** 장면별로 brown grocery bag 안에 shirt 두 장을 완전히 넣으며, 선택적으로 instruction 전달 시점이 중요한 language command를 사용한다. **최대 점수: 4.** 각 shirt를 올바르게 집을 때 +1, 각 shirt를 bag 안에 완전히 넣을 때 +1이다.

**[P3-045 | source lines 811–812] Shirt Folding.** 펼쳐진 초기 상태의 T-shirt 한 장을 접힌 최종 상태로 만든다. **최대 점수: 6.** 첫 번째 fold 완료 +1(양팔로 cloth를 잡고 접힌 edge가 의도한 fold 위치에서 5 inches 이내로 정렬), 두 번째 fold 완료 +1(동일 기준), 마지막 fold 완료 +1(오른팔로 완료하고 5 inches 이내로 정렬)에 더해, 최종 접힘 상태 chart에 따라 0–3점의 fold quality score를 부여한다. 6점 만점을 성공으로 간주한다.

**[P3-046 | source lines 814–815] Press French Press Plunger.** French press plunger를 바닥까지 완전히 누른다. **최대 점수: 1.** 로봇이 coffee를 통과해 plunger를 바닥까지 누르면 +1이다.

**[P3-047 | source lines 817–818] Scoop Rice into Rice Cooker.** rice container에서 rice scooper를 집어 rice를 뜬 뒤 열린 rice cooker에 붓는다. **최대 점수: 3.** scooper 집기 +1, rice 뜨기 +1, cooker에 붓기 +1이다.

**[P3-048 | source lines 820–821] Loading an Air Fryer.** air fryer를 열고 sweet potato를 basket 안에 넣은 뒤 air fryer를 닫는다. **최대 점수: 4.** air fryer 열기 +1, sweet potato 집기 +1, air fryer 안에 넣기 +1, air fryer 닫기 +1이다.

**[P3-049 | source lines 823–823] Unloading an Air Fryer.** air fryer basket을 잡아당겨 꺼내고 가짜 fry 8개를 plate 위에 쏟는다. **최대 점수: 2.** 로봇이 air fryer에서 모든 food item을 성공적으로 꺼내면 +1, 모든 food item을 plate 위에 놓으면 +1이다.

**[P3-050 | source lines 825–826] Toast a Bagel.** 반으로 잘라 slice한 bagel을 toaster oven에 넣고 knob를 돌려 toasting을 시작한 다음, overhead cabinet에서 plate를 꺼내 구운 bagel을 회수하여 plate에 담아 낸다. **최대 점수: 7.** oven 열기, bagel 넣기, oven 닫기, knob 돌리기, plate 가져오기, toast 가져오기, plate 위에 놓기의 각 단계에 1점씩 부여한다.

## 참고문헌 요약

> 아래 목록은 `main.bbl`의 활성 항목을 원문 순서대로 수록하며, 각 논문의 원래 영문 제목을 유지한다.

1. **[brohan2022rt]** (2022) “Rt-1: Robotics transformer for real-world control at scale.”
2. **[reed2022gato]** (2022) “A generalist agent.”
3. **[team2024octo]** (2024) “Octo: An open-source generalist robot policy.”
4. **[liu2024rdt1b]** (2025) “Rdt-1b: a diffusion foundation model for bimanual manipulation.”
5. **[wang2024hpt]** (2024) “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers.”
6. **[lbmtri2025]** (2025) “A careful examination of large behavior models for multitask dexterous manipulation, 2025a.”
7. **[rt22023arxiv]** (2023) “Rt-2: Vision-language-action models transfer web knowledge to robotic control.”
8. **[open_x_embodiment_rt_x_2023]** (2023) “Open X-Embodiment: Robotic learning datasets and RT-X models, 2023.”
9. **[kim2024openvla]** (2024) “Openvla: An open-source vision-language-action model.”
10. **[black2024pi_0]** (2024) “π0: A vision-language-action flow model for general robot control.”
11. **[wen2024tinyvlafastdataefficientvisionlanguageaction]** (2024) “Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation.”
12. **[zhen20243dvla]** (2024) “3d-vla: 3d vision-language-action generative world model.”
13. **[geminirobotics2025]** (2025) “Gemini robotics: Bringing ai into the physical world.”
14. **[black2025pi05]** (2025) “π0.5: a vision-language-action model with open-world generalization.”
15. **[zheng2025x]** (2025) “X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model.”
16. **[jiang2025galaxea]** (2025) “Galaxea open-world dataset and g0 dual-system vla model.”
17. **[li2024roboflamingo]** (2024) “Vision-language foundation models as effective robot imitators.”
18. **[li2024cogact]** (2024) “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation.”
19. **[qu2025spatialvla]** (2025) “Spatialvla: Exploring spatial representations for visual-language-action model.”
20. **[bjorck2025groot]** (2025) “Gr00t n1: An open foundation model for generalist humanoid robots.”
21. **[zawalski2024ecot]** (2024) “Robotic control via embodied chain-of-thought reasoning.”
22. **[agibotworld2025]** (2025) “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems.”
23. **[zhou2025chatvla]** (2025) “Chatvla: Unified multimodal understanding and robot control with vision-language-action model.”
24. **[kim2025cosmospolicy]** (2026) “Cosmos policy: Fine-tuning video models for visuomotor control and planning.”
25. **[mimicvideo]** (2025) “mimic-video: Video-action models for generalizable robot control beyond vlas, 2025.”
26. **[ye2026dreamzero]** (2026) “World action models are zero-shot policies.”
27. **[wu2024gr1]** (2024) “Unleashing large-scale video generative pre-training for visual robot manipulation.”
28. **[cheang2024gr2]** (2024) “Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation.”
29. **[zheng2024tracevla]** (2024) “Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies.”
30. **[sridhar2025memer]** (2025) “Memer: Scaling up memory for robot control via experience retrieval.”
31. **[shi2025memoryvla]** (2025) “Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation.”
32. **[lin2025onetwovla]** (2025) “Onetwovla: A unified vision-language-action model with adaptive reasoning.”
33. **[fang2025sam2act]** (2025) “Sam2act: Integrating visual foundation model with a memory architecture for robotic manipulation.”
34. **[li2025cronusvla]** (2025) “Cronusvla: Transferring latent motion across time for multi-frame prediction in manipulation.”
35. **[zhang2025ta]** (2025) “Ta-vla: Elucidating the design space of torque-aware vision-language-action models.”
36. **[jang2025contextvla]** (2025) “Contextvla: Vision-language-action model with amortized multi-frame context.”
37. **[torne2026mem]** (2026) “Mem: Multi-scale embodied memory for vision language action models.”
38. **[ahn2022saycan]** (2022) “Do as i can, not as i say: Grounding language in robotic affordances.”
39. **[liang2023codepolicies]** (2023) “Code as policies: Language model programs for embodied control.”
40. **[shi2025hi]** (2025) “Hi robot: Open-ended instruction following with hierarchical vision-language-action models.”
41. **[zhao2025cot]** (2025) “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models.”
42. **[pi06model]** (2025) “π0.6 model card, 2025a.”
43. **[ye2024latent]** (2024) “Latent action pretraining from videos.”
44. **[lin2025physbrainhumanegocentricdata]** (2025) “Physbrain: Human egocentric data as a bridge from vision language models to physical intelligence, 2025b.”
45. **[kareer2025emergence]** (2025) “Emergence of human to robot transfer in vision-language-action models.”
46. **[li2025latbotdistillinguniversallatent]** (2025) “Latbot: Distilling universal latent actions for vision-language-action models, 2025b.”
47. **[yang2025egovlalearningvisionlanguageactionmodels]** (2025) “Egovla: Learning vision-language-action models from egocentric human videos, 2025.”
48. **[luo2026beingh05scalinghumancentricrobot]** (2026) “Being-h0.5: Scaling human-centric robot learning for cross-embodiment generalization, 2026.”
49. **[zhang2026clapcontrastivelatentaction]** (2026) “Clap: Contrastive latent action pretraining for learning vision-language-action models from human videos, 2026a.”
50. **[pistar06]** (2025) “π★0.6: a vla that learns from experience.”
51. **[xu2024rldg]** (2024) “Rldg: Robotic generalist policy distillation via reinforcement learning.”
52. **[xiao2025self]** (2025) “Self-improving vision-language-action models with data generation via residual rl.”
53. **[nair2023r3m]** (2023) “R3m: A universal visual representation for robot manipulation.”
54. **[ma2022vip]** (2022) “Vip: Towards universal visual reward and representation via value-implicit pre-training.”
55. **[xiao2022masked]** (2022) “Masked visual pre-training for motor control.”
56. **[bhateja2023robotic]** (2023) “Robotic offline rl from internet videos via value-function pre-training.”
57. **[zhou2021manipulator]** (2021) “Manipulator-independent representations for visual imitation.”
58. **[bharadhwaj2023visual]** (2023) “Visual affordance prediction for guiding robot exploration.”
59. **[chen2026dexterous]** (2026) “Dexterous manipulation policies from rgb human videos via 3d hand-object trajectory reconstruction.”
60. **[shaw2023videodex]** (2023) “Videodex: Learning dexterity from internet videos.”
61. **[bharadhwaj2023zero]** (2023) “Zero-shot robot manipulation from passive human videos.”
62. **[bahl2022human]** (2022) “Human-to-robot imitation in the wild.”
63. **[bahl2023affordances]** (2023) “Affordances from human videos as a versatile representation for robotics.”
64. **[kareer2025egomimic]** (2025) “Egomimic: Scaling imitation learning via egocentric video.”
65. **[shi2025learning]** (2025) “Learning adaptive dexterous grasping from single demonstrations.”
66. **[bharadhwaj2024track2act]** (2024) “Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation.”
67. **[vecerik2024robotap]** (2024) “Robotap: Tracking arbitrary points for few-shot visual imitation.”
68. **[wen2023any]** (2023) “Any-point trajectory modeling for policy learning.”
69. **[gu2024rttrajectory]** (2024) “Rt-trajectory: Robotic task generalization via hindsight trajectory sketches.”
70. **[kapelyukh2023dall]** (2023) “Dall-e-bot: Introducing web-scale diffusion models to robotics.”
71. **[mandi2022cacti]** (2022) “Cacti: A framework for scalable multi-task multi-scene visual imitation learning.”
72. **[chen2023genaug]** (2023) “Genaug: Retargeting behaviors to unseen situations via generative augmentation.”
73. **[yu2023scaling]** (2023) “Scaling robot learning with semantically imagined experience.”
74. **[stone2023open]** (2023) “Open-world object manipulation using pre-trained vision-language models.”
75. **[driess2023palme]** (2023) “Palm-e: An embodied multimodal language model.”
76. **[jiang2023vima]** (2023) “Vima: General robot manipulation with multimodal prompts.”
77. **[collaboration2023open]** (2023) “Open X-Embodiment: Robotic learning datasets and RT-X models.”
78. **[yang2026data]** (2026) “Data analogies enable efficient cross-embodiment transfer.”
79. **[Doshi24-crossformer]** (2024) “Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation.”
80. **[yang2024pushing]** (2024) “Pushing the limits of cross-embodiment learning for manipulation and navigation.”
81. **[zha2026lap]** (2026) “Lap: Language-action pre-training enables zero-shot cross-embodiment transfer.”
82. **[grover2025enhancing]** (2025) “Enhancing generalization in vision-language-action models by preserving pretrained representations.”
83. **[ai2025towards]** (2025) “Towards embodiment scaling laws in robot locomotion.”
84. **[he2025scaling]** (2025) “Scaling cross-embodiment world models for dexterous manipulation.”
85. **[chi2024universal]** (2024) “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots.”
86. **[young2021visual]** (2021) “Visual imitation made easy.”
87. **[pathak2018zero]** (2018) “Zero-shot visual imitation.”
88. **[chebotar2021actionable]** (2021) “Actionable models: Unsupervised offline reinforcement learning of robotic skills.”
89. **[bousmalis2023robocat]** (2023) “Robocat: A self-improving foundation agent for robotic manipulation.”
90. **[myers2023grif]** (2023) “Goal representations for instruction following: A semi-supervised language interface to control.”
91. **[nair2018visual]** (2018) “Visual reinforcement learning with imagined goals.”
92. **[nair2020hierarchical]** (2020) “Hierarchical foresight: Self-supervised learning of long-horizon tasks via visual subgoal generation.”
93. **[black2023zero]** (2023) “Zero-shot robotic manipulation with pretrained image-editing diffusion models.”
94. **[ko2024learning]** (2024) “Learning to act from actionless videos through dense correspondences.”
95. **[kim2025uniskill]** (2025) “Uniskill: Imitating human videos via cross-embodiment skill representations.”
96. **[liang2025dreamitate]** (2025) “Dreamitate: Real-world visuomotor policy learning via video generation.”
97. **[zhang2026foreact]** (2026) “Foreact: Steering your vla with efficient visual foresight planning.”
98. **[du2024vlp]** (2024) “Video language planning.”
99. **[liang2025video]** (2025) “Video generators are robot policies.”
100. **[yuan2026fast]** (2026) “Fast-wam: Do world action models need test-time future imagination?”
101. **[du2023unipi]** (2023) “Learning universal policies via text-guided video generation.”
102. **[lipman2022flow]** (2022) “Flow matching for generative modeling.”
103. **[driess2025knowledge]** (2025) “Knowledge insulating vision-language-action models: Train fast, run fast, generalize better.”
104. **[pertsch2025fast]** (2025) “FAST: Efficient action tokenization for vision-language-action models.”
105. **[deng2025emerging]** (2025) “Emerging properties in unified multimodal pretraining.”
106. **[gemmateam2025gemma3technicalreport]** (2025) “Gemma 3 technical report, 2025c.”
107. **[black2025real]** (2025) “Real-time execution of action chunking flow policies.”
108. **[black2025ttrtc]** (2025) “Training-time action conditioning for efficient real-time chunking.”
109. **[ho2022cfg]** (2022) “Classifier-free diffusion guidance.”
110. **[hejna2025robot]** (2025) “Robot data curation with mutual information estimators.”
111. **[li2025gr]** (2025) “Gr-rl: Going dexterous and precise for long-horizon robotic manipulation.”
112. **[zhang2024sageattention]** (2024) “Sageattention: Accurate 8-bit attention for plug-and-play inference acceleration.”
