# 번역 산출물 인덱스

폴더명은 `<식별자>_<Title-Slug>` 규칙을 따른다(SKILL.md '폴더명 규칙').
웹 출처 폴더에는 원문 영상이 `assets/`에 함께 보관된다.

## 논문 (arXiv·학회) (10편)

- [CANVAS: Commonsense-Aware Navigation System for Intuitive Human-Robot Interaction](papers/2410.01273_CANVAS-Commonsense-Aware-Navigation-System/) — 8쪽 · VLN, navigation, robotics
- [CostNav: A Navigation Benchmark for Real-World Economic-Cost Evaluation of Physical AI Agents](papers/2511.20216_CostNav-Navigation-Benchmark-for-Economic-Cost/) — 27쪽 · benchmark, navigation, physical-AI
- [D2E: Scaling Vision-Action Pretraining on Desktop Data for Transfer to Embodied AI](papers/2510.05684_D2E-Scaling-Vision-Action-Pretraining-on-Desktop-Data/) — 18쪽 · VLA, pretraining, robotics
- [Describe Anything Anywhere At Any Moment (DAAAM)](papers/2512.00565_Describe-Anything-Anywhere-At-Any-Moment/) — 16쪽 · perception, captioning, SLAM
- [Ground Slow, Move Fast: A Dual-System Foundation Model for Generalizable Vision-and-Language Navigation](papers/2512.08186_Ground-Slow-Move-Fast-Dual-System-VLN/) — 12쪽 · VLN, foundation-model, navigation
- [HABIT: Human-Aware Behavior and Interaction Training Dataset for Robot Manipulation](papers/2606.31682_HABIT-Human-Aware-Behavior-and-Interaction-Training/) — 25쪽 · dataset, manipulation, HRI
- [KOFFVQA: An Objectively Evaluated Free-form VQA Benchmark for Large Vision-Language Models in the Korean Language](papers/2503.23730_KOFFVQA-Korean-Free-form-VQA-Benchmark/) — 7쪽 · benchmark, VLM, Korean
- [Large Language Models Develop Novel Social Biases Through Adaptive Exploration](papers/2511.06148_LLMs-Develop-Novel-Social-Biases-via-Adaptive-Exploration/) — 43쪽 · LLM, bias, cognitive-science
- [SC3-Eval: 자기일관적 비디오 생성을 통한 로봇 파운데이션 모델 평가](papers/SC3-Eval_Self-Consistent-Video-Generation-for-Robot-FM-Eval/) — 14쪽 · evaluation, video-generation, robotics
- [π0.7: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities](papers/pi07_Steerable-Generalist-Robotic-Foundation-Model/) — 29쪽, 영상 26개 · VLA, foundation-model, robotics

## 웹 아티클 (4편)

- [ACT-2 Preview: Generalizing Reliability](web/2026-07-17_Sunday-Robotics_ACT-2-Preview-Generalizing-Reliability/) — 9쪽, 영상 2개 · blog, manipulation, robotics
- [CMU Vision-Language-Navigation Challenge 2026](web/2026-07-22_CMU_Vision-Language-Navigation-Challenge-2026/) — 9쪽, 영상 3개 · challenge, VLN, navigation
- [Claude plays robotics](web/2026-07-09_Anthropic_Claude-plays-robotics/) — 22쪽, 영상 3개 · blog, LLM, robotics
- [Solving Dexterity: A Full-Stack Approach](web/2026-07-16_mimic-robotics_Solving-Dexterity-A-Full-Stack-Approach/) — 14쪽, 영상 13개 · blog, dexterous-manipulation, hardware

## 웹사이트 아카이브 (1편)

- [Physical Intelligence (π) — Research, Blog & Public Website Archive](sites/2026-07-26_pi.website_Physical-Intelligence-Site-Archive/) — 95쪽, 영상 321개 · website-archive, VLA, robotics

## 자산 보관 정책

웹 출처 번역은 원문 영상을 함께 보관한다(SKILL.md '미디어 자산 정책').
수집본이 커서(전체 3GB 이상) 대용량 파일은 Git LFS 대신 GCS에 두고,
저장소에는 매니페스트(`assets/videos.json`)·한국어 캡션·썸네일·작은 파일만 둔다.
각 PDF 말미의 「부록. 원문 영상 자산」에서 썸네일과 링크를 확인할 수 있다.

## 파일 무결성

`MANIFEST.csv`에 각 PDF의 쪽수·크기·SHA-256과 자산 개수가 기록되어 있다.
