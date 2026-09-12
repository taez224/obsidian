---
created: 2026-09-06
slug: rss-to-github-profile
summary: 가든이 글 종류별로 내는 RSS 피드를 프로필 저장소의 GitHub Actions가 읽어 README 목록을 갱신하는 구성이다.
tags:
  - 개발/도구
---

# RSS 피드로 GitHub 프로필 갱신하기

## RSS가 하는 일

RSS는 웹사이트의 새 콘텐츠를 다른 프로그램이 읽을 수 있도록 제공하는 XML 기반 형식이다. [RSS 2.0 명세](https://www.rssboard.org/rss-specification#whatIsRss)에서 풀 이름은 **Really Simple Syndication**이다. 여기서 syndication은 같은 콘텐츠를 여러 곳에서 받아 보여줄 수 있도록 배포한다는 뜻이다.

사이트가 글의 제목·주소·날짜·요약 등을 피드로 제공하면, RSS 리더나 자동화 프로그램이 그 주소를 읽어 새 항목을 확인한다. 사람이 웹페이지를 방문해 새 글을 찾는 대신 프로그램이 목록을 가져오는 방식이다. 피드에 요약만 담을 수도 있고 본문을 담을 수도 있다.

## 언제 어떻게 쓰는가

블로그나 뉴스처럼 새 콘텐츠가 계속 추가되는 사이트를 구독할 때 쓴다. 여러 사이트의 피드 주소를 RSS 리더에 등록하면 한곳에서 새 글을 모아 읽을 수 있다. 사이트마다 화면 구조가 달라도 리더는 같은 RSS 형식을 읽으면 된다.

글 목록을 다른 곳에 표시하는 자동화에도 쓸 수 있다. 웹페이지의 HTML을 분석해 제목과 링크를 찾아내는 대신, 피드에 들어 있는 항목을 가져와 최근 글 목록을 만들거나 알림으로 전달한다.

일반적인 RSS 리더는 피드 주소를 주기적으로 재조회한다. 사이트가 피드를 갱신했다고 모든 구독 화면이 즉시 바뀌는 것은 아니고, 피드를 구독하는 프로그램의 조회 주기에 따라 달라진다.

## 공개 목록을 담는 피드

나는 이 사이트에 새로운 노트나 글이 등록될 때마다 [내 GitHub 프로필 페이지의 최근 글 목록](https://github.com/taez224#%EC%B5%9C%EA%B7%BC-%EB%82%A8%EA%B8%B4-%EA%B8%80%EA%B3%BC-%EC%83%9D%EA%B0%81) 이 갱신되도록  RSS를 연결했다.

이 사이트의 RSS 파일은 CI에서 Astro가 [[생각의 정원을 만들고 배포하는 과정|사이트를 빌드할 때]] 웹페이지와 RSS 파일을 함께 만들게 된다.

| 피드 | 담는 내용 |
| --- | --- |
| `/rss.xml` | 발행한 글·생각 노트·개발 노트 |
| `/feeds/posts.xml` | 발행한 글 |
| `/feeds/notes.xml` | 생각 노트 |
| `/feeds/dev.xml` | 개발 노트 |

> [!example]- 글 피드에 실린 항목 하나
> ```xml
> <item>
>   <title>AI Agent 시대의 Human Agency</title>
>   <link>https://www.nextree.io/ai-agent-sidaeyi-human-agency/</link>
>   <pubDate>Mon, 24 Aug 2026 15:00:00 GMT</pubDate>
>   <category>글</category>
>   <description>AI와 함께 SSE 구현을 다듬는 동안 잘 돌아간다는 증거는 쌓였지만, 계속 써야 하는지는 실행만으로 판단할 수 없었다.</description>
> </item>
> ```

처음엔 그냥 통합 피드 하나만 뒀다가 GitHub 프로필에서 각 카테고리 별 최신글을 보여주고 싶어서 피드를 나눴다.

## GitHub Actions의 프로필 갱신

[프로필 저장소의 워크플로](https://github.com/taez224/taez224/blob/main/.github/workflows/garden-posts.yml)는 글 피드에서 최근 2개, 생각 노트와 개발 노트 피드에서 각각 최근 1개를 가져오도록 설정했다. 매일 예약 실행하며 필요할 때 수동으로도 실행할 수 있다.

README 수정에는 [blog-post-workflow](https://github.com/gautamkrishnar/blog-post-workflow)를 사용한다. README에 글·생각 노트·개발 노트 목록을 넣을 영역을 주석으로 지정하고, 액션에 각 피드 주소와 표시할 개수를 넘긴다. 액션은 그 영역만 바꾸므로 소개 문구와 나머지 내용은 유지된다.

아래처럼 피드 주소와 주석 영역과 템플릿을 지정하면 README.md 에 반영된다.

```yaml
- name: Update Thinking Garden posts
  uses: gautamkrishnar/blog-post-workflow@v1
  with:
    feed_list: "https://taez224.github.io/feeds/posts.xml"
    max_post_count: 2
    comment_tag_name: "GARDEN-POST-LIST"
    template: "- [글] [$title]($url)$newline"
```

```markdown
<!-- GARDEN-POST-LIST:START -->
- [글] [AI Agent 시대의 Human Agency](https://www.nextree.io/ai-agent-sidaeyi-human-agency/)
- [글] [AI로 빨라진 개인, 소화하지 못하는 팀](https://www.nextree.io/airo-bbalrajin-gaein-sohwahaji-moshaneun-tim/)
<!-- GARDEN-POST-LIST:END -->
```

사이트는 공개할 목록을 만들고, 프로필의 워크플로는 그 목록을 읽어 항목을 보여준다. 별도 API 서버 없이 배포된 RSS 파일을 사이에 두고 두 작업을 연결한 구성이다.
