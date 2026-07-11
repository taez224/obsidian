---
title: 기술 블로그
created: 2026-07-10
project_id: blog
status: active
started: 2026-06-10
ended: null
tags:
  - 프로젝트/blog
  - blog
---

# 기술 블로그

개인 경험과 엔지니어링 판단을 발행 가능한 글로 정리하는 프로젝트다.

## 발행 글

![[20_Projects/blog/_index.base#📰 발행 글]]

## 현재 작업

![[20_Projects/blog/_index.base#✍️ 작성 중]]

## 운영 원칙

- 글마다 작업 정본은 하나만 유지한다.
- 발행을 마친 반복본은 `40_Archive/blog-drafts/`로 보낸다.
- 글의 상태는 각 글의 frontmatter에서 관리하고, 이 노트는 프로젝트 전체의 상태만 관리한다.

## 블로그 글 메타데이터

- 공통: `title`, `created`, `tags`, `status`, `author`, `summary`, `related`
- 이미 외부에 발행한 글: `publication`, `source`를 추가하고, 원문 발행일을 확인할 수 있을 때만 `published`를 기록한다.
- 연재 글: `series`, `series_order`를 추가하고 앞·뒤 글만 `related`로 연결한다.
- 태그는 `blog`와 주제 태그 1~2개까지만 둔다. 플랫폼명·발행 상태·연재 여부는 태그 대신 속성이나 `related`로 관리한다.
