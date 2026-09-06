---
summary: 이름 기반 빈 선택에 필요한 파라미터 메타데이터와 모듈별 컴파일 옵션을 확인한다.
created: 2026-07-15
tags:
  - 개발/Spring
---

> [!bug] 문제
> 멀티모듈 프로젝트에서 코드를 다른 모듈로 이관한 뒤 Spring 부트 기동 실패. 생성자의 특정 파라미터에서 같은 타입(`Executor`)의 빈 여러 개가 매칭된다는 모호성 오류.

---

> [!question] 원인
> 동일 타입 빈이 여러 개이고 `@Qualifier`나 `@Primary` 같은 선택 기준이 없을 때, Spring은 **주입 지점의 이름과 빈 이름**을 맞춰 후보를 선택할 수 있다. Spring 6.1부터 생성자 파라미터 이름을 이 방식으로 사용하려면 컴파일 시 `-parameters` 플래그가 필요하다. 이관한 모듈의 빌드 설정에 플래그가 없으면 파라미터명이 소실되어 "expected single matching bean but found N"으로 터진다. **코드만 옮기고 빌드 옵션을 안 옮긴 것**이 근본 원인.

---

> [!tip] 해결 방법
> ```gradle
> tasks.withType(JavaCompile).configureEach {
>     options.compilerArgs.add('-parameters')
> }
> ```
> 이름에 기대는 선택이 의도한 계약인지도 확인한다. 특정 빈을 명시해야 하면 `@Qualifier`, 기본 후보가 있으면 `@Primary`를 검토한다.
>
> 멀티모듈 이관 체크리스트에 "빌드 옵션(컴파일 플래그·어노테이션 프로세서)도 함께 이관"을 포함할 것.

---

> [!info] 참고 자료
> - 출처: 비공개 개발 기록 2026-04-28
> - [Spring: Qualifiers와 이름 기반 후보 선택](https://docs.spring.io/spring-framework/reference/core/beans/annotation-config/autowired-qualifiers.html)

## 연관된 노트

- [[ApplicationContextException_REGISTER_BEAN|REGISTER_BEAN 조건과 ComponentScan 충돌]] - 후보 빈의 선택이 모호한 오류와, 설정을 파싱하며 빈 등록 조건이 충돌하는 오류를 구분한다.
