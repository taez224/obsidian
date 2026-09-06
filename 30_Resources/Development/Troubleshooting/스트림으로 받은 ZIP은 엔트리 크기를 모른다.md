---
summary: ZIP 엔트리 크기를 업로드 전에 알아야 할 때 순차 스트림과 파일 기반 접근을 구분한다.
created: 2026-08-25
tags:
  - 개발/Java
---

> [!bug] 문제
> 외부 서비스가 여러 파일을 ZIP으로 묶어 스트리밍으로 반환한다. 받아서 엔트리별로 오브젝트 스토리지에 올리려는데 업로드 API가 `Content-Length`를 요구한다.
>
> `ZipInputStream`으로 열어 `entry.getSize()`를 부르면 **-1**이 나온다. 결국 엔트리를 `byte[]`로 다 읽어 길이를 재고 올린다. 메모리를 아끼려고 응답을 임시 파일로 내렸는데, 업로드 직전에 도로 메모리로 올라간다.
>
> 작은 파일로 테스트하면 안 드러난다.

---

> [!question] 원인
> `ZipInputStream`은 각 엔트리의 **local file header**만 본다. 그런데 ZIP을 순차 스트림으로 쓰는 생성기는 압축 결과 크기를 미리 알 수 없다. 그래서 local header의 크기·CRC를 0으로 두고 general purpose bit 3을 세운 뒤, 실제 값을 데이터 뒤의 **data descriptor**에 적는다.
>
> 엔트리의 메타데이터를 모아 둔 곳은 **파일 끝의 central directory**다. `ZipInputStream`은 이 목록을 읽지 않는다. local header에 크기가 없는 엔트리는 읽기 시작할 때 `getSize()`가 -1일 수 있고, 데이터 뒤의 descriptor를 처리한 후에는 크기를 알게 될 수 있다.
>
> ZIP은 순차적으로 읽을 수 있다. 다만 **엔트리를 읽기 전에 크기를 요구하는 업로드 API와는 맞지 않을 수 있다.** 미리 크기를 읽을 수 있는 파일 기반 접근이나 별도의 크기 확인 단계가 필요하다.

---

> [!tip] 해결 방법
> - **이미 파일로 내렸다면 `ZipFile`이나 `FileSystems.newFileSystem(zipPath)`를 쓴다.** central directory를 읽으므로 `getSize()`가 정확하고, `Content-Length`를 그대로 채울 수 있다. 엔트리 목록을 미리 알기 때문에 **병렬 업로드**도 가능해진다. 엔트리 크기를 미리 알아야 하는 이 상황에서는 파일로 내려놓은 뒤에도 `ZipInputStream`을 쓸 이점이 작다
> - 임시 파일은 보관되는 동안 업로드 실패를 **다시 시도할 수 있는 근거**가 된다. 재시도 범위를 파일 수명 안에 두고, 최종 성공·오류·취소 뒤에는 정리한다. `Flux<DataBuffer>`를 임시 파일로 기록한다면 [[DataBuffer 해제 책임은 최종 소비자가 정한다|파일 기록 단계의 버퍼 해제 책임]]도 함께 확인한다
> - 파일로 내리지 않고 순수 스트리밍으로 가야 한다면 컨테이너를 바꾼다. `multipart/mixed`처럼 **경계가 순차적으로 나오는 형식**이면 목록을 미리 몰라도 도착하는 대로 흘려보낼 수 있다
> - 곁들여 — 이미 압축된 데이터는 재압축 이득이 작을 수 있으므로 파일별 크기와 CPU 비용을 비교한다. 묶는 목적이면 `STORED`도 후보지만, Java `ZipOutputStream`으로 STORED 엔트리를 쓸 때는 크기와 CRC를 미리 준비해야 한다


## 참고 자료

- [Java ZipInputStream](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipInputStream.html) - local header와 central directory를 읽는 방식의 차이
- [Java ZipEntry.getSize](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipEntry.html#getSize()) - 크기를 모르면 -1 반환
- [Java ZipOutputStream.putNextEntry](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipOutputStream.html#putNextEntry(java.util.zip.ZipEntry)) - 엔트리 기록 방식
