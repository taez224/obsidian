---
title: 내가 만든 @Annotation으로 인가 로직 관리하기
created: 2023-04-13
published: 2023-04-13
tags:
  - blog
  - 개발/Java
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/%EB%82%B4%EA%B0%80-%EB%A7%8C%EB%93%A0-Annotation%EC%9C%BC%EB%A1%9C-%EC%9D%B8%EA%B0%80-%EB%A1%9C%EC%A7%81-%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0
summary: "@Constraint와 ConstraintValidator로 역할 티어 기반 사용자 조회·수정 권한을 DTO 검증으로 분리한 구현 기록."
---

# 내가 만든 @Annotation으로 인가 로직 관리하기

## 요구사항

> 우리 회사는 다단계 회사이다.  
> 단계 별로 role tier가 있고 각 tier 별 관리자가 있다.  
> 관리자는 자기가 속한 role tier 이하의 사용자 정보만 조회 및 수정할 수 있다.  
> (2 tier 관리자일 경우 3 tier 사용자를 2 tier로 승격 가능. 1 tier로 승격 및 1 tier 사용자를 수정하는 것은 불가)

이러한 상황에서 role tier check logic을 분리하여 처리하는 방식에는 여러가지가 있겠지만 이번에는 `@Valid`, `@Constraint` 와 `ConstraintValidator` 로 구현해보자.

## 현재 상황

### 도메인

```java
public class User {

    private String userId;
    private Role userRole;
    private boolean admin;
    
    /* 생략 */
}
```
```java
public class UserDto {

    private String userId;
    private Role userRole;
    private boolean admin;
    
    /* 생략 */
}
```
```java
@Getter
@AllArgsConstructor
public enum Role {
    MASTER("master", 0),
    DIAMOND("diamond", 1),
    GOLD("gold", 2),
    SILVER("silver", 3),
    BRONZE("bronze", 4),
    ;
    
    private String name;
    private int tier;
    
    /* 생략 */
}
```

### 컨트롤러

```java
@RestController
@RequestMapping("/users")
public class UserController {
    
    /* 생략 */
    
    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUserById(@PathVariable String userId){
        UserDto userDto = this.userService.getUserByUserId(userId);
        return ResponseEntity.ok(userDto);
    }
        
    @PostMapping("/update")
    public ResponseEntity<UserDto> updateUser(@RequestBody UpdateUserRequest request) {
        UserDto updatedUserDto = this.userService.updateUser(request.getUserDto());
        return ResponseEntity.ok(updatedUserDto);
    } 
   
}
```
```java
@Getter
@Setter
public class UpdateUserRequest {
    private UserDto userDto;
    /* 생략 */
}
```

## 요구사항 적용

### 구상

- 조회 API  
	\- @PathVariable로 들어오는 userId가 조회 가능한 user인지 확인한다.
	1. 요청자의 Role tier 및 관리자 여부를 확인한다. (Spring Security Context에 User 정보가 들어가 있다고 가정)
		2. userId로 찾은 User가 요청자의 Role tier 이하인지 확인한다.  
		`@AccessibleUser` 라는 Custom Annotation을 붙여서 검증하고 싶다.
- 수정 API  
	\- @RequestBody로 들어오는 userDto의 userId와 userRole을 검증한다.
	1. userId는 위에서 만든 `@AccessibleUser` 로 검증하고 싶다.
		2. userRole은 `@ModifiableRole` annotation을 만들어 검증한다.

## 조회

### @AccessibleUser 만들기

```java
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
public @interface AccessibleUser {
    String message() default "Access denied for this user.";
}
```
- @Target({ElementType.FIELD, ElementType.PARAMETER}): 해당 어노테이션이 파라미터와 필드에 사용될 수 있도록 함
- @Retention(RetentionPolicy.RUNTIME): 런타임 시 어노테이션 정보 유지

### AccessibleUserValidator 만들기

```java
@RequiredArgsConstructor
public class AccessibleUserValidator implements ConstraintValidator<AccessibleUser, String> {

    private final UserService userService;

    @Override
    public boolean isValid(String userId, ConstraintValidatorContext context) {
        // SecurityContext에서 요청자 정보 가져오기
        User currentUser = getCurrentUser();
        if (currentUser == null || !currentUser.isAdmin()) {
            return false;
        }
        // 조회 혹은 수정 할 user의 role tier가 요청자의 tier 이하 면 OK!
        User userToCheck = userService.getUserById(userId);
        return currentUser.getUserRole().getTier() <= userToCheck.getUserRole().getTier();
    }

    // 대충 Spring Security로 사용자 정보 가져오는 로직
    private User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            return null;
        }
        return ((CustomUserDetails) authentication.getPrincipal()).getUser();
    }
}
```
- implements ConstraintValidator<AccessibleUser, String>  
	`ConstraintValidator` 를 구현한 class로 첫 번째 generic으로 Annotation이 들어가고 두 번째 generic에는 검증 할 파라미터(필드)의 타입이 들어간다.
- public boolean isValid(String userId,...)  
	첫 번째 파라미터로 우리가 검증 할 무언가가 들어온다. valid면 `true` 아니면 `false` 를 return 하면 되겠다.

