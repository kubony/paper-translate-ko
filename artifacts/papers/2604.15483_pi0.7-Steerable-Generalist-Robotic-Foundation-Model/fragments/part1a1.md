[P1A-001 | 원문 176–178행]
## 초록

[P1A-002 | 원문 177–177행]
광범위한 scenario에서 강력한 out-of-the-box 성능을 발휘할 수 있는 새로운 로봇 파운데이션 모델 π0.7을 제시한다. π0.7은 다양한 주방 기기를 사용하는 multi-stage task를 포함하여 보지 못한 environment에서 다양한 언어 instruction을 따를 수 있고, 예를 들어 해당 task를 이전에 본 적 없는 로봇이 빨래를 개도록 하는 zero-shot cross-embodiment generalization을 제공하며, 별도의 준비 없이 espresso machine을 조작하는 것과 같은 까다로운 task를 훨씬 더 전문화된 RL-finetuned model에 필적하는 성능으로 수행한다. π0.7의 핵심 아이디어는 학습 중 다양한 context conditioning을 사용하는 것이다. Prompt에 담긴 이 conditioning 정보를 통해 모델이 서로 다른 전략으로 여러 task를 수행하도록 정밀하게 조정할 수 있다. 모델은 무엇을 해야 하는지 설명하는 언어 명령뿐만 아니라, task 성능에 관한 metadata와 subgoal image를 포함하여 이를 수행할 방식 또는 전략까지 설명하는 추가 multimodal 정보에도 conditioning된다. 이로써 π0.7은 demonstration, 실패를 포함할 수 있는 잠재적으로 suboptimal한 (자율) 데이터, 비로봇 출처의 데이터 등 매우 다양한 데이터를 사용할 수 있다. 실험에서는 속도와 dexterity, 언어 instruction 준수, compositional task generalization이 요구되는 수많은 task에 걸쳐 여러 로봇 platform에서 π0.7을 평가한다.

[P1A-003 | 원문 182–182행]
## 1. 서론

[P1A-004 | 원문 184–185행]
> *나는 내가 만났던 모든 것의 일부다.*  
> — Alfred, Lord Tennyson, *Ulysses*

[P1A-005 | 원문 187–187행]
파운데이션 모델은 크고 다양한 dataset으로 학습하면 generalist capability가 출현한다는 원리에 기반한다. 예를 들어 large language model은 사실과 semantic knowledge를 기억할 수 있을 뿐만 아니라, 그 지식을 새로운 방식으로 조합하여 좀처럼 연결되지 않을 법한 요소가 필요한 문제를 해결하고, 사용자가 정의한 형식(예: JSON)을 적용하며, chain-of-thought reasoning을 수행할 수도 있다.

[P1A-006 | 원문 188–188행]
이러한 종류의 *compositional* generalization은 generalist capability의 초석이라 할 수 있지만, physical intelligence 영역에서는 좀처럼 달성되지 않았다. Vision-Language-Action(VLA, 비전-언어-액션) model과 같은 로봇 파운데이션 모델은 규모와 capability 면에서 크게 발전했지만, 새로운 task로 generalization하거나 skill을 새로운 방식으로 재조합하는 능력은 지금까지 제한적이었다. 학습 데이터에서 서로 다른 capability를 조합해 새로운 문제를 해결할 수 있는 language model과 달리, 기존 VLA는 새로운 task를 해결하는 능력이 부족할 뿐 아니라 task-specific fine-tuning 없이는 학습했던 모든 instruction을 능숙하게 수행하는 데에도 흔히 어려움을 겪는다.

[P1A-007 | 원문 190–190행]
본 논문에서는 compositional generalization의 강한 징후를 보이는 새로운 모델 π0.7을 제시한다. 이 모델은 다양한 언어 instruction을 따르고, dexterous task에서 더 전문화된 fine-tuned model에 필적하는 성능을 달성하며, 나아가 이러한 behavior를 새로운 방식으로 조합할 수도 있다. 이는 다양한 전략을 사용하는 여러 로봇의 데이터, 자율 실행에서 얻은 suboptimal 데이터(RL post-trained agent의 데이터와 실패 사례 모두 포함), 사람이 task를 수행하는 video 및 인터넷의 일반 multimodal 데이터와 같은 비로봇 데이터 등 크고 다양한 dataset을 활용함으로써 가능해진다. 그러나 이러한 데이터를 단순하게 사용하는 것만으로는 성공할 수 없다. 전략과 task 성능이 모두 서로 다른 다양한 example을 사용하는 단순한 학습 과정은 dataset의 상이한 mode를 평균화하고 suboptimal한 결과를 생성하는 모델로 이어진다. π0.7 학습에서는 *무엇을* 해야 하는지뿐만 아니라 *어떻게* 해야 하는지에 관한 정보까지 담은 상세한 context annotation을 데이터에 부여하고, 다양한 multimodal conditioning signal을 사용해 이 지식을 모델에 제공함으로써 이 문제를 해결한다. 이 방식에서 각 episode는 로봇에게 세밀한 concept과 skill을 가르치며, 로봇은 이를 사용해 학습 task를 효과적으로 수행할 뿐만 아니라 새로운 방식으로 조합하여 새로운 task를 해결할 수도 있다. 제안하는 prompt 구조는 상세한 언어 label, strategy metadata, subgoal image와 같은 multimodal 정보를 포함한다. 이를 통해 크고 다양한 dataset의 모호성을 해소하고, 성능을 저하하지 않으면서 suboptimal behavior로부터 학습하며, instruction, embodiment, environment 전반에 걸친 폭넓은 generalization을 달성할 수 있다.

