---
summary: 옮겨 간 모듈에 -parameters 컴파일 플래그가 없어 Spring 6.1이 생성자 파라미터 이름으로 빈 후보를 좁히지 못한 것이며, 코드와 함께 빌드 옵션을 옮기면 풀린다.
created: 2026-07-15
slug: spring6-duplicate-bean-parameters
tags:
  - 개발/Spring
---

# 모듈을 옮긴 뒤 빈 후보가 여러 개라 실패하는 Spring 6 기동

멀티모듈 프로젝트에서 코드를 다른 모듈로 옮긴 뒤 Spring Boot가 기동에 실패했다. 생성자의 특정 파라미터에서 같은 타입인 `Executor` 빈 여러 개가 매칭된다는 모호성 오류였다.

같은 타입의 빈이 여러 개이고 `@Qualifier`나 `@Primary` 같은 선택 기준이 없으면, Spring은 [주입 지점의 이름과 빈 이름을 맞춰](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html) 후보를 고를 수 있다. 그런데 Spring 6.1부터 생성자 파라미터 이름을 이 방식으로 쓰려면 컴파일할 때 `-parameters` 플래그가 필요하다.

옮겨 간 모듈의 빌드 설정에는 이 플래그가 없었다. 파라미터 이름이 소실되어 Spring이 이름으로 후보를 좁히지 못하고 `expected single matching bean but found N`을 냈다. 코드만 옮기고 빌드 옵션을 옮기지 않은 것이 근본 원인이다.

플래그를 모든 컴파일 작업에 붙여서 해결했다.

```gradle
tasks.withType(JavaCompile).configureEach {
    options.compilerArgs.add('-parameters')
}
```

다만 플래그를 붙이기 전에, 이름에 기대는 선택이 정말 의도한 계약인지도 함께 봐야 한다. 특정 빈을 반드시 써야 한다면 `@Qualifier`로 명시하고, 여러 후보 중 기본값이 있다면 `@Primary`를 검토한다.

여기서 얻은 것은 멀티모듈 이관 체크리스트에 넣을 항목 하나다. 코드를 옮길 때는 컴파일 플래그와 어노테이션 프로세서 같은 빌드 옵션도 함께 옮긴다.

## 확인 범위

이름 기반 후보 선택과 `-parameters` 요구 사항은 위 공식 문서로 확인했다. 실제 사례에서는 옮긴 모듈의 컴파일 작업에 플래그를 붙인 뒤 기동을 확인했다.

## 연관된 노트

- [[ComponentScan 설정과 REGISTER_BEAN 조건의 충돌|REGISTER_BEAN 조건과 ComponentScan 충돌]] - 후보 빈의 선택이 모호한 오류와, 설정을 파싱하며 빈 등록 조건이 충돌하는 오류를 구분한다.
