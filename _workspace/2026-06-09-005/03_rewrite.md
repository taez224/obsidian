# Targeted Humanize Suggestions

원문 전체를 다시 쓰기보다는, AI 티가 강하게 잡힌 지점만 국소 수정하는 것이 적절합니다. 아래는 의미를 바꾸지 않는 범위의 권장 치환입니다.

## 1. Heading Emphasis

Before:

```markdown
## **AI 시대의 병목은 작성이 아니라 흡수다**
### **Reviewability: 판단 가능성**
```

After:

```markdown
## AI 시대의 병목은 작성이 아니라 흡수다
### Reviewability: 판단 가능성
```

## 2. Evidence Density

Before:

```markdown
DORA의 Generative AI 연구도 비슷한 신호를 보입니다. AI 사용 증가는 개인 생산성에는 긍정적인 효과를 줄 수 있지만, AI adoption이 25% 증가할 때 delivery throughput은 1.5%, delivery stability는 7.2% 낮아지는 상관관계가 관찰됐습니다.
```

After:

```markdown
DORA 연구도 같은 방향의 신호를 보입니다. AI 사용이 개인 생산성에는 도움이 되더라도, 조직의 배포 성과까지 자동으로 끌어올리지는 않았습니다.
```

## 3. PR Enumeration

Before:

```markdown
첫째, **AI 초안과 사람이 확인한 범위를 나눠 남겨야 합니다.**
둘째, **판단 근거와 실행 결과가 PR 안에서 이어져야 합니다.**
셋째, **리뷰어에게 맥락 복원까지 떠넘기지 않아야 합니다.**
```

After:

```markdown
- **AI 초안과 사람이 확인한 범위를 나눠 남깁니다.**
- **판단 근거와 실행 결과가 PR 안에서 이어지게 합니다.**
- **리뷰어에게 맥락 복원까지 떠넘기지 않습니다.**
```

## 4. Conclusion Rhythm

Before:

```markdown
더 중요한 질문은 이것에 가깝습니다.
```

After:

```markdown
질문은 이쪽에 가까워야 합니다.
```

## 5. Final Phrase

Before:

```markdown
형식은 작아도 됩니다. 중요한 것은 하나입니다.

이 변경이 팀이 책임질 수 있는 상태로 들어오는가.
```

After:

```markdown
형식은 작아도 됩니다. 결국 볼 것은 하나입니다. 이 변경이 팀이 책임질 수 있는 상태로 들어오는가.
```
