---
title: Vizend QRA
created: 2026-01-29
tags:
  - project
  - 프로젝트/vizend-qra
status: active
---

# Vizend QRA

> GitOps 기반 배포 오케스트레이션 & 런타임 모니터링 플랫폼

## 목표

Gallery(기존 배포 시스템)의 배포 모니터링 기능을 독립 서비스로 분리하여:
- GitOps 상태 → ArgoCD → K8s Pod 전체 배포 파이프라인을 관측
- 런타임 이상 신호 감지 및 알림
- 구독(Subscription) 기반 멀티테넌트 배포 관리

## 기술 스택

| 영역 | 기술 |
|------|------|
| 언어 | Java 17, Spring Boot 3.2 |
| 빌드 | Gradle (멀티모듈) |
| DB | PostgreSQL + Flyway |
| 메시징 | Kafka (Vello) |
| K8s | Fabric8 6.13.5, SharedInformer |
| CI/CD | GitLab CI, ArgoCD |
| Registry | Harbor, ECR, NCR |
| 모니터링 | SSE 실시간 스트리밍 |

## 모듈 구조

```
qra-boot      ← 부트 모듈 (설정, 실행)
qra-domain    ← 도메인 모델 (Entity, VO, Enum)
qra-feature   ← 비즈니스 로직 (Flow, Action, Seek)
qra-facade    ← REST API (Resource, Facade, Fetch)
qra-proxy     ← 외부 연동 (K8s, ArgoCD, Harbor, Git)
qra-event     ← Kafka 이벤트 정의
qra-store-jpa ← JPA 영속 계층
```

## EPIC 현황

| EPIC | 이름 | 상태 |
|------|------|------|
| EPIC-2 | Gallery Subscription Integration | ✅ 완료 |
| EPIC-3 | GitOps Manifest Mutation | ✅ 완료 |
| EPIC-5 | Deployment Completion Event | ✅ 완료 |
| EPIC-6 | Runtime Health Monitoring | ✅ 완료 |
| EPIC-7 | Notification Integration | ✅ 완료 |
| EPIC-9 | K8S Cluster Monitoring | ✅ 완료 |
| EPIC-14 | Infrastructure Configuration Mgmt | ✅ 완료 |

## 주간 회고

| 주차 | 기간 | 핵심 테마 |
|------|------|-----------|
| [[2026-W05 vizend-qra\|W05]] | 01-29 ~ 02-02 | 프로젝트 킥오프, PoC, 아키텍처 설계 |
| [[2026-W06 vizend-qra\|W06]] | 02-03 ~ 02-09 | Gallery 마이그레이션, ArgoCD observation 도입 |
| [[2026-W07 vizend-qra\|W07]] | 02-10 ~ 02-16 | API 확장, 동시성 보호, 코드 품질 |
| [[2026-W08 vizend-qra\|W08]] | 02-17 ~ 02-23 | 런타임 모니터링 리팩토링, 장애 감지 시스템 |
| [[2026-W09 vizend-qra\|W09]] | 02-24 ~ 03-02 | 배포 생명주기, JaCoCo, 요구사항 체계 |
| [[2026-W10 vizend-qra\|W10]] | 03-03 ~ 03-09 | 배포 파이프라인 완성, 멱등성, undeploy |
| [[2026-W11 vizend-qra\|W11]] | 03-10 ~ 03-16 | 레거시 정리, Registry 연동, 모니터링 재설계 |
| [[2026-W12 vizend-qra\|W12]] | 03-17 ~ 03-22 | K8s 인프라 최적화, Event enrichment |

## 핵심 아키텍처 결정

| ADR | 주제 | 날짜 |
|-----|------|------|
| ADR-003 | K8S Observation Strategy (Fabric8) | 02-02 |
| ADR-009 | GitLab 이슈 동기화 | 02-27 |
| ADR-011 | ArgoCD project 검증 정책 | 03-04 |
| ADR-012 | PackageType workloadType 필터링 | 03-03 |
| ADR-014 | deploymentGroupKey 재배포 모델 | 03-06 |
| ADR-015 | Leader-only RuntimeWatch 원칙 | 03-19 |
| ADR-016 | ArgoCd 멱등 수렴 모델 | 03-19 |

## 관련 링크

- 코드베이스: `/Users/taez/Projects/nextree/vizend/qra-backend`
- DevLog: [[2026-02-04|DevLog 시작]] ~ [[2026-03-20|최근]]
