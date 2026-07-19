---
title: "Mastering Kafka: Advanced Concepts Every Senior Software Engineer Should Know"
source: "https://manjulapiyumal.medium.com/mastering-kafka-advanced-concepts-every-senior-software-engineer-should-know-9283664c99e1"
author:
  - "[[Manjula Piyumal]]"
published: 2024-08-25
created: 2024-12-21
description: 실시간 데이터 파이프라인과 스트리밍 애플리케이션을 위한 Apache Kafka의 고급 개념을 시니어 엔지니어 관점에서 설명한다.
tags:
  - "clippings"
status: unread
my_take: ""
---

## 내용 요약

- Kafka 토픽의 파티션이 병렬 처리와 순서를 결정하는 방식, 파티션 수를 동적으로 늘릴 때 생기는 키 분배와 운영상의 제약을 설명한다.
- 리더·팔로워 복제와 ISR을 통한 데이터 중복성, at-most-once·at-least-once·exactly-once 전달 보장의 차이를 다룬다.
- 소비자 오프셋 커밋과 재처리 일관성, 컨트롤러와 ZooKeeper가 브로커·파티션 리더를 관리하는 역할을 정리한다.
- Avro·Protobuf·JSON Schema의 호환성 정책과 실행 중 메시지가 오가는 상황을 포함해 스키마 진화 전략을 설명한다.
- 로그 압축·보존 정책과 Kafka Streams를 이용한 실시간 처리처럼 저장 공간과 스트림 애플리케이션 운영에 필요한 기능을 다룬다.
- TLS·SASL·ACL과 감사·보존 정책, JMX·Prometheus·Grafana를 활용한 브로커 상태·소비자 지연·미복제 파티션 관측을 제시한다.
