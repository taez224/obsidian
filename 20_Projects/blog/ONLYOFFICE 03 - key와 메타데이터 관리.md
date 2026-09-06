---
title: "ONLYOFFICE 연동 3편: key와 메타데이터 관리"
created: 2026-01-14
published: 2026-01-14
tags:
  - 프로젝트/onlyoffice-demo
  - blog
  - 개발/인프라
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/ONLYOFFICE-%EC%97%B0%EB%8F%99-%EA%B5%AC%EC%B6%95%EA%B8%B0-3%ED%8E%B8
series: ONLYOFFICE 연동 바이브코딩 기록
series_order: 3
summary: document.key와 referenceData.fileKey를 분리하고 SAVE·FORCESAVE를 구분해 문서 메타데이터와 버전을 관리한 구현 기록.
related:
  - "[[onlyoffice-demo|ONLYOFFICE 연동]]"
  - "[[ONLYOFFICE 02 - Antigravity와 함께한 Vibe Coding기|2편: 기본 연동 구현]]"
  - "[[ONLYOFFICE 04 - SDK, MinIO, Saga|4편: SDK, MinIO, Saga]]"
---

# ONLYOFFICE 연동 3편: key와 메타데이터 관리

## TL;DR by 🤖

> ONLYOFFICE를 연동하다 보면 언젠가 반드시 마주치는 질문이 있다.
> 
> ```
> “왜 어떤 경우에는 저장이 잘 되는데,
> 어떤 경우에는 동시 편집이 깨질까?”
> ```
> 
> 이 문제의 원인은 대부분 **ONLYOFFICE의 key 설계와 저장 메커니즘을 정확히 이해하지 못한 상태에서 구현을 시작했기 때문** 이다.
> 
> 이 글에서는
> 
> - ONLYOFFICE의 `document.key` 와 `referenceData.fileKey` 의 역할 차이
> - `SAVE` 와 `FORCESAVE` 가 내부적으로 어떻게 동작하는지
> - 실제 서비스에서는 어떤 기준으로 key와 버전을 관리해야 하는지
> 
> 를 **가상 시나리오와 구현 코드** 를 바탕으로 정리한다.

---

## 3편에서는...

2편에서는 **ONLYOFFICE** 를 연동하는 최소한의 코드를 작성했지만, 그야말로 PoC 수준이므로 여러 문제가 남아있다.

### 2편의 문제점

- `fileName` 을 식별자로 사용
- 문서 메타데이터 관리 부재
- `ONLYOFFICE` 관련 하드코딩된 부분 존재
- 로컬 파일시스템에 파일 저장  
	등등...

### 3편에서 해결할 것

- **파일 식별자 `fileName → fileKey` 전환**: ONLYOFFICE의 document key 스펙 이해 및 적용
- **PostgreSQL + JPA 도입**: 문서 메타데이터 영구 저장
- **Callback 처리 개선**: `SAVE` vs `Force Save` 이해 및 구현
	- **ONLYOFFICE SDK** 적용을 통한 고도화는 **4편** 에 진행 예정

> **⚠️ 주의**: 파일시스템은 3편까지 로컬 저장소를 사용한다. **4편** 에서 **MinIO** 연동 예정.

---

## ONLYOFFICE key 스펙 이해하기

### Key의 두 가지 종류

ONLYOFFICE Config에는 두 종류의 key가 있다.

