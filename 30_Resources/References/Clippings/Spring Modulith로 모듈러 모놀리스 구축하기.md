---
title: "Spring Modulith: Building Modular Monoliths for a Structured Tomorrow 🌱"
source: "https://halilural5.medium.com/spring-modulith-building-modular-monoliths-for-a-structured-tomorrow-f52da666c233"
author:
  - "[[Halil Ural]]"
published: 2024-09-14
created: 2025-01-26
description: Spring Modulith를 사용해 모놀리스의 단순함을 유지하면서 모듈 경계를 갖춘 애플리케이션을 만드는 방법을 소개한다.
tags:
  - "clippings"
status: unread
my_take: ""
---

## 내용 요약

- 모듈러 모놀리스를 하나의 배포 단위를 유지하면서 책임과 의존성이 분리된 모듈로 애플리케이션을 구성하는 방식으로 설명한다.
- Spring Modulith는 모듈 경계, 이벤트 기반 통신, 의존성 관리와 격리 테스트를 Spring Boot 애플리케이션에 적용한다.
- 사용자와 주문 모듈을 패키지로 나누고 `ApplicationModuleListener`로 모듈 간 이벤트를 처리하는 예제를 보여준다.
- JPA로 모듈 데이터를 저장하고 모듈 의존성 규칙과 단위·통합 테스트로 경계가 유지되는지 검증한다.
- 분산 시스템의 운영 복잡성을 피하면서 필요할 때 일부 모듈을 마이크로서비스로 분리할 수 있다는 확장 경로를 제시한다.
