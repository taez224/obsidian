---
title: "W05: 프로젝트 킥오프"
created: 2026-02-02
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W05
status: active
---

# W05 (01-29 ~ 02-02) — 프로젝트 킥오프

## 이번 주 요약

QRA 프로젝트의 시작. PoC로 로컬 GitOps 환경을 구축하고, Gallery에서 분리할 기능의 범위를 정의한 주.

## 주요 작업

### PoC 환경 구축 (01-29 ~ 01-30)
- Docker Compose 기반 로컬 개발 환경 (Gitea + ArgoCD + K8s/k3d)
- GitOps → ArgoCD → K8s 배포 파이프라인 검증
- Helm/Kustomize 양쪽 테스트

### 아키텍처 설계 (01-30 ~ 02-02)
- Gallery에서 배포 모니터링 기능 분리 설계
- ADR-003: Fabric8 6.13.5 선정 (Spring Boot 3.2/Jackson 호환)
- AGENTS.md 체계 구축, 도메인 모델 문서화
- EPIC 1-9 범위 정의, PRD 작업

### 초기 셋업 (02-02)
- qra-backend Git default branch 설정 (master → main)
- Gradle Wrapper 설정
- docs/ 구조 통일, 문서 체계 정비

## 데일리 로그

- [[2026-01-29]] — PoC 로컬 환경 구성
- [[2026-01-30]] — 통합 테스트, Gallery 분석, 도메인 모델링
- [[2026-02-02]] — 문서 체계 정비, ADR, AGENTS.md

## 회고

> [!check] 잘한 점
> - PoC 우선 접근으로 기술 리스크를 초반에 해소
> - AGENTS.md + CLAUDE.md 심볼릭 링크 패턴으로 멀티 AI 도구 호환성 확보

> [!warning] 개선할 점
> - 프로젝트 초기 문서 체계에 시간을 많이 투자 — 하지만 이후 주에서 효과를 봄

## 다음 주 방향

→ Gallery 마이그레이션 본격 착수, DeploymentFlow 구현
