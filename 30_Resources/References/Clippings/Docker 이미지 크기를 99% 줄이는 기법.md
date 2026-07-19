---
title: "Docker pros are shrinking images by 99%: The hidden techniques you can’t afford to miss"
source: "https://aws.plainenglish.io/docker-pros-are-shrinking-images-by-99-the-hidden-techniques-you-cant-afford-to-miss-a70ee26b4cbf"
author:
  - "[[Dipanshu ‎]]"
published: 2024-09-18
created: 2025-02-17
description: Docker 이미지 크기를 크게 줄여 더 빠르고 가벼운 컨테이너를 만드는 최적화 기법을 소개한다.
tags:
  - "clippings"
status: unread
my_take: ""
---

## 내용 요약

- 비대한 이미지가 빌드·배포 시간, 저장 공간과 네트워크 비용에 미치는 영향을 설명하고 1.2GB 이미지를 줄이는 사례를 제시한다.
- 멀티 스테이지 빌드로 빌드 도구와 런타임 산출물을 분리하고, 실행 파일만 최종 이미지로 옮기는 과정을 보여준다.
- 레이어 병합, `scratch`·distroless 기반 이미지, BuildKit, `.dockerignore`, 이미지 분석 도구를 이용한 최적화를 다룬다.
- 공식 베이스 이미지, 비루트 사용자, 취약점 검사, 비밀정보 분리와 모니터링 등 경량화 과정의 보안 수칙을 함께 정리한다.
