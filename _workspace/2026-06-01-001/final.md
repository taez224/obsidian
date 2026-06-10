---
title: "AI 활용 격차를 팀 역량으로 바꾸려면"
created: 2026-05-31
tags:
  - blog
  - AI
  - 개발/도구
  - 소프트웨어공학
status: draft
author: TaeZ
summary: "AI 활용 수준은 개발자마다 다르게 나타난다. 팀이 할 일은 모두를 같은 방식으로 맞추는 것이 아니라, 각자의 AI 활용을 설명과 검증, 기록과 학습으로 회수해 팀의 역량으로 바꾸는 일이다."
---

# AI 활용 격차를 팀 역량으로 바꾸려면

![AI가 양산한 코드 중 일부만 검토와 회수를 거쳐 팀 지식이 되고, 나머지는 이해 부채로 쌓였다가 나중에 비용으로 돌아오는 삽화](assets/2026-05-ai-cost/recovery-rate-hero.png)

AI 코딩 도구를 팀에 도입하면 처음에는 도구 사용률이 보인다. 누가 얼마나 쓰는지, 어떤 모델을 쓰는지, 에이전트를 몇 번 돌렸는지, PR이 얼마나 빨리 나오는지 같은 숫자는 비교적 쉽게 잡힌다.

그런데 실제 현장에서 더 크게 벌어지는 것은 사용량이 아니라 사용 방식의 차이다.

AI를 자동완성처럼 쓰는 개발자가 있다. 설계 대안을 비교하는 상대로 쓰는 개발자도 있다. 테스트 초안을 뽑는 데 강한 사람도 있고 디버깅 가설을 세우는 데 잘 쓰는 사람도 있다. 반대로 어디까지 맡겨도 되는지 감을 잡지 못해 결과를 그대로 받아들이거나 아예 불신해서 거의 쓰지 않는 경우도 있다.

이 차이를 개인의 센스나 성실함으로만 두면 팀 안의 격차는 더 커진다. 잘 쓰는 사람은 더 빨라지고, 익숙하지 않은 사람은 더 조심스러워진다. 같은 도구를 쓰고 있어도 누군가는 사고를 확장하고 누군가는 판단을 외주화한다.

그래서 AI 활용은 개인기가 아니라 팀의 문제다.

## AI 활용 격차는 개인 문제로만 남겨둘 수 없다

AI를 잘 쓰는 법을 개인이 익혀야 한다는 말은 맞다. 하지만 그 말만으로는 충분하지 않다. 팀에서 만드는 소프트웨어는 개인 작업의 합이 아니라 공유된 이해 위에서 움직이는 시스템이기 때문이다.

개발자마다 강점도 다르다. 누군가는 도메인 맥락을 잘 붙잡고 누군가는 테스트 경계를 잘 본다. 빠르게 초안을 만드는 사람이 있는가 하면 미묘한 설계 냄새를 잘 맡는 사람도 있다. AI를 잘 쓰는 방식도 이 성향을 따라 달라진다.

팀이 해야 할 일은 모든 개발자를 같은 프롬프트 방식으로 맞추는 것이 아니다. 각자가 자기 역량과 성향에 맞게 AI를 쓰되, 그 결과가 팀의 품질 기준과 지식 체계 안으로 들어오게 만드는 것이다.

좋은 AI 활용은 개인의 생산성에서 끝나지 않는다. 팀이 다시 이해할 수 있어야 하고 검증할 수 있어야 하며 다음 사람이 이어받을 수 있어야 한다.

## 산출물은 자동으로 팀 역량이 되지 않는다

AI가 만든 코드는 저장소에 들어간다. 하지만 저장소에 들어갔다고 팀의 지식이 되지는 않는다.

외부에서 들어온 지식은 언제나 변환 과정을 거친다. 예제 코드는 우리 버전과 맞아야 하고 테스트는 우리 실패 조건을 설명해야 하며 설계 판단은 우리 시스템의 경계와 맞아야 한다. 이 과정을 거치지 않으면 산출물은 남아도 팀의 이해는 남지 않는다.

경영학에서 말하는 흡수역량도 결국 이 문제와 닿아 있다. 바깥에서 들어온 지식을 조직 안에서 쓸 수 있는 자산으로 바꾸는 능력. AI 코딩에서도 핵심은 비슷하다. 모델이 만든 결과를 팀이 다시 설명하고 검증하고 다음 사람이 쓸 수 있는 형태로 바꾸어야 한다.

그래서 나는 AI 활용도를 볼 때 생성량보다 회수율을 보고 싶다.

회수율은 AI가 만든 산출물이 설명 가능한 지식, 검증 가능한 테스트, 공유 가능한 문서, 재사용 가능한 판단으로 얼마나 전환되었는지를 보는 기준이다.

