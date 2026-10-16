---
title: 기술 블로그
created: 2026-07-10
project_id: blog
status: active
started: 2026-06-10
ended: null
tags:
  - 프로젝트/blog
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
- 연재 상태는 연재명과 같은 허브 노트에서 관리한다. Base의 공백 경고는 점검 신호이며 `on-hold`·`completed` 전환은 직접 판단한다.

## 아웃라인 관리

- 글 하나당 `_outlines/<글 제목> - 아웃라인.md` 하나를 두고, 집필 계약도 그 안에 포함한다. 원고 전문은 기존처럼 `20_Projects/blog/`에 둔다.
- 아웃라인에는 독자·목적·범위, 절별 역할, 사용할 근거와 미결정 사항만 남긴다. 원고 복제본이나 리뷰 이력으로 만들지 않는다.
- 아웃라인에서 원고로 링크하고, 공개 원고 본문에는 관리 문서 링크를 넣지 않는다. 기본 속성은 `title`, `created`이며 원고용 `status`, `slug`, `published`는 두지 않는다. Base는 `status`로 발행 원고만 센다.
- 목적·범위·절 구성이 바뀔 때 갱신한다. 문장 수정마다 맞추지 않으며, 본문이 더 나아졌다면 아웃라인을 고친다. 발행 후에는 마지막 집필 기준으로 보존하고 완료된 리뷰 기록을 덧붙이지 않는다.
- 사이트 `config.json`의 `exclude`에 `20_Projects/blog/_outlines`를 명시한다. 파일명 앞의 `_`나 발행 속성 누락에만 의존하지 않는다. 이 제외는 사이트 게시를 막는 것이며 Git 공개 여부와는 별개다.

## 블로그 글 메타데이터

- 공통: `title`, `created`, `tags`, `status`, `author`, `summary`, `related`
- 이미 외부에 발행한 글: `publication`, `source`를 추가하고, 원문 발행일을 확인할 수 있을 때만 `published`를 기록한다.
- 연재 글: `series`, `series_order`를 추가하고 앞·뒤 글만 `related`로 연결한다.
- 연재 허브: 글의 `series`와 같은 파일명에 `type: series`, `status`, `started`, `ended`, `last_published`, `next_action`을 기록한다.
- 태그는 [속성 스키마의 태그 사용 기준](../../99_Templates/_property-schema.md#태그-사용-기준)을 따른다. 첫 태그는 글의 중심 주제로 두고, 나머지는 실제 검색·탐색에 필요한 맥락만 붙인다. 단순히 언급한 기술이나 중복 분류는 붙이지 않는다. 블로그 글임은 폴더가 나타내므로 `blog` 태그는 붙이지 않는다. 플랫폼명·발행 상태·연재 여부는 태그 대신 속성이나 `related`로 관리한다.
