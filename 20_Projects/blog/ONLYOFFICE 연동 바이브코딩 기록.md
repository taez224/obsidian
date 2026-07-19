---
title: ONLYOFFICE 연동 바이브코딩 기록
created: 2026-07-15
type: series
status: active
started: 2025-11-24
ended: null
last_published: 2026-01-22
next_action: 5편 진행 여부 결정
tags:
  - 프로젝트/blog
  - 프로젝트/onlyoffice-demo
---

# ONLYOFFICE 연동 바이브코딩 기록

## 연재 목적

ONLYOFFICE Docs를 실제 서비스에 연결하면서 드러난 문서 편집기 이상의 통합 책임과, AI 코딩 도구를 활용해 구현을 확장한 과정을 기록한다.

## 현재 상태

Velog에 4편을 발행했고 후속 구현 글감이 남아 있는 진행형 연재다.

## 연재 흐름

1. [[ONLYOFFICE 01 - 그냥 문서 편집기인 줄 알았는데]] - ONLYOFFICE 통합이 에디터 연결만의 문제가 아닌 이유를 소개한다.
2. [[ONLYOFFICE 02 - Antigravity와 함께한 Vibe Coding기]] - 로컬 파일 기반의 기본 연동과 AI 코딩 과정을 다룬다.
3. [[ONLYOFFICE 03 - key와 메타데이터 관리]] - Document key, 저장 상태, 메타데이터와 DB 연동을 정리한다.
4. [[ONLYOFFICE 04 - SDK, MinIO, Saga]] - SDK, 오브젝트 스토리지, 저장 정합성으로 확장한다.

## 후속 후보

- 프론트엔드 고도화: React·Next.js 기반 편집 경험
- 백엔드 고도화: Spring Boot·Hibernate 기반 통합 구조
- 데모 프로젝트가 이력서나 포트폴리오에서 보여줄 수 있는 문제 해결 범위

## 편집 기준

- 제품 소개보다 실제 통합 과정에서 마주친 책임과 선택을 중심에 둔다.
- AI 도구 사용 자체보다 AI가 구현 과정과 판단 방식에 어떤 변화를 만들었는지 설명한다.
- 공개할 수 없는 업무 코드는 의사 코드, 다이어그램, 재현 가능한 데모로 대체한다.

## 운영 메모

- 실제 발행 상태와 순서는 각 글의 frontmatter를 정본으로 삼는다.
- 후속 후보의 순서는 구현과 검증이 끝난 뒤 확정한다.

## 연관된 노트

- [[blog]] - 전체 블로그 프로젝트의 운영 허브
- [[onlyoffice-demo]] - 연재의 구현 근거가 되는 프로젝트 허브
