---
title: WebSocket에 Spring Security, JWT 적용해보기
created: 2023-03-20
published: 2023-03-20
tags:
  - blog
  - 개발/Java
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/WebSocket%EC%97%90-Spring-Security-JWT-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0
summary: WebSocket CONNECT 단계에 Spring Security JWT 인증을 연결해 SecurityContext와 MongoDB 감사 정보를 복원한 방법.
---

# WebSocket에 Spring Security, JWT 적용해보기

## 적용 계기

entity에 생성일과 생성한 사용자 등을 관리하려는 중 **WebSocket** 통신으로 이루어진 채팅 메세지는 생성한 `사용자 auditing이 안되는 현상` 을 발견하게 되는데...  
![chat-room](https://velog.velcdn.com/images/taez224/post/e6c0814d-3f00-4d28-9cc5-7b72b2b64138/image.png)  
http 통신으로 이루어진 Chat Room 등록은 user auditing이 잘 되는데

![chat-message](https://velog.velcdn.com/images/taez224/post/b825de2b-ec2d-44af-84c0-11c178665ddf/image.png)  
websocket으로 이루어진 Chat Message는 user auditing이 되지 않는다..

mongoDB를 사용중이기에 @EnablieMongoAuditing이 걸려있었고 사용자 정보는 아래와 같이 SecurityContext에서 가지고 오고 있었다.

```java
public class SpringSecurityAuditorAware implements AuditorAware<String> {
    @Override
    public Optional<String> getCurrentAuditor() {

        return Optional.ofNullable(SecurityContextHolder.getContext())
                .map(SecurityContext::getAuthentication)
                .filter(Authentication::isAuthenticated)
                .map(Authentication::getPrincipal)
                .map(CustomUserDetails.class::cast)
                .map(CustomUserDetails::getUserId)
                ;
    }
}
```

확인해보니 SecurityContextHolder.getContext()가 null 이어서 못 가지고 온 것이었다.

## 원인

- http와 WebSocket의 Security chain, config는 완전히 독립적.
- 기존 AuthenticationProvider는 Websocket Authentication에 관여하지 않는다.
- Websocket에 CONNECT 되면 해당 user는 websocket session에 저장되며 이후 메세지에는 인증 과정을 거치지 않는다.

## 기존 상태

WebSocket CONNECT 시에만 JWT를 통해서 인증하고 이후에는 검증하지 않았다.

- WebSocketInterceptor.java
```java
public class WebSocketInterceptor implements ChannelInterceptor {

    private final JwtProvider jwtProvider;

    @SneakyThrows
    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);

        if (accessor.getCommand() == StompCommand.CONNECT) {
            String authToken = accessor.getFirstNativeHeader("Authorization");

            if (authToken == null || !jwtProvider.validateJwt(authToken)) {
                throw new AuthException("Authentication failed!!");
            }
        }
        return message;
    }
}
```
- WebSocketConfig.java
```java
@RequiredArgsConstructor
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    private final WebSocketInterceptor webSocketInterceptor;

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/sub");
        config.setApplicationDestinationPrefixes("/pub");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws/chat").setAllowedOriginPatterns("*").withSockJS();
    }

    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        registration.interceptors(webSocketInterceptor);
    }
}
```

## 적용하기

1. 먼저 build.gradle에 해당 dependency를 추가해준다
	`implementation("org.springframework.security:spring-security-messaging")`
2. `AbstractSecurityWebSocketMessageBrokerConfigurer` 를 상속받은 `SecurityWebSocketConfig` 를 작성한다.
```java
@Configuration
public class SecurityWebSocketConfig extends AbstractSecurityWebSocketMessageBrokerConfigurer {

    @Override
    protected void configureInbound(MessageSecurityMetadataSourceRegistry message) {
        message
                .nullDestMatcher().permitAll()
                .simpDestMatchers("/pub/**").authenticated()
                .simpSubscribeDestMatchers("/sub/**").authenticated()
                .anyMessage().denyAll()
                ;
    }

    @Override
    protected boolean sameOriginDisabled() {
        return true;
    }
}
```
- nullDestMatcher()
	- CONNECT, HEARTBEAT 등은 permitAll()로 열여준다.
- simpDestMatchers()
	- destination이 /pub/\*\* 인 메세지는 인증 된 사용자(authenticated())만 전송 가능
- simpSubscribeDestMatchers()
	- 인증 된 사용자만 /sub/\*\* subscribe 가능
- anyMessage()
	- 이외의 다른 모든 message는 허용하지 않는다 (denyAll())
- sameOriginDisabled()
	- 개발 중 CSRF 비활성화를 위해 true로 설정
3. WebSocketInterceptor 수정
```java
public class WebSocketInterceptor implements ChannelInterceptor {

    private final JwtProvider jwtProvider;

    @SneakyThrows
    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor = MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);

        if (accessor.getCommand() == StompCommand.CONNECT) {
            String authToken = accessor.getFirstNativeHeader("Authorization");

            if (authToken == null || !jwtProvider.validateJwt(authToken)) {
                throw new AuthException("Authentication failed!!");
            }

            // UsernamePasswordAuthenticationToken 발급
            UsernamePasswordAuthenticationToken authentication = jwtProvider.getAuthentication(authToken);
            // accessor에 등록
            accessor.setUser(authentication);

        }

        return message;
    }
}
```
- CONNECT 시에 JWT 검증을 통과한 뒤 해당 토큰을 바탕으로 UsernamePasswordAuthenticationToken을 발급해 accessor의 user로 등록해준다.
4. WebSocketConfig 수정
```java
@Order(Ordered.HIGHEST_PRECEDENCE + 99)
@RequiredArgsConstructor
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    private final WebSocketInterceptor webSocketInterceptor;
...
}
```
- @Order(Ordered.HIGHEST\_PRECEDENCE + 99) 를 통해 WebSocketInterceptor가 먼저 처리될 수 있도록 설정

## 결과

![](https://velog.velcdn.com/images/taez224/post/6e021802-1fe6-4038-8d07-0b5abb93c237/image.png)  
![](https://velog.velcdn.com/images/taez224/post/e82b4881-9406-4e43-b31e-e250b8439139/image.png)
