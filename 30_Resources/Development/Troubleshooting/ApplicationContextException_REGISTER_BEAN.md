---
title: ApplicationContextException - REGISTER_BEAN phase
created: 2025-08-13
summary: ComponentScan을 수행하는 설정과 REGISTER_BEAN 단계의 조건이 충돌할 때 조건의 위치와 평가 시점을 확인한다.
tags:
  - 개발/Spring
---

# ApplicationContextException - REGISTER_BEAN phase

> [!bug] 문제
> Spring Boot 버전업 후 기동 과정에서 다음 오류가 발생했다.
>
> `Component scan for configuration class [...] could not be used with conditions in REGISTER_BEAN phase`

## 원인

컴포넌트 스캔을 수행할 설정에 빈 등록 단계에서 평가하는 조건이 결합된 경우를 확인해야 한다. Spring 6.2의 `ConfigurationClassParser`는 `@ComponentScan`을 처리하기 전에 해당 설정과 일부 외부 감싸는 설정의 조건을 모은다. 그중 `ConfigurationCondition`의 단계가 `REGISTER_BEAN`인 조건이 있으면 이 오류를 발생시킨다.

일반 `@Component`에 `@Conditional`이 붙어 있다는 사실만으로 오류가 나는 것은 아니다. 중요한 것은 **스캔을 수행하는 설정과 조건의 평가 단계가 함께 맞물리는지**다. `@Conditional`을 Spring Boot 어노테이션으로 바꾸기만 하면 해결된다고 볼 수도 없다. 어노테이션 이름보다 실제 조건 구현의 평가 시점을 확인한다.

## 확인과 수정

1. 오류에 나온 configuration class와 조건 목록을 찾는다. 직접 선언뿐 아니라 합성 어노테이션이나 감싸는 설정도 확인한다.
2. 조건이 `ConfigurationCondition`이라면 `getConfigurationPhase()`가 반환하는 단계를 확인한다.
3. 빈 존재 여부에 따라 일부 빈만 등록하려는 목적이라면, 컴포넌트 스캔과 개별 빈의 조건부 등록을 분리한다. 자동설정에서 `@Bean` 메서드에 조건을 두는 방식이 한 가지 선택이다.
4. 조건이 환경 속성이나 클래스 존재 여부만 필요로 하는지 검토한다. 이를 이유로 실제로 필요한 빈 의존 조건을 무조건 다른 조건으로 바꾸지는 않는다.

`PARSE_CONFIGURATION`은 설정을 해석하는 단계이고, `REGISTER_BEAN`은 그 설정에서 빈 정의를 등록할지 판단하는 단계다. 조건이 필요로 하는 정보와 작업 순서가 맞는지가 이 문제의 핵심이다.

## 참고 자료

- [Spring 6.2 ConfigurationClassParser](https://github.com/spring-projects/spring-framework/blob/v6.2.0/spring-context/src/main/java/org/springframework/context/annotation/ConfigurationClassParser.java) - `@ComponentScan` 처리와 `collectRegisterBeanConditions`
- [Spring ConfigurationCondition](https://docs.spring.io/spring-framework/docs/6.2.0/javadoc-api/org/springframework/context/annotation/ConfigurationCondition.html) - 조건 평가 단계

## 연관된 노트

- [[Spring 6 동일 타입 다중 빈 기동 실패 - parameters 플래그]] - 설정·빈 정의를 처리하는 단계의 오류와, 이미 등록된 후보 중 주입 대상을 선택하는 오류를 구분한다.
