---
tags:
  - devlog
  - java
  - troubleshooting
created: 2025-08-13
type:
  - java
  - spring boot
---

> [!danger]  문제  
> Spring boot 버전업 후 부트 시 다음 오류 발생
> 
`org.springframework.context.ApplicationContextException: Component scan for configuration class[~~~~] could not be used with conditions in REGISTER_BEAN phase`  

---

> [!caution] 원인
> Bean registration lifecycle의 강화된 조건 처리 시스템에서 발생하는 오류다.
 `@Conditional` 조건이 Bean 등록 단계(*REGISTER_BEAN*)에서 사용할 수 없는 설정이나 위치에 걸려 있을 때 발생한다.
### 📌 문제 발생 예시
#### `@ComponentScan` 대상 클래스에 `@Conditional`이 걸려 있을때

```java
@Configuration
@ComponentScan(basePackages = "com.example")
public class MyAppConfig {}	
```

```java
package com.example.sample;

@Component
@Conditional(OnSomethingCondition.class)  // ← 이게 문제	
public class SomeClass {}
```
	→ 이 경우 Spring은 ComponentScan으로 클래스를 찾고 빈으로 등록하려 하지만,
	REGISTER_BEAN 단계에서 조건 평가가 불가능해서 에러 발생
	
 --- 

> [!tip] 해결 방법
> #### 안전하게 조건부 *Bean* 등록
> 1. `@Bean`  메서드 수준에서 `@Conditional` 적용
>    
> 2. `@Conditional` 대신 `@ConditionalOnProperty`, `@Profile`, `@ConditionalOnClass` 같은 *Spring Boot* 전용 어노테이션 사용 (추천)

### 상세 설명
#### 1. `@Bean`  메서드 수준에서 `@Conditional` 적용

```java
@Configuration
public class ExampleConfig {

	@Bean
	@Conditional(OnSomethingCondition.class)
	public SomeClass someClass() {
		return new SomeClass();
	}
}
```

#### 2. `@Conditional` 대신 `@ConditionalOnProperty`, `@Profile`, `@ConditionalOnClass` 같은 *Spring Boot* 전용 어노테이션 사용 (추천)

```java
package com.example.sample;

@Component
@ConditionalOnProperty(name= "something.enabled", havingValue = "true")
public class SomeClass {}
```

>[!note] 보충 설명
> #### *REGISTER_BEAN* Phase란?
> Spring의 Bean 등록 단계,
> ==bean definition → bean registration → bean instantiation → bean wiring==
> 중 두 번째 단계.
> 
> `@ComponentScan`은 *REGISTER_BEAN* phase에서 `@Conditional` 이 걸린 클래스를 처리할 수 없음. 
> 안전하게 적용하려면 *Spring Boot* 전용 조건부 어노테이션 사용


---

> [!info] 참고 자료
> - 블로그/문서/책 등 참고 링크
