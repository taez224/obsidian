---
created: 2026-07-15
tags:
  - 개발/트러블슈팅
  - 개발/Java
---

> [!bug] 문제
> 멀티모듈 프로젝트에서 코드를 다른 모듈로 이관한 뒤 Spring 부트 기동 실패. 생성자의 특정 파라미터에서 같은 타입(`Executor`)의 빈 여러 개가 매칭된다는 모호성 오류.

---

> [!question] 원인
> Spring 6.x는 동일 타입 빈이 여러 개일 때 **파라미터 이름**으로 주입 대상을 구분하는데, 이는 컴파일 시 `-parameters` 플래그가 있어야 바이트코드에 보존된다. 이관한 모듈의 빌드 설정에 플래그가 없으면 파라미터명이 소실되어 "expected single matching bean but found N"으로 터진다. **코드만 옮기고 빌드 옵션을 안 옮긴 것**이 근본 원인.

---

> [!tip] 해결 방법
> ```gradle
> tasks.withType(JavaCompile).configureEach {
>     options.compilerArgs.add('-parameters')
> }
> ```
> 멀티모듈 이관 체크리스트에 "빌드 옵션(컴파일 플래그·어노테이션 프로세서)도 함께 이관"을 포함할 것.

---

> [!info] 참고 자료
> - 출처: 로컬 DevLog 2026-04-28 (git 미추적 원본)
> - 같은 계열: [[ApplicationContextException_REGISTER_BEAN]] - Spring 빈 등록 단계의 기동 실패 사례