> 📚 **공식 문서**: [document.key](https://api.onlyoffice.com/editors/config/document#key) | [referenceData.fileKey](https://api.onlyoffice.com/editors/config/document#referencedata)

`document.key` 는 **편집 세션을 식별하기 위한 key** 다.  
**ONLYOFFICE Document Server** (이하 ONLYOFFICE 서버)는 이 key를 기준으로 문서를 캐싱하고, 동일한 key로 접속한 사용자들을 하나의 **co-editing 세션** 으로 묶는다.  
따라서 파일 수정 후 저장될 때마다 반드시 **새 key로 갱신** 되어야 한다.

반면 `referenceData.fileKey` 는 **파일 자체를 영구적으로 식별하기 위한 key** 다.  
문서의 버전이 바뀌더라도 이 값은 유지되어야 하며, 항상 **"같은 파일"을 가리키는 기준** 이 된다.

> 💡 이 프로젝트에서는 단순하게
> 
> - `fileKey` 는 파일 등록 시 **UUID** 로 생성하고
> - `document.key` 는 `{fileKey}_v{editorVersion}` 형태로 제공한다.

---

## ONLYOFFICE 저장 방식 이해하기

2편에서도 언급했지만, ONLYOFFICE 이해를 위해 아래 개념을 반드시 숙지해야한다.

> ONLYOFFICE는 파일 저장 시스템이 아니라,  
> key 단위로 문서 상태를 관리하는 외부 세션 서버에 가깝다.

**ONLYOFFICE** 는 co-editing 등을 위한 문서 상태 관리를 담당하며, 파일의 실제 저장과 버전 관리 등은 연동하려는 서비스 - *바로 우리* - 가 직접 책임져야 한다.  
우리의 프로젝트가 바로 ONLYOFFICE를 연동하기 위한 **Document Storage Service** 다.

이 전제를 확실히 이해해야 ONLYOFFICE의 두 가지 저장 방식, **SAVE** 와 **FORCESAVE** 의 차이를 이해할 수 있다.

### SAVE vs FORCESAVE

> 📚 **공식 문서**: [Saving](https://api.onlyoffice.com/docs/docs-api/get-started/how-it-works/saving-file/) | [Force Saving](https://api.onlyoffice.com/docs/docs-api/get-started/how-it-works/saving-file/#force-saving)

#### 편집 중인 파일은 어디에서 관리될까?

사용자가 ONLYOFFICE 에디터를 통해 문서를 열고 편집을 시작하면,  
변경 사항은 우리 서버가 아니라 **ONLYOFFICE Server** **내부 캐시** 에 저장된다.

이 캐시는 `document.key` 단위로 관리되며, 동일한 key로 접속한 사용자들은 같은 캐시를 공유해 실시간 **co-editing** 이 가능해진다.

> 💡 **보충 설명**: 사용자가 `ONLYOFFICE Token(config)` 를 통해 에디터를 열 때, 요청한 `document.key` 가 **캐시에 있으면 캐시된 문서를 바로 사용** 하고, **없으면 config의 `document.url` 을 통해 원본 파일을 내려받아 캐시에 적재** 한 뒤 편집 세션을 시작한다.

#### SAVE - 편집 세션이 끝났을 때 최종 반영

모든 사용자가 에디터를 종료하면,  
**ONLYOFFICE** 는 **SAVE 콜백** 을 우리의 **Document Storage Server** 로 보낸다.

이 시점에서 **Storage Server** 는 다음 작업을 수행한다.

- 최종 파일을 **ONLYOFFICE Server** 로부터 다운로드해 저장하고
- `editorVersion` 을 증가시키며
- 다음 편집 세션에서는 새로운 **`document.key`** 를 제공한다.

즉, **SAVE** 는 **편집 세션 종료 + 캐시 무효화** 가 함께 일어나는 안전한 저장 방식이다.

#### FORCESAVE - 세션이 끝나기 전 중간 반영

**FORCESAVE** 는 **편집 세션이 유지된 상태에서**  
**ONLYOFFICE Server** 캐시에 있는 **중간 결과물 파일** 을 강제로 Storage Server로 하여금 저장하게 하는 방식이다.

기본적으로 **FORCESAVE** 는 비활성화되어있으며, 이 때 에디터 상에서 `Ctrl + S` 등 저장 버튼을 클릭하면 해당 문서는 **ONLYOFFICE의 Document Server 내에 캐시로 저장** 된다.

하지만 **FORCESAVE를 활성화한 상태** 에서는 에디터에서 저장요청 시  
`ONLYOFFICE Document Server` 에서 우리의 `Storage Server` 로 **FORCESAVE Callback** 을 보낸다.  
그럼 우리는 이 콜백을 바탕으로 해당 시점의 파일을 파일시스템에 반영한다.

> **FORCESAVE 활성화 방법**
> 
> 기본적으로 **FORCESAVE** 는 비활성화되어있다. 사전 설정이나 token(config) 옵션 등을 통해 활성화할 수 있으며, 몇가지 ForceSave를 트리거할 수 있는 방식이 존재한다.
> 
> | forcesavetype | 트리거 방법 | 설정 |
> | --- | --- | --- |
> | 0 | Command Service API 호출 | `Document Command Service` 를 통해 `forcesave` 명령 전송 |
> | 1 | 저장 버튼 클릭 | `editorConfig.customization.forcesave: true` |
> | 2 | 서버 타이머 (Auto Assembly) | `services.CoAuthoring.autoAssembly.enable: true` |

> 📚 **공식 문서**:
> 
> - [Auto Assembly](https://helpcenter.onlyoffice.com/docs/installation/docs-developer-configuring.aspx#autoassembly_block)
> - [Command Service - forcesave](https://api.onlyoffice.com/docs/docs-api/additional-api/command-service/forcesave/)

**SAVE** 와 **FORCESAVE** 의 가장 큰 차이는 **편집 세션이 유지되는가 그렇지 않은가** 이다.

**SAVE** 콜백이 오면 **Storage Server** 에서 해당 파일을 저장하며 `editorVersion` 을 증가시킨다. 이렇게 하면 다음 편집 세션에서 새로운 `document.key` 가 생성되어 **ONLYOFFICE Server** 의 캐시는 자연스럽게 무효화된다.

하지만 **FORCESAVE** 과정에서 `editorVersion` 을 증가시키면 문제가 생긴다.

> **FORCESAVE 활성화 + editorVersion 증가 시**
> 
> 1. **User A, B** 가 `doc_v3` 의 `document.key` 로 co-editing 중...
> 2. **User A** 가 편집 중 **저장 버튼 클릭** → **FORCESAVE** 트리거
> 3. 이때 `editorVersion` 증가하면 → key는 `doc_v4` 로 갱신
> 4. **User B** 가 페이지 새로고침 → `doc_v4` 키로 **새 세션** 시작
> 5. **User A** 는 여전히 `doc_v3` 세션에 있음
> 6. 둘이 다른 세션! co-editing 깨짐

따라서

- **SAVE**: 편집 완료 → `editorVersion` 증가
- **FORCESAVE**: 편집 중 → `editorVersion` 유지

설명은 길게 했는데, 우리의 데모 프로젝트에서는 깔끔히 FORCESAVE 비활성화한다.

> 📚 **공식 문서**: [Callback Handler - ForceSave Status](https://api.onlyoffice.com/docs/docs-api/usage-api/callback-handler/#status)

---

> ### \[참고\] ONLYOFFICE SAVING SEQUENCE
> 
> ![sd](https://velog.velcdn.com/images/taez224/post/18af4094-b6af-44ee-ad29-238e2c3e235a/image.png)

---

## fileName → fileKey 마이그레이션

2편에서는 파일명(`sample.docx`)을 그대로 식별자로 사용했는데, 이제 UUID 기반의 `fileKey` 로 전환하자.

초반에 안잡으면 두고두고 헷갈리니 `fileKey` 와 `documentKey(editorKey)` 를 다시한번 정리하고 넘어가자.

### fileName vs fileKey vs document.key

> 💡 이 프로젝트에 적용 할 기준. 실제로는 각 환경에 맞게 커스터마이징 가능

| 구분 | fileName | fileKey | document key(editorKey) |
| --- | --- | --- | --- |
| **용도** | 사용자 표시용 | 파일 식별자 (불변) | 편집 세션용 |
| **예시** | `보고서_최종.docx` | `uuid-file-key` | `uuid-file-key_v3` |
| **생성 시점** | 업로드 시 (사용자 지정) | 업로드 시 (자동 생성) | editor config 요청 시 (계산) |
| **변경 여부** | ✅ 변경 가능 | ❌ 불변 | ✅ Save 시 변경 |
| **고유성** | 중복 허용 | 유일해야함 | 유일해야함 |
| **저장 위치** | DB (`file_name`) | DB (`file_key`) | `editorVersion` 만 DB, key는 계산 |
| **ONLYOFFICE 매핑** | `document.title` | `referenceData.fileKey` | `document.key` |

**editorKey 획득 예시:**

```java
// Document.java
public String getEditorKey() {
    return this.fileKey + "_v" + this.editorVersion;
}
```

> ### Editor 캐시 관련 주의사항
> 
> 현재 구현의 전제는 **"모든 편집은 ONLYOFFICE를 통해서만 발생한다"** 이다.
> 
> 만약 파일을 ONLYOFFICE 외부에서 직접 수정하면(파일 덮어쓰기 등) ONLYOFFICE Server 캐시와 실제 파일 간에 불일치가 발생할 수 있다.
> 
> 1. **User A** 가 문서 열기 → editorKey = `abc_v0`
> 2. Document Server가 `abc_v0` 키로 문서 캐싱
> 3. 외부에서 파일 직접 덮어씀 (ONLYOFFICE 거치지 않음)
> 4. `editorVersion` 은 그대로 0 (콜백이 없으니까)
> 5. **User B** 가 문서 열기 → editorKey = `abc_v0` (동일)
> 6. 🚨 Document Server가 **캐시된 예전 버전** 반환!
> 
> **해결 방안**
> 
> | 방안 | 설명 | 트레이드오프 |
> | --- | --- | --- |
> | **외부 수정 시 버전 증가** | 파일 덮어쓰기 API에서도 `editorVersion++` | 모든 수정 경로 추적 필요 |
> | **Command Service** | 외부 수정 후 `forcesave` 명령으로 캐시 무효화 | 추가 API 호출 필요 |

---

## Part 1: 인프라 셋업

문서의 메타데이터를 DB로 관리하기 위한 최소한의 실행 환경을 준비한다.  
2편에서 docker를 통해 onlyoffice 서버를 띄웠으니 추가로 간단히 postgres를 추가하자.

#### docker-compose.yml

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: onlyoffice-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data

  onlyoffice-docs:
    # 이전과 동일
```

#### .env 파일 예시

```
# PostgreSQL 관련 항목 추가
POSTGRES_DB=onlyoffice_demo
POSTGRES_USER=onlyoffice_demo_user
POSTGRES_PASSWORD=your-secure-password-here
```

---

## Part 2: Document Entity 설계

ONLYOFFICE 연동에서 핵심 필드는 다음과 같다.

- 파일을 영구적으로 식별하기 위한 `fileKey`
- ONLYOFFICE Server 캐시를 제어하기 위한 `editorVersion`

이 둘을 엔티티의 명시적인 필드로 관리하고

여기에 더해

- 엔티티 무결성을 위한 JPA `version`
- 상태 관리를 위한 `status` 필드와
- Soft Delete를 위한 `deleted_at`

등 문서의 편집 상태와 생명주기를 하나의 엔티티로 관리한다.

#### Document.java (핵심 필드만)

```java
@Entity
@Table(name = "documents")
public class Document {

    private String fileName;                    // 사용자 표시용

    @Column(unique = true)
    private String fileKey;                     // UUID, 불변 식별자

    private Integer editorVersion = 0;          // ONLYOFFICE 캐시 무효화용

    @Version
    private Integer version = 1;                // DB 동시성 제어용

    @Enumerated(EnumType.STRING)
    private DocumentStatus status = DocumentStatus.PENDING;

    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;            // Soft Delete용

    // fileType, documentType, fileSize, storagePath, timestamps...

    /** 편집 종료(status=2) 후 버전 증가 */
    public void incrementEditorVersion() {
        this.editorVersion++;
    }

    /** Soft Delete */
    public void softDelete() {
        this.status = DocumentStatus.DELETED;
        this.deletedAt = LocalDateTime.now();
    }
}

// DocumentStatus.java
public enum DocumentStatus {
    PENDING,    // 업로드 처리 중
    ACTIVE,     // 정상 사용 가능
    DELETED     // 삭제됨 (soft delete)
}
```

> **⚠️ version vs editorVersion**
> 
> | 필드 | 용도 | 증가 시점 | 관리 주체 |
> | --- | --- | --- | --- |
> | `version` | JPA Optimistic Locking (동시 수정 충돌 방지) | 엔티티 UPDATE마다 자동 | JPA |
> | `editorVersion` | ONLYOFFICE document.key 생성 (캐시 무효화) | SAVE 콜백(status=2)에서만 | 우리 코드 |
> 
> - `version`: 두 사용자가 동시에 같은 엔티티를 수정하면 나중 저장이 실패 → 데이터 정합성 보장
> - `editorVersion`: ONLYOFFICE가 캐시된 문서 대신 새 버전을 불러오도록 key 변경

#### DocumentRepository.java (핵심 메서드만)

```java
public interface DocumentRepository extends JpaRepository<Document, Long> {

    // fileKey로 조회 - Soft Delete 필터링
    Optional<Document> findByFileKeyAndDeletedAtIsNull(String fileKey);

    // 활성 문서 목록 조회
    List<Document> findAllByStatusAndDeletedAtIsNull(DocumentStatus status);

    // 비관적 락 (동시성 제어) - Callback 처리용
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
    @Query("SELECT d FROM Document d WHERE d.fileKey = :fileKey AND d.deletedAt IS NULL")
    Optional<Document> findWithLockByFileKey(@Param("fileKey") String fileKey);
}
```

**⚠️ Soft Delete 패턴:**

- `findByFileKeyAndDeletedAtIsNull`: 삭제되지 않은 문서만 조회
- 모든 조회 메서드에 `AndDeletedAtIsNull` 접미사 또는 `WHERE deletedAt IS NULL` 조건 추가
- 실제 삭제 대신 `softDelete()` 메서드로 `deleted_at` 타임스탬프 설정

> 💡 **참고**: `Claude Code` 에게 Soft Delete로 해줘! 했더니 이렇게 만들었다. 현재 방식은 문서 조회 시 직접 모든 쿼리에 조건(`~AndDeletedAtIsNull`)을 추가해야하는데, 추후 Hibernate 7로 마이그레이션 하면서 리팩토링 예정이니 불편함을 참자.

#### 왜 비관적 락을 사용했을까?

ONLYOFFICE Callback은 **우리 애플리케이션이 아닌 외부 시스템(ONLYOFFICE Document Server)** 에서 비동기로 전달된다.  
따라서 호출 시점, 호출 횟수, 재시도 여부를 우리 쪽에서 정확히 통제할 수 없다.

이러한 환경에서 동일한 `fileKey` 에 대한 Callback이 네트워크 지연이나 재시도로 중복되거나 거의 동시에 도착할 수 있다.

이 데모에서는 FORCESAVE를 비활성화하고, 편집 종료 시점(SAVE)에서만 `editorVersion` 을 증가시키므로 **상태 변경은 드물다**.

그럼에도 비관적 락을 선택한 이유는 **충돌 시 복구가 어렵기 때문** 이다.  
콜백이 드물기 때문에 비관적 락의 성능 오버헤드는 무시할 수준이다.  
따라서 재시도나 보정 로직을 설계하기보다, Callback 처리 구간을 비관적 락으로 직렬화(순차 실행으로 강제)해 외부 호출의 불확실성을 DB 레벨에서 흡수하는 편이 더 단순하고 명확하다고 판단했다.

---

## Part 3: Service 계층

#### DocumentService.java

```java
@Service
@RequiredArgsConstructor
public class DocumentService {

    private final DocumentRepository documentRepository;

    /** editorKey 생성 */
    public String getEditorKey(String fileKey) {
        Document doc = documentRepository.findByFileKeyAndDeletedAtIsNull(fileKey)
            .orElseThrow(() -> new DocumentNotFoundException(fileKey));
        return KeyUtils.generateEditorKey(doc.getFileKey(), doc.getEditorVersion());
    }

    /** 편집 종료(status=2) 후 버전 증가 - 비관적 락 사용 */
    public void incrementEditorVersion(String fileKey) {
        Document doc = documentRepository.findWithLockByFileKey(fileKey)
            .orElseThrow(() -> new DocumentNotFoundException(fileKey));
        doc.incrementEditorVersion();
        documentRepository.save(doc);
    }

    /** ONLYOFFICE에서 편집된 파일 다운로드 후 저장 */
    public void saveDocumentFromUrl(String downloadUrl, String fileKey) {
        Document doc = findByFileKey(fileKey).orElseThrow();
        try (InputStream in = URI.create(downloadUrl).toURL().openStream()) {
            Files.copy(in, Path.of(doc.getStoragePath()), REPLACE_EXISTING);
        } catch (Exception e) {
            throw new RuntimeException("Failed to save document", e);
        }
    }
}
```

> **💡 참고:** 역시 추후 백앤드 고도화 편에서 리팩토링 예정

---

## Part 4: Controller 계층

#### API 엔드포인트 변경

| 구분 | Before (fileName) | After (fileKey) |
| --- | --- | --- |
| Config 요청 | `GET /api/config?fileName=..` | `GET /api/documents/{fileKey}/config` |
| 파일 다운로드 | `GET /files/{fileName}` | `GET /files/{fileKey}` |
| Callback | `POST /callback?fileName={fileName}` | `POST /callback?fileKey={fileKey}` |

#### EditorController.java

```java
@GetMapping("/{fileKey}/config")
public Map<String, Object> getEditorConfig(@PathVariable String fileKey) {
    Document doc = documentService.findByFileKey(fileKey).orElseThrow();
    String editorKey = documentService.getEditorKey(fileKey);

    // ONLYOFFICE Config 구성
    Map<String, Object> document = Map.of(
        "title", doc.getFileName(),              // 사용자에게 표시
        "url", baseUrl + "/files/" + fileKey,    // 파일 다운로드 URL
        "key", editorKey                         // ⭐ fileKey_v{version}
    );

    Map<String, Object> editorConfig = Map.of(
        "callbackUrl", baseUrl + "/callback?fileKey=" + fileKey
    );

    // JWT와 함께 리턴
    return Map.of("config", config, "token", jwtManager.createToken(config));
}
```

#### CallbackController.java (Status별 처리)

```java
@PostMapping("/callback")  // POST /callback?fileKey={fileKey}
public Map<String, Object> callback(@RequestParam("fileKey") String fileKey,
                                    @RequestBody Map<String, Object> data) {
    int status = (int) data.get("status");
    String url = (String) data.get("url");

    switch (status) {
        case 2 -> {  // 편집 종료 & 저장
            documentService.saveDocumentFromUrl(url, fileKey);
            documentService.incrementEditorVersion(fileKey);  // ⭐ 버전 증가
        }
        case 6 -> {  // Force Save (co-editing 유지)
            documentService.saveDocumentFromUrl(url, fileKey);
            // editorVersion 유지 → key 변경 없음 → 세션 유지
        }
    }
    return Map.of("error", 0);
}
```

> 💡 **참고**: 현재 Controller에서 JWT와 Config를 직접 구성하고 각종 하드코딩된 로직이 들어가있다. 바로 다음 편에서 **ONLYOFFICE Java SDK** 를 도입하면 이 부분이 더 깔끔해진다.

---

## 정리

1. **document.key 스펙 이해**: 편집 세션(editorKey) vs 파일 영구 ID(fileKey)
2. **SAVE vs Force Save 구분**: SAVE 콜백에서만 버전 증가, FORCESAVE 시 co-editing 세션 유지
3. **DB 기반 메타데이터 관리**: PostgreSQL + JPA로 문서 정보 영구 저장

---

### 비교표

| 항목 | 2편 | 3편 |
| --- | --- | --- |
| **식별자** | `fileName` (중복 가능) | `fileKey` (UUID, 고유) |
| **API 경로** | `/api/config?fileName=..` | `/api/documents/{fileKey}/config` |
| **editorKey** | `fileName + lastModified` | `fileKey + "_v" + editorVersion` |
| **버전 관리** | 파일시스템 의존 | DB 메타데이터로 통합 관리 |
| **SAVE/FORCESAVE** | 구분 안 함 | save시에만 editorVersion++ |

---

## 4편 예고

#### 현재 한계

1. **파일 저장소**: 로컬 파일 시스템 사용
2. **분산 트랜잭션**: DB + Storage 간 정합성 미보장
3. **ONLYOFFICE 관련**: Config 구성 시 하드코딩된 key, JWT 관련 수동 처리 등

#### 4편에서 적용할 것

- **ONLYOFFICE Java SDK**: Config 생성, JWT 관련 고도화
- **MinIO 적용**: S3 호환 Object Storage 연동
- **Saga 패턴**: DB + MinIO 간 분산 트랜잭션 정합성 보장

---

## 참고 자료

> **ONLYOFFICE**: [공식 문서](https://api.onlyoffice.com/docs/docs-api/get-started/basic-concepts/)
> 
> **GitHub**: [onlyoffice-demo](https://github.com/taez224/onlyoffice-demo)
