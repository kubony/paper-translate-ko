### 표 20. 오픈소스 텍스트 생성·편집 벤치마크 비교

| Benchmark | Type | Size | Human Filter | GT Ann. | Sub-class | Traditional Eval. | LLM Eval. |
|---|---|---:|:---:|:---:|---:|:---:|:---:|
| AnyText | Text Generation | 2,000 | ✗ | ✗ | – | ✓ | ✗ |
| LongText | Text Generation | 320 | ✓ | ✗ | 8 | ✗ | ✓ |
| CVTG-2K | Text Generation | 2,000 | ✓ | ✗ | 2 | ✓ | ✗ |
| MARIO-Eval-edit | Text Edit | 4,000 | ✗ | ✗ | – | ✓ | ✗ |
| **TextEdit (본 연구)** | Text Edit | **2,148** | ✓ | ✓ | **18** | ✓ | ✓ |

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