[P1A-008 | 원문 192–192행]
상세한 prompt 또는 context가 파운데이션 모델의 성능을 향상할 수 있다는 아이디어는 다른 분야에서도 연구되었다. 예를 들어 image 및 video generation model은 고품질 결과물을 생성하기 위해 *prompt expansion*을 활용한다. 본 접근법은 이러한 방법과 여러 면에서 유사하다. 그러나 robotics에서는 데이터에 더 상세한 텍스트로 단순히 *captioning*하는 것만으로는 충분하지 않다. Task의 성공과 숙련도를 결정하는 세부 사항은 더 미묘할 수 있고(예: episode의 전반적 품질에 관한 정보), 언어만으로 표현하기가 어려울 수도 있기 때문이다(예: 깔끔하게 접힌 티셔츠의 구체적인 외관). 따라서 모델은 더 상세한 텍스트를 사용할 뿐만 아니라 Figure fig:teaser와 같이 episode 품질에 관한 정보(strategy metadata), 로봇이 사용한 control modality, subgoal image를 비롯한 다양한 추가 metadata를 prompt에 더한다. 이 정보 중 일부는 test time에 제공하거나 생략할 수 있지만, 학습에 포함하면 모델이 학습한 concept을 더 효과적으로 조합하고 다양한 emergent capability를 나타낼 수 있다.

[P1A-009 | 원문 194–194행]
평가를 통해 π0.7이 기존 로봇 파운데이션 모델을 넘어서는 다음과 같은 여러 capability를 보인다는 것을 입증한다.

[P1A-010 | 원문 195–196행]
- **Out-of-the-box 성능:** π0.7은 task-specific post-training 없이도 다양한 environment에서 espresso machine 사용, 빨래 개기, 쓰레기봉투 꺼내기, 상자 접기, 채소 껍질 벗기기와 같이 높은 dexterity가 필요한 long-horizon task를 안정적으로 수행할 수 있다.

[P1A-011 | 원문 197–197행]
- **Instruction generalization:** π0.7은 보지 못한 environment에서 다양한 언어 instruction을 따를 수 있으며, 복잡하고 보지 못한 언어 reference에 대한 강건한 generalization을 보여준다. 예를 들어 π0.7은 전혀 보지 못한 주방과 침실 environment에서 다양한 open-ended instruction을 따를 수 있다.

[P1A-012 | 원문 198–198행]
- **Cross-embodiment generalization:** π0.7은 zero-shot cross-embodiment transfer를 가능하게 한다. 이에 따라 빨래를 개는 task를 한 번도 학습하지 않은 로봇으로 티셔츠 접기와 같은 dexterous task를 transfer할 수 있으며, 로봇을 teleoperation하는 expert operator의 최초 시도와 동등한 성능을 달성한다.

[P1A-013 | 원문 199–200행]
- **Compositional task generalization:** π0.7은 이전에 보지 못한 방식으로 skill을 조합하여 새로운 task를 수행하도록 instruction할 수 있다. 예를 들어 π0.7에 고구마를 air fryer에 넣는 것과 같이 새로운 주방 기기를 사용하도록 prompt하거나, task를 새로운 방식으로 수행하도록 prompt할 수 있다.

[P1A-014 | 원문 201–201행]
Ablation 및 scaling study를 통해 다양한 dataset과 상세한 context 사이에 강한 synergy가 있음을 실증적으로도 입증한다. 본 접근법은 모델 성능을 저하하지 않으면서 품질이 혼재된 데이터와 비표준 데이터 출처로부터 학습할 수 있게 하며, 학습 중 상세한 context 정보가 제공되면 다양한 데이터가 모델 성능을 높인다.
