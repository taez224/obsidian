---
title: Spring Boot와 JPA로 시작하는 데이터베이스 멀티테넌시
created: 2026-10-06
slug: spring-jpa-database-multitenancy
tags:
  - 개발/데이터베이스
  - 개발/Spring
status: draft
author: TaeZ
summary: 하나의 애플리케이션에서 테넌트별 데이터를 어떻게 분리할까요? Spring Boot와 JPA 예제로 스키마·DB 분리의 원리와 조회·수정 흐름을 살펴봅니다.
---

# Spring Boot와 JPA로 시작하는 데이터베이스 멀티테넌시

여러 고객사의 데이터를 같은 테이블에 저장한다면, 조회할 때 어떤 고객사의 데이터인지 구분해야 합니다. 이 방식에서는 단건 조회뿐 아니라 검색과 집계, 수정·삭제 쿼리마다 `tenantId` 조건을 직접 넣어야 합니다.

예를 들어, 같은 테이블에서 고객사별 주문을 관리하는 Repository라면 다음처럼 됩니다.

```java
interface OrderRepository extends JpaRepository<Order, Long> {
    Optional<Order> findByOrderIdAndTenantId(String orderId, String tenantId);

    List<Order> findAllByStatusAndTenantId(String status, String tenantId);

    long countByStatusAndTenantId(String status, String tenantId);
}
```

조건을 빠뜨려도 쿼리는 오류 없이 실행될 수 있습니다. 조회 결과에 다른 고객사의 데이터가 섞이거나, 수정·삭제가 다른 고객사의 데이터에 적용될 수도 있습니다.

테넌트 조건을 쿼리에 넣는 대신, 스키마나 DB를 테넌트별로 나누는 방법도 있습니다. 멀티테넌시 기능을 구현하며 다뤘던 이 두 방식을 Spring Boot와 JPA 예제로 옮겨, Repository 코드를 바꾸지 않고 고객사별 데이터를 조회하고 수정해 봤습니다.

> **예제 환경**
>
> Java 25 · Spring Boot 4.1.1 · Hibernate ORM 7.4.5.Final · PostgreSQL 17
>
> Spring Data JPA 등 의존성은 Spring Boot가 관리하는 버전을 사용했습니다.

> [!info] 코드 발췌 안내
> 본문에는 원리를 설명하는 데 필요한 코드만 실었습니다. import·생성자·getter·보조 메서드와 부가 빈 설정, 접속 계정, 테스트의 DB 준비·초기화 및 나머지 테스트는 생략했습니다. 필터 코드는 헤더 검증과 try/catch를 생략하고, 테넌트 바인딩과 요청 처리 부분만 보여 줍니다.

## 테넌트와 데이터 분리 방식

멀티테넌시는 여러 고객사나 조직이 하나의 서비스를 함께 사용하는 구조입니다. 이때 데이터를 구분하는 고객사·조직 등의 단위를 테넌트라고 합니다. 한 테넌트에 여러 사용자가 속할 수 있고, 한 사용자가 여러 테넌트에 속할 수도 있습니다.[^tenant-membership] 따라서 사용자 ID와 테넌트 ID는 구분해야 합니다. 애플리케이션을 공유하더라도 각 테넌트의 DB까지 같을 필요는 없습니다.[^azure-patterns]

관계형 DB에서 데이터를 나누는 대표적인 방법은 세 가지이며, 구분하는 단위가 행, 스키마, DB로 달라집니다.[^tenancy-models] 스키마는 DB 안에서 테이블 등의 객체를 묶는 네임스페이스입니다.

| 방식 | 데이터 배치 | 조회 범위를 정하는 지점 |
| --- | --- | --- |
| 행 단위 격리 (Discriminator column) | 같은 테이블에 여러 테넌트의 데이터를 저장 | SQL의 테넌트 조건 (`tenant_id`) |
| 스키마 분리 (Schema per tenant) | 같은 DB 안의 테넌트별 스키마에 테이블 구성 | 커넥션에서 사용할 스키마 |
| DB 분리 (Database per tenant) | 테넌트별 DB에 테이블 구성 | 커넥션을 얻을 DataSource |

