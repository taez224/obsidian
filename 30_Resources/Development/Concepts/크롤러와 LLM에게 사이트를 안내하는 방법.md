---
created: 2026-09-10
slug: machine-readable-outputs
summary: robots.txt와 사이트맵, llms.txt, 구조화 데이터가 기계 독자에게 각각 무엇을 알리고, 이 사이트는 그중 무엇에 기대를 걸지 않는가.
tags:
  - 개발/설계
---

# 크롤러와 LLM에게 사이트를 안내하는 방법

이 사이트(가든)에 robots.txt와 사이트맵을 두고, 구조화 데이터와 llms.txt를 뒤이어 붙였다. 넣고 나니 각각이 크롤러에게 무엇을 약속하는지 분명하지 않았다. 넷을 나눠 보면 robots.txt는 접근 규칙을, 사이트맵과 llms.txt는 사이트에 무엇이 있는지 알리는 목록을, 구조화 데이터는 각 페이지가 무엇인지 알리는 표기를 맡는다.

## 크롤러 접근 규칙

robots.txt는 크롤러에게 어느 경로를 요청해도 되는지 알리고 사이트맵의 위치를 함께 적는다. 가든의 robots.txt는 모든 경로를 허용하고 사이트맵 위치만 가리킨다. 비공개 노트는 빌드에서 빠지므로 크롤러에게 가려야 할 경로가 남지 않는다.

> [!warning] robots.txt의 한계
> robots.txt는 크롤러에게 보내는 요청이지 접근을 차단하는 수단이 아니다. 막아야 할 경로가 생기면 robots.txt에 적기 전에 그 경로를 공개 대상에서 먼저 뺀다.

## 같은 목록의 서로 다른 독자

사이트맵과 llms.txt와 RSS는 모두 사이트에 무엇이 있는지 알리는 목록인데, 읽는 독자가 서로 달라서 형식도 달라진다.

| 출력 | 독자 | 담는 것 |
|------|------|---------|
| `sitemap.xml` | 검색 크롤러 | 공개 URL 전체. 기계가 파싱하는 XML |
| `llms.txt` | LLM 크롤러 | 종류별 목록과 한 줄 요약. 사람도 읽는 Markdown |
| `rss.xml` | 사람 구독자 | 최근 항목만 |

## 구조화 데이터와 schema.org

HTML만으로는 `<h1>`이 글 제목인지 사이트 이름인지 기계가 알 수 없다. 그래서 페이지마다 제목·저자·발행일을 schema.org 어휘로 JSON-LD에 따로 적는다.

가든은 홈에 `WebSite`, 발행한 글에 `BlogPosting`, 개발 노트에 `TechArticle`, 소개 페이지에 `AboutPage`, 나머지에 `WebPage`를 쓴다. 타입은 구체적일수록 페이지가 무엇인지 더 정확히 알리므로, 맞는 타입이 있으면 `WebPage`보다 그쪽을 쓴다.

## 화면에 없는 정보의 위험

구조화 데이터에는 페이지가 이미 가진 제목·요약·날짜·주소만 넣는다. 값이 없으면 빈 문자열을 넣지 않고 필드 자체를 만들지 않는다. Google은 화면에 보이지 않는 내용을 구조화 데이터로 표시하지 말라고 하며, 어기면 리치 결과로 표시되지 않거나 스팸으로 분류될 수 있다고 밝힌다.^[Google Search Central, [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)의 Quality guidelines 절.]

## llms.txt의 채택 상태

llms.txt는 [Jeremy Howard가 2024년 9월에 제안](https://llmstxt.org/)했고 아직 표준이 아니다.

Google은 2026년 6월에 갱신한 AI 최적화 안내에서 llms.txt를 검색에 쓰지 않으며 검색에 노출되려고 별도의 기계 판독 파일을 만들 필요도 없다고 밝혔다.^[Google Search Central, [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)의 "Mythbusting generative AI search: what you don't need to do" 절. 2026년 6월 15일 갱신은 [문서 업데이트 이력](https://developers.google.com/search/updates)에 있다.] 서버 로그를 공개한 실험들에서도 AI 크롤러가 llms.txt를 요청한 경우는 드물었다.^[OtterlyAI, [llms.txt and AI Visibility: Results from OtterlyAI's GEO Study](https://otterly.ai/blog/the-llms-txt-experiment/), 2026. 사이트 한 곳의 90일 로그에서 AI 크롤러 요청 6만 2천여 건 중 84건(0.1%)이 llms.txt였다. wislr, [AI Bot Traffic Is Accelerating Fast. 48 Days of Server Logs Expose What GPTBot, ChatGPT, ClaudeBot, and 16 Others Are Doing.](https://www.wislr.com/articles/ai-bot-behavior-log-analysis/), 2026. 사이트 한 곳의 48일 로그에서 봇 요청 12,099건 중 llms.txt 요청은 없었다.]

OpenAI와 Anthropic이 자사 개발자 문서에 llms.txt를 두고 있지만, 그렇다고 그 모델들이 탐색할 때 다른 사이트의 llms.txt를 꼭 읽는다는 것은 아니다.

그래도 가든은 llms.txt를 둔다. 빌드 과정에서 함께 생성되는 출력이라 따로 관리가 필요하지 않고, 사이트맵과 달리 사람이 열어도 읽히는 목록이라 그 자체로 쓸 데가 있다. 다만 아직 널리 활용되진 않으므로 이 파일에 검색 노출이나 인용 빈도를 기대하지는 않는다.

## 두지 않은 파일

`ai.txt`는 두지 않았다. `ai.txt`는 학습 데이터 사용을 거절하는 용도인데, 가든은 공개를 전제로 쓴 글만 올리므로 거절할 내용이 없다. 그럴듯해 보인다는 이유로 파일을 미리 채우지 않고, 필요한 이유가 생길 때 더한다.

## 배포 산출물 검사

이 출력들은 화면에 보이지 않아서 템플릿을 고치다가 메타 태그 한 줄이 빠져도 페이지는 멀쩡해 보인다. 그래서 빌드 뒤 산출물 검사에 넣었다. 모든 페이지에 구조화 데이터가 있는지, llms.txt가 제목과 절과 절대 주소를 갖췄는지, 피드가 모두 나왔는지를 확인하고 하나라도 어긋나면 배포하지 않는다.

## 확인 범위

llms.txt의 채택에 관한 판단은 공개된 조사와 Google의 발표에 근거한 것이고, 이 사이트에서 실제로 누가 llms.txt를 가져갔는지는 확인하지 못한다. 정적 호스팅에서는 액세스 로그를 받지 못하고, 방문 통계는 브라우저에서 동작하기 때문에 크롤러의 파일 요청을 세지 않는다.

## 연관된 노트

- [[정적 사이트의 OG 카드와 방문 통계]]: 공유 이미지도 페이지 밖으로 나가는 출력이지만 독자가 사람이라 만드는 방식과 검증 기준이 다르다.
- [[RSS 피드로 GitHub 프로필 갱신하기]]: 피드를 종류별로 나누고 종류마다 항목 수를 정한 이유.
- [[생각의 정원을 만들고 배포하는 과정]]: 빌드가 노트를 읽어 사이트로 배포하는 전체 흐름.
