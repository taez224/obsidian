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

## 연재 관리

![[20_Projects/blog/_index.base#📚 시리즈 현황]]

![[20_Projects/blog/_index.base#⏳ 연재 점검]]

## 발행 글

![[20_Projects/blog/_index.base#📰 발행 글]]

## 현재 작업

![[20_Projects/blog/_index.base#✍️ 작성 중]]

## 운영 원칙

- 글마다 작업 정본은 하나만 유지한다.
- 발행을 마친 반복본은 `40_Archive/blog-drafts/`로 보낸다.
- 글의 상태는 각 글의 frontmatter에서 관리하고, 이 노트는 프로젝트 전체의 상태만 관리한다.
- 아웃라인·집필 계약 같은 관리 문서에는 `blog` 태그와 `status`를 두지 않는다. Base는 발행 원고만 센다.
- 연재 상태는 연재명과 같은 허브 노트에서 관리한다. Base의 공백 경고는 점검 신호이며 `on-hold`·`completed` 전환은 직접 판단한다.

## 블로그 글 메타데이터

- 공통: `title`, `created`, `tags`, `status`, `author`, `summary`, `related`
- 이미 외부에 발행한 글: `publication`, `source`를 추가하고, 원문 발행일을 확인할 수 있을 때만 `published`를 기록한다.
- 연재 글: `series`, `series_order`를 추가하고 앞·뒤 글만 `related`로 연결한다.
- 연재 허브: 글의 `series`와 같은 파일명에 `type: series`, `status`, `started`, `ended`, `last_published`, `next_action`을 기록한다.
- 태그는 `blog`와 주제 태그 1~2개까지만 둔다. 플랫폼명·발행 상태·연재 여부는 태그 대신 속성이나 `related`로 관리한다.