- 더 나은 코드가 남았는가.
- 더 정확한 테스트가 남았는가.
- 더 명확한 설계 판단이 남았는가.
- 다음 사람이 이해할 수 있는 문서가 남았는가.
- 개발자가 다음 문제를 더 잘 풀 수 있게 되었는가.

남은 것이 없다면 그것은 학습이 아니라 소비다.

## 회수하지 못한 비용은 부채가 된다

AI가 만든 코드는 겉으로는 깔끔해 보일 수 있다. 이름도 그럴듯하고 구조도 정돈돼 있고 설명도 붙어 있다. 그래서 부채가 줄어든 것처럼 보인다.

하지만 설명할 수 없는 코드가 늘어난다면 부채는 사라진 것이 아니다. 위치를 옮겼을 뿐이다.

개인에게는 이해 부채로 쌓인다. 결과는 소유했지만 판단 근거는 소유하지 못한 상태다. 커밋에는 이름이 남아 있지만 그 코드가 어떤 가정과 제약 위에서 만들어졌는지 설명하지 못한다.

팀에게는 인지 부채로 쌓인다. 한 사람이 설명하지 못하는 변경은 작은 빈틈처럼 보일 수 있다. 그러나 그런 변경이 반복되면 코드베이스는 깔끔해 보여도 시스템이 왜 그렇게 움직이는지 설명할 수 있는 공유 모델은 약해진다.

장기적으로는 역량 부채도 생긴다. 결과는 빨리 만들지만 문제를 분해하고 원인 가설을 세우고 실패를 통해 범위를 좁히는 경험이 줄어든다. 장애나 큰 변경 앞에서야 그 비용이 드러난다.

이 부채는 개인의 부족함만으로 생기지 않는다. 팀이 무엇을 설명해야 하는지, 어디까지 검증해야 하는지, 어떤 판단을 남겨야 하는지 합의하지 않았을 때 더 쉽게 쌓인다.

## 팀에는 얇은 하네스가 필요하다

AI 활용을 개인의 성실함에만 맡기면 오래가지 않는다. 바쁜 날에는 설명을 줄이고 테스트를 줄이고 검토를 나중으로 미룬다. 그래서 팀에는 얇은 하네스가 필요하다.

하네스는 거창한 프로세스가 아니다. AI가 만든 결과가 팀의 품질 기준 안으로 다시 들어오게 만드는 최소한의 장치다.

설명 루프는 AI가 만든 코드를 자기 언어로 다시 말하게 만든다. PR 설명에는 “무엇을 바꿨는가”만이 아니라 “왜 이렇게 바꿨는가”도 남긴다.

검증 루프는 성공 조건보다 실패 조건을 먼저 보게 만든다. 어떤 입력에서 깨지는지, 어떤 테스트가 보장하지 못하는지, 롤백은 가능한지를 확인한다.

학습 루프는 AI가 해결한 문제를 그냥 닫지 않게 만든다. 다음에 비슷한 문제를 만나면 어떤 단서부터 볼 것인지 한 줄이라도 남긴다.

여기서 목표는 통제가 아니라 회수다. PR 템플릿, 테스트, 실행 로그, 리뷰 규칙은 AI를 느리게 만들기 위한 장치가 아니다. 개인이 끌어낸 AI의 결과물을 팀의 지식 체계 안으로 회수하기 위한 장치다.

회수하면 지식이 되고 방치하면 슬롭이 된다.

## 같은 방식으로 쓰게 만들 필요는 없다

조직 차원의 AI 활용이라고 하면 쉽게 표준화부터 떠올린다. 어떤 도구를 쓸지 정하고 어떤 프롬프트를 공유할지 문서화하고 어떤 워크플로를 따를지 합의한다. 이런 기준은 필요하다. 하지만 기준이 너무 빨리 개인의 사용 방식을 덮어버리면 AI의 장점도 줄어든다.

AI는 사람마다 다른 방식으로 역량을 끌어낸다. 구현이 빠른 사람에게는 비교 대상과 반례를 더해 줄 수 있다. 설계 감각이 좋은 사람에게는 대안을 넓혀 줄 수 있다. 디버깅에 강한 사람에게는 가설을 더 빨리 펼치게 해 준다. 문서화에 강한 사람에게는 팀의 암묵지를 밖으로 꺼내게 해 준다.

팀이 해야 할 일은 이 차이를 없애는 것이 아니라 안전하게 증폭시키는 것이다.

그러려면 개인의 AI 활용을 평가할 때 “얼마나 많이 썼는가”만 보면 안 된다. 그 사람이 AI를 통해 어떤 판단을 더 잘하게 되었는지, 어떤 반복 작업을 줄였는지, 어떤 지식을 팀에 남겼는지를 함께 봐야 한다.

AI 역량은 프롬프트를 잘 쓰는 기술만이 아니다. 자신의 강점과 약점을 알고, 어떤 작업을 맡기고 어떤 판단은 직접 붙잡아야 하는지 아는 감각에 가깝다. 그 감각은 혼자서만 키우기보다 팀 안에서 피드백과 사례를 통해 더 빨리 자란다.