스키마·DB 분리에서는 Hibernate가 테넌트 식별자를 애플리케이션이 등록한 구현에 넘겨 스키마나 DataSource를 정합니다. 따라서 업무 코드는 테넌트마다 다른 Repository를 호출하지 않아도, 테넌트에 맞는 스키마나 DB에서 데이터를 조회하고 수정할 수 있습니다.[^hibernate]

행 단위 격리에서도 개발자가 모든 쿼리에 조건을 직접 작성해야 하는 것은 아닙니다. Hibernate의 `@TenantId`나 DB의 행 수준 보안(RLS) 정책으로 조건을 적용할 수 있습니다.[^row-security] 다만 Hibernate가 `@TenantId`로 붙이는 테넌트 조건은 네이티브 SQL에는 적용되지 않습니다.[^hibernate] Hibernate 세션으로 실행하면 DB 분리에서는 네이티브 SQL도 선택한 DB에서 실행되고, 스키마 분리에서는 스키마 이름을 생략한 테이블 참조에 선택한 스키마가 적용됩니다.

저장 위치를 나누는 것과 접근 권한을 제한하는 것은 구분해야 합니다. 스키마를 선택해도 다른 스키마의 접근 권한까지 바뀌지는 않습니다. 아래 예제는 같은 계정으로 두 스키마에 접근하며, 같은 PostgreSQL 인스턴스 안에서 DB를 나누므로 서버 자원도 공유합니다.

## 두 방식의 공통 예제

예제에서는 Marvel과 DC를 테넌트로 삼아 캐스팅 목록을 따로 준비했습니다. Ryan Reynolds의 배역은 Marvel에서는 `Deadpool`, DC에서는 `Green Lantern`입니다. 테넌트마다 배우별 배역을 하나씩 저장하고, 배우 식별자인 `actorSlug`를 각 테이블의 기본 키로 사용합니다.

| 세계관(테넌트) | 배우 식별자 (`actorSlug`) | 배역 (`characterName`) |
| --- | --- | --- |
| Marvel (`marvel`) | `ryan-reynolds` | Deadpool |
| DC (`dc`) | `ryan-reynolds` | Green Lantern |

같은 배우를 조회해도 세계관에 맞는 배역이 나오는지, Marvel의 배역명을 바꿔도 DC의 배역은 유지되는지 확인합니다.

예제는 두 방식을 `schema`와 `database` Profile로 나눴습니다. 두 Profile은 같은 API를 사용하고 저장 위치만 다릅니다. 테넌트별 저장 위치는 설정에 둡니다. `demo` 아래 키는 예제에서 정의한 것입니다.

```yaml
spring:
  jpa:
    open-in-view: false  # 요청 전체에 세션을 유지하지 않음
demo:
  admin-url: jdbc:postgresql://localhost:55432/control  # control DB: database Profile이 테넌트 없이 쓰는 DB
  shared-url: jdbc:postgresql://localhost:55432/shared  # schema Profile이 연결하는 DB
  schemas:    # schema Profile: 테넌트 ID → 스키마
    marvel: marvel_schema
    dc: dc_schema
  databases:  # database Profile: 테넌트 ID → DB
    marvel: jdbc:postgresql://localhost:55432/marvel_db
    dc: jdbc:postgresql://localhost:55432/dc_db
```

DB와 스키마, `casting` 테이블은 초기화 스크립트로 미리 만들었습니다. 두 Profile의 Entity와 Repository 코드는 같습니다.

```java
@Entity
@Table(name = "casting")
public class Casting {
    @Id
    @Column(name = "actor_slug")
    private String actorSlug;
    @Column(name = "character_name")
    private String characterName;
}

public interface CastingRepository extends JpaRepository<Casting, String> {}
```

