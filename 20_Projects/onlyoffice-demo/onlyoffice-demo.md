---
title: ONLYOFFICE 연동
created: 2026-01-15
tags:
  - 프로젝트/onlyoffice-demo
  - 개발/인프라
project_id: onlyoffice-demo
status: on-hold
started: 2026-01-15
ended: null
aliases:
  - onlyoffice
---

# ONLYOFFICE 연동

> [!note] 현재 상태
> 지금은 보류 중인 프로젝트다. 재개할 때는 이 노트의 아키텍처와 아래 발행 시리즈부터 확인한다.

## 발행 시리즈

- [[ONLYOFFICE 01 - 그냥 문서 편집기인 줄 알았는데|1편: ONLYOFFICE 개요와 통합 구조]]
- [[ONLYOFFICE 02 - Antigravity와 함께한 Vibe Coding기|2편: 기본 연동 구현]]
- [[ONLYOFFICE 03 - key와 메타데이터 관리|3편: key와 메타데이터 관리]]
- [[ONLYOFFICE 04 - SDK, MinIO, Saga|4편: SDK, MinIO, Saga]]

## 아키텍처 개요

### 전체 아키텍처 흐름 (편집 요청 → 편집 → 저장 콜백)

```mermaid
flowchart LR
    classDef server fill:#1f77b4,stroke:#0b3d62,stroke-width:1px,color:white;
    classDef storage fill:#2ca02c,stroke:#145214,stroke-width:1px,color:white;
    classDef client fill:#ff7f0e,stroke:#b35500,stroke-width:1px,color:white;
    classDef onlyoffice fill:#9467bd,stroke:#56357c,stroke-width:1px,color:white;

subgraph C1[Client]
A1[웹/모바일 클라이언트<br/>React · Vue]
end
class A1 client;

subgraph S1[통합 App/Callback Server]
B1[문서 권한 체크]
B2[Config JSON 생성<br/>fileUrl / key / jwt]
B3[callback 처리<br/>status=2,6,7]
B4[최종 파일 저장]
end
class B1,B2,B3,B4 server;

subgraph OO1[ONLYOFFICE Docs Server]
C2[렌더링 & 공동편집]
C3[diff merge]
C4[autosave / force-save]
end
class C2,C3,C4 onlyoffice;

subgraph ST1[Object Storage<br/>S3 / MinIO]
E1[원본 파일]
E2[최종 파일]
end
class E1,E2 storage;

A1 -->|1. 편집 요청| B1
B1 --> B2
B2 -->|2. config JSON| A1

A1 -->|3. 파일 로드| E1
E1 --> A1

A1 -->|4. 편집 이벤트| C2

C2 --> C3 --> C4
C4 -->|5. 저장 요청| B3
B3 -->|6. 파일 다운로드| B4
B4 -->|7. 저장| E2


```

---

### 콜백 서버 상세 시퀀스 (status별 처리 흐름)

```mermaid
sequenceDiagram
    autonumber
    participant DS as Docs Server
    participant CB as Callback Server
    participant ST as Storage (S3/MinIO)

    DS->>CB: POST /callback (status=1) <br/>편집 중 이벤트
    Note right of CB: 무시 (임시 저장)

    DS->>CB: POST /callback (status=2) <br/>정상 저장 완료
    CB->>DS: GET file<br/>최종 파일 다운로드
    CB->>ST: PUT file<br/>최종 파일 저장

    DS->>CB: POST /callback (status=6)<br/>force-save
    CB->>DS: GET file
    CB->>ST: PUT file (force-save 버전)

    DS->>CB: POST /callback (status=7)<br/>빈 파일 최초 생성
    CB->>ST: PUT file (initial)
```

---

### JWT & Security 구조

```mermaid
flowchart TD
    classDef jwt fill:#444,stroke:#222,color:white;

    A[Application Server<br/>Config 생성] --> B[JWT 생성<br/>document token]
    class B jwt;

    B --> C[Editor iframe<br/>JS Config]
    C --> D[Docs Server<br/>JWT 검증]
    D --> E[Callback Server<br/>JWT 재검증]

    E --> F[최종 파일 저장]
```
