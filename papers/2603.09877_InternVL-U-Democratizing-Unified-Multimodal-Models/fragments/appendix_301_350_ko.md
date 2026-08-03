<!-- source: sections/appendix.tex:301-337 -->

```json
{
  "score": {
    "Q1": 5,
    "Q2": 1,
    "Q3": 2,
    "Q4": 5,
    "Q5": 4
  },
  "reason": {
    "Q1": "대상 텍스트 'PARTY'의 철자가 정확하고 명확하게 읽힌다. 제거하도록 지정된 대상 텍스트('MUSIC')는 잔상 없이 완전히 사라졌다.",
    "Q2": "모델이 대상이 아닌 텍스트를 광범위하게 훼손했다. 'NIGHT CLUB', '31 OCT', 'FREE DRINKS', 'LIVE', 'PRICE'가 모두 잘못 삭제되었으며, '10$'는 환각으로 생성된 텍스트 '1TY'로 변형되었다.",
    "Q3": "전체 장면의 무결성이 심각하게 훼손되었다. 마라카스를 들고 있던 해골의 팔이 지워져 마라카스가 공중에 떠 있는 모습이 되었으며, 이로 인해 삽화의 물리적 논리가 무너졌다.",
    "Q4": "의미적 실패에도 불구하고 이미지의 기술적 품질은 매우 뛰어나다. 경계가 선명하고 배경 인페인팅이 매끄러우며, 눈에 띄는 픽셀 아티팩트나 흐림, 노이즈가 없다.",
    "Q5": "'PARTY'에 선택된 글꼴 스타일은 포스터의 손으로 그린 듯한 벡터 미학과 잘 어우러진다. 다만 색상은 원본 텍스트의 선명한 빨간색보다 더 어두운 적갈색이다."
  }
}
```

![세로형 평가 예시](figures/appendix/eval_example_vertical.pdf)

JSON 블록 외부에는 어떠한 마크다운이나 대화형 텍스트도 출력하지 않는다.

<!-- source: sections/appendix.tex:339-341 -->

**그림: 평가 프롬프트의 후속 부분.** 마지막 평가 차원(Q5)과 결과 파싱에 필요한 엄격한 JSON 출력 스키마를 자세히 보여준다.

<!-- source: sections/appendix.tex:344-347 -->

### MiniSet-500 결과

오픈 소스 커뮤니티에 가볍고 표준화된 평가 하위 집합을 제공하기 위해 전체 TextEdit 벤치마크에서 **MiniSet-500**을 구축한다. 시나리오 유형 전반에 걸쳐 균형 잡힌 분포를 보장하도록 18개 하위 범주 각각에서 인스턴스를 무작위로 샘플링해 구성한다. MiniSet-500은 총 **500개의 이미지 편집 쌍**을 포함하며, 과제의 다양성은 유지하면서 평가 비용을 크게 줄인다. 이는 신속한 벤치마킹과 절제 연구를 위한 효율적인 프로토콜로 활용되며, 종합 평가에는 전체 벤치마크가 여전히 표준으로 사용된다. 표 `exp_textedit_rule_miniset`과 표 `miniset-textedit-mllm`에는 MiniSet-500 TextEdit 벤치마크에서 여러 모델이 보인 성능을 보고한다.

<!-- table source: tables/final/textedit-rule-miniset -->
<!-- table source: tables/final/textedit-mllm-miniset -->

<!-- source: sections/appendix.tex:349-350 -->

<div style="page-break-after: always;"></div>

## 데이터 구축 세부 사항