`CastingService.findByActor()`는 배우 식별자로 `CastingRepository.findById()`를 호출합니다. `changeCharacterName()`도 같은 배역 조회 코드를 사용해 배역명을 바꿉니다. 두 메서드 모두 `@Transactional`이며, 세계관마다 다른 Repository를 호출하는 분기는 없습니다.

## 요청의 테넌트를 세션에 전달

이 예제의 JPA `EntityManager`는 Hibernate의 `Session`을 기반으로 동작합니다. 세션은 열릴 때 정해진 테넌트를 계속 사용하므로, 세션이 열리기 전에 요청의 테넌트 식별자를 Hibernate에 전달해야 합니다.[^hibernate] 예제에서는 서블릿 필터가 `X-Tenant-Id` 헤더에서 테넌트를 확인합니다.

```text
필터에서 테넌트 확인
  → 요청 처리 범위에 테넌트 바인딩
  → @Transactional 서비스 호출
  → Hibernate 세션에 테넌트 지정
  → 테넌트에 맞는 스키마 또는 DB에서 조회·수정
```

### 요청 처리 동안 테넌트 보관

요청에서 얻은 테넌트 ID를 하위 메서드마다 인자로 넘기는 대신, 요청을 처리하는 동안 사용할 컨텍스트에 보관합니다. 이런 컨텍스트에는 `ThreadLocal`을 흔히 사용합니다.

이번 예제에서는 요청 초기에 정한 테넌트 ID를 하위 호출에서 읽기만 하므로, Java 25의 `ScopedValue`를 선택했습니다.[^scoped-value] 테넌트 ID를 실행 범위에 연결해 두는 것을 바인딩이라고 합니다.

예제의 `TenantContext`는 `ScopedValue`를 감싼 보조 클래스입니다.

```java
public final class TenantContext {
    private static final ScopedValue<String> CURRENT = ScopedValue.newInstance();

    // 지정한 테넌트를 바인딩한 범위에서 작업을 실행한다.
    public static <T> T call(String tenant, Supplier<T> work) {
        return ScopedValue.where(CURRENT, tenant).call(work::get);
    }

    // 바인딩된 테넌트를 읽는다. 바인딩 범위 밖에서 호출하면 예외가 발생한다.
    public static String required() {
        if (!CURRENT.isBound()) {
            throw new IllegalStateException("No tenant is bound");
        }
        return CURRENT.get();
    }
}
```

필터는 헤더에서 확인한 테넌트를 바인딩하고, 그 범위에서 나머지 요청을 처리합니다. 필터에서 쓰는 `callChecked()`는 `call()`과 같은 방식으로 바인딩하며, 작업에서 발생한 Checked Exception을 호출한 곳으로 던질 수 있습니다.

```java
public class TenantFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        String tenant = request.getHeader("X-Tenant-Id");
        TenantContext.callChecked(tenant, () -> {
            chain.doFilter(request, response);  // 나머지 요청 처리는 이 바인딩 범위 안에서 실행된다.
            return null;
        });
    }
}
```

테넌트 바인딩은 `TenantContext`가, 트랜잭션은 서비스의 `@Transactional`이 담당합니다.