### @AccessibleUser 수정

```java
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = AccessibleUserValidator.class)
public @interface AccessibleUser {
    String message() default "Access denied for this user.";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```
- @Constraint(validatedBy = AccessibleUserValidator.class):  
	`validatedBy` 에 조금전에 만든 Validator class를 넣어주었다. 해당 class의 `isValid` 로 검증을 하겠다는 뜻

### UserController 수정

```java
@Validated
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{userId}")
    public ResponseEntity<UserDto> getUserById(@PathVariable @AccessibleUser String userId){
        UserDto userDto = this.userService.getUserByUserId(userId);
        return ResponseEntity.ok(userDto);
    }
    /* 생략 */
 }
```
- @Validated: Spring에서 제공하는 어노테이션으로 해당 클래스에 validation이 가능하도록 설정해준다.
- userId 앞에 `@AccessibleUser` 어노테이션을 붙여 `@Constraint` 에 지정된 `AccessibleUserValidator` 로 검증하게 한다.

### 결과

![](https://velog.velcdn.com/images/taez224/post/b0b897d9-e095-49be-a1a7-84f29e85affd/image.png)  
만약 validation이 실패하면 위와 같이 `ConstraintViolationException` 이 떨어진다.  
이 exception을 핸들링하여 활용 가능하겠지만 일단 지금은 생략하자.

## 수정

> - @RequestBody로 들어오는 userDto의 userId와 userRole을 검증한다.
> 	1. userId는 위에서 만든 @AccessibleUser로 검증하고 싶다.
> 		2. userRole은 @ModifiableRole annotation을 만들어 검증한다.

### @ModifiableRole 만들기

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface ModifiableRole {
    String message() default "Cannot change to the specified role.";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

마찬가지로 만들어주고 @Constraint안에 넣어 줄 validator까지 만들어보자.

### RoleValidator 만들기

```java
@RequiredArgsConstructor
public class RoleValidator implements ConstraintValidator<ModifiableRole, Role> {

    private final AuthFacade authFacade;

    @Override
    public boolean isValid(Role targetRole, ConstraintValidatorContext context) {
        // SecurityContext에서 요청자 정보 가져오기
        User currentUser = authFacade.getCurrentUser();
        if (currentUser == null || !currentUser.isAdmin()) {
            return false;
        }
        
        // 수정할 권한이 요청자의 권한 이하일때만 valid
        return currentUser.getUserRole().getTier() <= targetRole.getTier();
    }

}
```
- ConstraintValidator<ModifiableRole, Role>: `@ModifiableRole` 로 `Role` 타입을 검증하겠다는 의미이다.

### @ModifiableRole 수정

```java
@Constraint(validatedBy = RoleValidator.class)
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ModifiableRole {
    String message() default "Cannot change to the specified role.";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

@Constraint에 RoleValidator class를 지정해주자.

### UserDto 수정

```java
public class UserDto {

    @AccessibleUser
    private String userId;
    @ModifiableRole
    private Role userRole;
    private boolean admin;
    
    /* 생략 */
}
```

UserDto에 담겨있는 userId와 userRole에 제약 조건을 담은 어노테이션을 붙여주고

### UserController 수정

```java
@Validated
@RestController
@RequestMapping("/users")
public class UserController {

   /* 생략 */
   
   @PostMapping("/update")
    public ResponseEntity<UserDto> updateUser(@RequestBody @Valid UpdateUserRequest request) {
        UserDto updatedUserDto = this.userService.updateUser(request.getUserDto());
        return ResponseEntity.ok(updatedUserDto);
    } 
 }
```
- @Valid: JSR-303 표준 스펙(자바 진영 스펙)으로 해당 객체의 제약조건을 검증하게 한다.
- UpdateUserRequest 앞에 @Valid 어노테이션을 붙여 request 내의 제약조건이 있는 field의 검증을 진행한다.

### 결과

![](https://velog.velcdn.com/images/taez224/post/f1ffa962-35c8-43e4-bd13-8f692b7bced9/image.png)  
![](https://velog.velcdn.com/images/taez224/post/79b46c39-1ca2-42c0-b175-b240ad8d3f35/image.png)

MethodArgumentNotValidException이 발생하는데 DefaultHandlerExceptionResolver가 처리하면서 400으로 떨어뜨린다.  
이번에는 우리가 직접 저 Exception을 간단하게 핸들링해보자.

## 번외) ExceptionHandling

```java
@RestControllerAdvice
@RequiredArgsConstructor
public class ValidationExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidationExceptions(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errors);
    }
}
```

`@RestControllerAdvice` 를 하나 만들어서 `MethodArgumentNotValidException` 처리를 위한 `@ExceptionHandler` 를 추가했다.  
간단하게 Exception안에 있는 errorMessage를 ResponseBody에 넣어줬다.

이렇게 하면..

![](https://velog.velcdn.com/images/taez224/post/f30e84a6-0d30-4f48-a368-fa25b6fc9117/image.png)

userRole 검증 실패 시

![](https://velog.velcdn.com/images/taez224/post/1b7e153c-74c8-4428-bde0-0c8961e7c1b9/image.png)

userId와 userRole 모두 검증 실패 시