## 기록은 통제가 아니라 다음 사람을 위한 맥락이다

앞으로는 커밋 이력도 조금 달라져야 할지 모른다. 지금 Git에는 주로 누가 언제 어떤 메시지로 변경했는지가 남는다. AI가 만든 변경이 늘어난다면 그것만으로는 부족하다.

어떤 모델이 어떤 맥락을 보고 어떤 권한 안에서 수정했는지. 사람이 어디를 승인했으며 어떤 검증을 통과했는지. 최소한 PR이나 커밋 단위에서는 이런 판단의 계보를 추적할 수 있어야 한다.

이 방향은 완전히 새로운 상상만은 아니다. GitHub Copilot의 agent session log나 Linux kernel의 AI-assisted contribution 안내처럼 코드 diff 바깥의 맥락을 남기려는 크고 작은 시도는 이미 나오고 있다. 아직 표준은 아니지만 문제의식은 흩어져 나타나고 있다.

프롬프트나 컨텍스트를 그대로 남기자는 뜻은 아니다. 민감한 정보가 섞일 수 있기 때문이다. 필요한 것은 “AI가 썼다”는 면책 표시가 아니라, 나중에 문제가 생겼을 때 그 판단이 어디서 왔는지 따라갈 수 있는 구조다.

![AI 시대의 커밋 이력이 모델, 프롬프트 참조, 컨텍스트, 권한, 승인, 테스트를 함께 남기는 모습을 상상한 삽화](assets/2026-05-ai-cost/future-git-provenance.png)

_앞으로의 커밋 이력은 코드뿐 아니라 판단의 계보도 남겨야 할지 모른다._

## 팀의 AI 역량은 회수율로 드러난다

AI 도구는 앞으로 더 많은 코드를 더 빠르게 만든다. 더 긴 맥락을 읽고 더 복잡한 변경을 제안하고 지금은 어렵게 느껴지는 작업도 당연하게 자동화한다.

그럴수록 팀의 질문은 단순해져야 한다.

더 많이 만들었는가보다 무엇이 남았는가.  
더 빨리 머지했는가보다 다음 사람이 이해할 수 있는가.  
AI를 얼마나 많이 썼는가보다 그 사용이 팀의 지식으로 회수됐는가.

AI 시대의 개발팀은 구성원 모두를 같은 방식으로 만들 필요가 없다. 오히려 각자의 역량과 성향에 맞는 AI 활용을 끌어내야 한다. 다만 그 결과가 개인의 작업 속도에만 머물지 않고 팀의 설명, 검증, 학습, 이력으로 남게 만들어야 한다.

그때 AI 활용은 개인기가 아니라 팀의 역량이 된다.

---

## 참고 문헌

- Edsger W. Dijkstra, ["On the cruelty of really teaching computing science"](https://www.cs.utexas.edu/~EWD/transcriptions/EWD10xx/EWD1036.html) (EWD 1036, 1988)
- Cohen & Levinthal, ["Absorptive Capacity: A New Perspective on Learning and Innovation"](https://www.jstor.org/stable/2393553) (1990)
- Sreecharan Sankaranarayanan, ["Mitigating 'Epistemic Debt' in Generative AI-Scaffolded Novice Programming using Metacognitive Scripts"](https://arxiv.org/abs/2602.20206) (arXiv 2602.20206, 2026; ACM L@S '26)
- Judy Hanwen Shen & Alex Tamkin, ["How AI Impacts Skill Formation"](https://arxiv.org/abs/2601.20245) (arXiv 2601.20245 / Anthropic Research, 2026)
- Margaret-Anne Storey, ["From Technical Debt to Cognitive and Intent Debt: Rethinking Software Health in the Age of AI"](https://arxiv.org/abs/2603.22106) (arXiv 2603.22106, 2026)

<!-- HUMANIZE-SUMMARY v2.0.0
run_id: 2026-06-01-001
mode: focused-refresh
genre: blog
rewritten_length: 5694
metrics_risk_band: low
metrics_risk_score: 2
high_signal_metrics:
  - conclusion_pivot_count: 0
  - safe_balance_count: 0
  - ending_comma_rate: reduced after comma-chain cleanup
category_counts_after:
  - company_blog_focus: centered on team-level AI capability
  - personal_skill_framing: reduced
  - comma_chain_residue: none found by targeted rg pattern
self_check: 6/6
quality_grade: A
highlights:
  - Reframed the article from usage metrics to AI capability gaps inside teams.
  - Added the argument that teams should draw out each developer's AI strengths instead of forcing one usage style.
  - Kept recovery rate as the operating lens rather than the opening thesis.
  - Connected harness, records, and review loops to organizational learning rather than individual diligence.
residual_findings:
  - Reference list remains because this version targets a company technical blog.
-->