> [!info]- ThreadLocal과 ScopedValue 비교
>
> | 구분 | `ThreadLocal` | `ScopedValue` |
> | --- | --- | --- |
> | 값의 수명 | 직접 제거하거나 스레드가 끝날 때까지 유지 | 지정한 실행 범위가 끝날 때까지 유지 |
> | 종료 시 정리 | 보통 `finally`에서 `remove()` | 정상·예외 종료 시 바인딩 자동 해제 |
> | 중첩된 값 사용 | 이전 값을 직접 저장·복원 | 안쪽 범위 종료 후 이전 바인딩 복원 |
>
> `ThreadLocal`에서 `ScopedValue`로 옮기는 과정과 서블릿 필터 적용은 넥스트리의 [컨텍스트 전파 리팩토링 영상 강좌](https://www.nextree.io/modeon-baegendeu-keontegseuteu-jeonpa-ripaegtoring-1/)에서 살펴볼 수 있습니다.

### Hibernate에 테넌트 전달

Hibernate는 `CurrentTenantIdentifierResolver`로 새 세션에 사용할 테넌트 식별자를 얻습니다. 예제의 `TenantResolver`는 앞에서 바인딩한 테넌트를 읽어 반환합니다.

```java
public class TenantResolver implements CurrentTenantIdentifierResolver<String> {
    private final TenantProperties tenants;  // 설정의 demo 값

    @Override
    public String resolveCurrentTenantIdentifier() {
        String tenant = TenantContext.required();
        // 설정에 등록된 테넌트인지 확인한다.
        if (!tenants.knows(tenant)) {
            throw new IllegalArgumentException("Unknown tenant: " + tenant);
        }
        return tenant;
    }
}
```

필터를 거치지 않고 서비스를 호출해도, 테넌트가 바인딩되지 않았거나 등록되지 않은 테넌트라면 Resolver가 예외를 던져 세션이 열리지 않습니다.

Resolver를 Spring Boot의 `HibernatePropertiesCustomizer`로 Hibernate 속성에 추가합니다. 뒤에서 다룰 `TenantSchemaMapper`와 `MultiTenantConnectionProvider`도 같은 방식으로 등록합니다.

```java
@Configuration
public class TenantConfiguration {
    @Bean
    HibernatePropertiesCustomizer tenantIdentity(TenantResolver resolver) {
        return properties -> properties.put(
                MultiTenancySettings.MULTI_TENANT_IDENTIFIER_RESOLVER, resolver);
    }
}
```

## 스키마 분리: 같은 DB에서 스키마 선택

예제의 스키마 분리는 DataSource 하나로 `shared` DB에 연결하고, 테넌트에 따라 사용할 스키마를 바꿉니다. 앞의 Resolver는 그대로 두고, 같은 `TenantConfiguration` 안의 `Schema` 설정에서 Hibernate 7.1부터 제공하는 `TenantSchemaMapper`로 스키마를 정합니다.[^schema]

```java
@Configuration
public class TenantConfiguration {
    @Configuration
    @Profile("schema & !database")  // schema 활성화·database 비활성화일 때 적용한다.
    static class Schema {
        @Bean
        TenantSchemaMapper<String> schemaMapper(TenantProperties properties) {
            return tenant -> {
                // demo.schemas에서 테넌트 ID에 맞는 스키마 이름을 찾는다.
                String schema = properties.schemas().get(tenant);
                if (schema == null) {
                    throw new IllegalArgumentException("Unknown tenant: " + tenant);
                }
                return schema;
            };
        }
    }
}
```

위 매퍼 빈을 앞에서 사용한 `HibernatePropertiesCustomizer`로 등록합니다. `schema` Profile의 등록 부분만 발췌하면 다음과 같습니다.

```java
properties.put(MultiTenancySettings.MULTI_TENANT_SCHEMA_MAPPER, mapper);
```

Hibernate는 커넥션을 얻을 때 세션의 테넌트 식별자로 매퍼를 호출하고, 반환된 이름으로 `Connection.setSchema()`를 호출합니다.[^schema] 그래서 같은 배우를 조회해도 Marvel 세션에서는 `marvel_schema.casting`을, DC 세션에서는 `dc_schema.casting`을 읽습니다.

## DB 분리: 테넌트별 DataSource 선택

DB 분리에서는 스키마를 바꾸는 대신, 테넌트에 맞는 DB의 DataSource를 선택합니다. 예제는 기동할 때 `demo.databases`의 접속 정보로 테넌트별 HikariCP 풀을 만들어 둡니다.

Hibernate는 커넥션이 필요할 때 세션의 테넌트 식별자를 `MultiTenantConnectionProvider`에 전달합니다.[^hibernate][^provider] 예제의 `Connections.Provider`는 Hibernate가 제공하는 DataSource 기반 추상 클래스를 상속해 DataSource 선택 메서드를 재정의합니다.

```java
public static final class Provider
        extends AbstractDataSourceBasedMultiTenantConnectionProviderImpl<String> {
    private final Catalog catalog;      // 테넌트별 풀을 보관하는 예제의 보조 객체
    private final DataSource metadata;  // control DB의 DataSource

    @Override
    protected DataSource selectDataSource(String tenant) {
        // 컨텍스트를 다시 읽지 않고, 세션이 넘긴 테넌트 식별자를 사용한다.
        return catalog.require(tenant);
    }

    @Override
    protected DataSource selectAnyDataSource() {
        // 기동 중 메타데이터 조회처럼 테넌트가 정해지지 않았을 때 쓴다.
        return metadata;
    }
}
```

테넌트가 정해지지 않은 메타데이터 조회를 테넌트 DB와 분리하려고, 업무 테이블이 없는 `control` DB를 사용했습니다. `MultiTenantConnectionProvider` 구현은 Spring 빈으로 등록한 뒤, 앞과 같이 `HibernatePropertiesCustomizer`로 Hibernate 속성에 추가합니다. 아래는 `database` Profile의 등록 부분입니다.

```java
properties.put(MultiTenancySettings.MULTI_TENANT_CONNECTION_PROVIDER, provider);
```

이제 Marvel용 세션에서 `findById("ryan-reynolds")`를 호출하면 `marvel_db`에서, DC용 세션에서는 `dc_db`에서 배역을 읽습니다. Repository는 어느 DataSource가 선택됐는지 알 필요가 없습니다.

## 같은 테스트로 조회·수정 확인

조회 API에는 테넌트 헤더를 보냅니다. 예를 들어 Marvel의 배역은 다음처럼 조회합니다.

```bash
curl -s -H 'X-Tenant-Id: marvel' http://localhost:8080/castings/ryan-reynolds
# {"tenant":"marvel","actorSlug":"ryan-reynolds","characterName":"Deadpool"}
```

다음 공통 통합 테스트는 테넌트별 조회 결과와 함께, 한 테넌트의 수정이 다른 테넌트에 영향을 주지 않는지 확인합니다. 테스트마다 Marvel의 배역을 `Deadpool`, DC의 배역을 `Green Lantern`으로 초기화하고, 바깥 트랜잭션이 없는 상태에서 Spring이 주입한 `CastingService`를 호출합니다.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
abstract class TenantApiTest {
    @Autowired
    CastingService castingService;

    @Test
    void sameActorReturnsDifferentCharacters() {
        var marvelCasting = TenantContext.call("marvel", () ->
                castingService.findByActor("ryan-reynolds"));
        var dcCasting = TenantContext.call("dc", () ->
                castingService.findByActor("ryan-reynolds"));
        assertThat(marvelCasting.characterName()).isEqualTo("Deadpool");
        assertThat(dcCasting.characterName()).isEqualTo("Green Lantern");
    }

    @Test
    void characterNameChangeDoesNotAffectOtherTenant() {
        TenantContext.call("marvel", () ->
                castingService.changeCharacterName("ryan-reynolds", "Deadpool (updated)"));
        var marvelCasting = TenantContext.call("marvel", () ->
                castingService.findByActor("ryan-reynolds"));
        var dcCasting = TenantContext.call("dc", () ->
                castingService.findByActor("ryan-reynolds"));
        assertThat(marvelCasting.characterName()).isEqualTo("Deadpool (updated)");
        assertThat(dcCasting.characterName()).isEqualTo("Green Lantern");
    }
}
```

`SchemaModeTest`와 `DatabaseModeTest`는 이 클래스를 상속해 공통 테스트를 그대로 실행하고, `@ActiveProfiles`로 각자의 Profile을 지정합니다. PostgreSQL 17에서 두 Profile 모두 이 테스트를 통과했습니다.

스키마 분리에서는 같은 커넥션을 재사용해도 현재 테넌트의 데이터를 읽어야 합니다. 예제의 풀 크기는 1이므로, 같은 커넥션으로 Marvel → DC → Marvel 순서로 조회했을 때도 각 테넌트의 배역이 반환됐고, 커넥션을 반납한 뒤에는 스키마가 원래 값으로 돌아왔습니다.

## 테넌트 전환과 트랜잭션

조회할 테넌트를 바꾸려면 새 세션이 열리기 전에, 이 예제에서는 서비스 트랜잭션을 시작하기 전에 테넌트 ID를 바인딩해야 합니다. 별도 테스트에서 이미 Marvel용으로 열린 트랜잭션 안에서 컨텍스트만 DC로 바꾼 뒤, 같은 배우의 배역을 조회해 봤습니다. 세션의 테넌트는 Marvel로 유지됐고, 오류 없이 `Deadpool`이 반환됐습니다. 요청한 테넌트와 다른 데이터를 읽어도 예외로 드러나지 않습니다.

앞의 첫 테스트가 올바른 호출 순서를 보여 줍니다. 두 호출을 감싸는 바깥 트랜잭션이 없으므로, 첫 호출은 Marvel용 세션·트랜잭션에서 `Deadpool`을 읽고 종료합니다. 두 번째 호출은 DC용 세션·트랜잭션을 새로 열어 `Green Lantern`을 읽습니다.

배치나 스케줄러에서 테넌트를 순회할 때도 각 작업의 트랜잭션을 시작하기 전에 테넌트를 바인딩해야 합니다.

> [!note] OSIV를 켠 경우
> Spring Boot는 웹 애플리케이션에서 기본적으로 Open EntityManager in View(OSIV)를 적용해 요청 전체에 같은 EntityManager를 유지합니다. 이때는 요청 안에서 컨텍스트만 다른 테넌트로 바꿔도 기존 세션의 테넌트가 계속 쓰입니다. 예제는 바깥 트랜잭션 없이 서비스를 호출하며, 서비스 트랜잭션마다 새 세션을 사용하도록 `open-in-view: false`로 설정했습니다.[^osiv]

## 운영에서 더 따져 볼 것

예제는 미리 준비한 스키마와 DB에서 테넌트별 조회·수정 동작을 확인했습니다. 운영에 적용할 때는 아래 항목을 함께 정해야 합니다.

- **사용자 접근 권한:** 로그인한 사용자가 요청한 테넌트에 접근할 수 있고 그 작업을 할 권한이 있는지 확인해야 합니다.
- **DB 계정과 권한:** 애플리케이션의 DB 계정이 접근할 수 있는 DB·스키마·테이블을 제한하고, 테넌트별 계정을 쓸 경우 접속 정보와 풀 관리 방식도 정해야 합니다.
- **전체 커넥션 수:** 테넌트 수, 애플리케이션 인스턴스 수, 풀 크기를 함께 보고 DB가 감당할 커넥션 수를 산정해야 합니다.
- **테넌트 추가와 풀 수명:** DB·스키마·테이블 준비, 테넌트 등록, 풀 생성·종료 시점을 정해야 합니다. 예제는 기동 시 설정된 목록을 사용합니다.
- **테이블 구조 변경:** 모든 테넌트에 마이그레이션을 적용할 순서와 실패했을 때의 복구 방법을 정해야 합니다.
- **백업·복구 단위:** 특정 테넌트만 복구할 수 있는지, 사용하는 DB 서비스의 복구 단위가 요구에 맞는지 확인해야 합니다.[^azure-patterns]
- **공유 자원의 부하:** 같은 DB 인스턴스의 CPU·메모리·I/O를 공유하는 테넌트 사이에서 부하 간섭을 살펴야 합니다.
- **공용 DB 병용:** 테넌트별 데이터와 공용 데이터를 함께 읽는 경우, 조회 경로와 트랜잭션 구성을 별도로 정해야 합니다.

## 마치며

스키마 분리에서는 같은 DB 안에서 사용할 스키마를 정하고, DB 분리에서는 테넌트별 DataSource를 선택했습니다. 두 방식 모두 Entity와 Repository, 배역 조회·배역명 변경 서비스를 그대로 사용할 수 있었습니다.

이 구조에서 테넌트를 정하는 시점은 세션이 열리기 전입니다. 같은 배우에 서로 다른 배역을 넣은 작은 예제만으로도, 요청한 테넌트의 데이터를 조회하고 수정하는지 확인할 수 있습니다.

[^tenant-membership]: Wonkook Lee, [테넌트·테넌시 개념과 싱글테넌시·멀티테넌시 비교](https://blog.wonkooklee.com/docs/software-design-and-theory/tenancy-fundamentals/). 사용자와 테넌트의 소속 관계를 설명합니다.
[^azure-patterns]: Microsoft Learn, [다중 테넌트 SaaS 데이터베이스 테넌시 패턴](https://learn.microsoft.com/ko-kr/azure/azure-sql/database/saas-tenancy-app-design-patterns?view=azuresql). 애플리케이션과 DB의 공유 범위, 테넌트별 복구와 운영 선택을 설명합니다.
[^tenancy-models]: Microsoft Learn, [Design your SaaS database for scale with PostgreSQL](https://learn.microsoft.com/en-us/postgresql/citus/designing-saas?view=citus-14). 테넌트별 DB, 테넌트별 스키마, 테이블 공유의 세 가지 배치를 설명합니다.
[^hibernate]: Hibernate ORM, [A Short Guide to Hibernate 7: Multi-tenancy](https://docs.hibernate.org/orm/7.4/introduction/html_single/#multitenancy). 세 가지 멀티테넌시 방식과 세션의 테넌트 지정을 설명하며, `@TenantId` 조건이 네이티브 SQL에 적용되지 않는다고 명시합니다.
[^row-security]: PostgreSQL 17, [Row Security Policies](https://www.postgresql.org/docs/17/ddl-rowsecurity.html). 정책으로 조회·추가·수정·삭제할 행을 제한하는 기능을 설명합니다.
[^scoped-value]: Oracle, [Java 25 ScopedValue](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.html). 실행 범위 종료 시 바인딩 해제와 중첩 범위 종료 후 이전 바인딩 복원을 설명합니다.
[^osiv]: Spring Boot, [SQL Databases](https://docs.spring.io/spring-boot/reference/data/sql.html). Spring Boot가 기본으로 OSIV를 적용하며, `spring.jpa.open-in-view`로 끌 수 있다고 설명합니다.
[^schema]: Hibernate ORM, [TenantSchemaMapper](https://docs.hibernate.org/orm/7.4/javadocs/org/hibernate/context/spi/TenantSchemaMapper.html). 7.1에 추가된 `@Incubating` API입니다. [`MultiTenancySettings`](https://docs.hibernate.org/orm/7.4/javadocs/org/hibernate/cfg/MultiTenancySettings.html#MULTI_TENANT_SCHEMA_MAPPER)로 등록하면 Hibernate가 반환된 이름으로 `Connection.setSchema()`를 호출합니다. 7.1 이전에는 [`MultiTenantConnectionProvider`](https://docs.hibernate.org/orm/6.6/userguide/html_single/#multitenacy)에서 커넥션의 스키마를 지정할 수 있습니다.
[^provider]: Hibernate ORM, [MultiTenantConnectionProvider](https://docs.hibernate.org/orm/7.4/javadocs/org/hibernate/engine/jdbc/connections/spi/MultiTenantConnectionProvider.html). 테넌트별 커넥션 제공과 반납 계약을 설명합니다.
