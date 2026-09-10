---
created: 2025-08-13
slug: register-bean-phase-error
summary: 컴포넌트 스캔을 수행하는 설정에 REGISTER_BEAN 단계에서 평가되는 조건이 결합되면 기동에 실패하며, 어노테이션 이름이 아니라 조건 구현의 평가 단계를 확인해야 풀린다.
aliases:
  - could not be used with conditions in REGISTER_BEAN phase
tags:
  - 개발/Spring
---

# ComponentScan 설정과 REGISTER_BEAN 조건의 충돌

Spring Boot 버전을 올린 뒤 기동 과정에서 `ApplicationContextException`이 발생했고 다음 메시지가 붙었다.

```text
Component scan for configuration class [...] could not be used with conditions in REGISTER_BEAN phase
```

버전을 올리기 전에는 같은 설정으로 기동했다. 조건 어노테이션을 바꾼 적도 없어서 처음에는 어노테이션 종류를 의심했다.

## 스캔 설정과 조건 단계의 충돌

Spring 6.2의 [`ConfigurationClassParser`](https://github.com/spring-projects/spring-framework/blob/v6.2.0/spring-context/src/main/java/org/springframework/context/annotation/ConfigurationClassParser.java)는 `@ComponentScan`을 처리하기 전에 해당 설정과 일부 외부 감싸는 설정의 조건을 모은다. 그중 [`ConfigurationCondition`](https://docs.spring.io/spring-framework/docs/6.2.0/javadoc-api/org/springframework/context/annotation/ConfigurationCondition.html)의 단계가 `REGISTER_BEAN`인 조건이 있으면 이 오류를 발생시킨다. `PARSE_CONFIGURATION`은 설정을 해석하는 단계이고, `REGISTER_BEAN`은 그 설정에서 빈 정의를 등록할지 판단하는 단계다. 스캔은 해석 단계에서 일어나는데 조건은 등록 단계의 정보를 요구하니 순서가 맞지 않는다.

일반 `@Component`에 `@Conditional`이 붙어 있다는 사실만으로 오류가 나는 것은 아니다. 스캔을 수행하는 설정과 조건의 평가 단계가 함께 맞물릴 때 난다. 그래서 `@Conditional`을 Spring Boot 어노테이션으로 바꾸기만 하면 해결된다고 볼 수도 없다. 어노테이션 이름이 아니라 실제 조건 구현이 어느 단계에서 평가되는지를 봐야 한다.

## 확인과 수정

1. 오류에 나온 configuration class와 조건 목록을 찾는다. 직접 선언뿐 아니라 합성 어노테이션이나 감싸는 설정도 확인한다.
2. 조건이 `ConfigurationCondition`이라면 `getConfigurationPhase()`가 반환하는 단계를 확인한다.
3. 빈 존재 여부에 따라 일부 빈만 등록하려는 목적이라면, 컴포넌트 스캔과 개별 빈의 조건부 등록을 분리한다. 자동설정에서 `@Bean` 메서드에 조건을 두는 방식이 한 가지 선택이다.
4. 조건이 환경 속성이나 클래스 존재 여부만 필요로 하는지 검토한다. 이를 이유로 실제로 필요한 빈 의존 조건을 무조건 다른 조건으로 바꾸지는 않는다.

## 확인 범위

파서가 조건을 모으는 시점과 단계 판정은 Spring Framework 6.2.0 소스와 javadoc으로 확인했다. 실제 프로젝트에서 어느 조건이 걸렸고 어떤 수정으로 기동했는지는 당시 기록에 남아 있지 않아 이 노트에 적지 않았다.

## 연관된 노트

- [[모듈을 옮긴 뒤 빈 후보가 여러 개라 실패하는 Spring 6 기동]] - 설정·빈 정의를 처리하는 단계의 오류와, 이미 등록된 후보 중 주입 대상을 선택하는 오류를 구분한다.
