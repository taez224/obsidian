---
summary: ZIP 엔트리 크기를 업로드 전에 알아야 할 때 순차 스트림과 파일 기반 접근을 구분한다.
created: 2026-08-25
slug: zip-stream-unknown-size
tags:
  - 개발/Java
---

# 스트림 ZIP이 돌려주는 엔트리 크기 -1

외부 서비스가 여러 파일을 ZIP으로 묶어 스트리밍으로 반환한다. 이것을 받아 엔트리별로 오브젝트 스토리지에 올리려는데 업로드 API가 `Content-Length`를 요구했다.

`ZipInputStream`으로 열어 [`entry.getSize()`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipEntry.html#getSize())를 부르면 -1이 나온다. 결국 엔트리를 `byte[]`로 전부 읽어 길이를 재고 올리게 된다. 메모리를 아끼려고 응답을 임시 파일로 내려놓았는데 업로드 직전에 도로 메모리로 올라가는 셈이다. 작은 파일로 테스트하면 이 문제가 드러나지 않는다.

## local header와 central directory

[`ZipInputStream`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipInputStream.html)은 각 엔트리의 local file header만 읽는다. 그런데 ZIP을 순차 스트림으로 쓰는 생성기는 압축 결과의 크기를 미리 알 수 없다. 그래서 [엔트리를 기록할 때](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipOutputStream.html#putNextEntry(java.util.zip.ZipEntry)) local header의 크기와 CRC를 0으로 두고 general purpose bit 3을 세운 뒤, 실제 값을 데이터 뒤의 data descriptor에 적는다.

엔트리의 메타데이터를 모아 둔 곳은 파일 끝의 central directory인데, `ZipInputStream`은 이 목록을 읽지 않는다. 그래서 local header에 크기가 없는 엔트리는 읽기 시작하는 시점에 `getSize()`가 -1일 수 있고, 데이터 뒤의 descriptor를 처리한 뒤에야 크기를 알게 될 수 있다.

ZIP을 순차적으로 읽는 것 자체는 가능하다. 다만 엔트리를 읽기 전에 크기를 요구하는 업로드 API와는 맞지 않을 수 있다. 크기를 미리 읽을 수 있는 파일 기반 접근이나 별도의 크기 확인 단계가 필요하다.

## 파일로 내렸다면 파일로 읽는다

이미 파일로 내려놓았다면 `ZipFile`이나 `FileSystems.newFileSystem(zipPath)`를 쓴다. 이쪽은 central directory를 읽으므로 `getSize()`가 정확하고 `Content-Length`를 그대로 채울 수 있다. 엔트리 목록을 미리 알기 때문에 병렬 업로드도 가능해진다. 엔트리 크기를 미리 알아야 하는 이 상황에서는, 파일로 내려놓은 뒤에도 `ZipInputStream`을 쓸 이점이 작다.

임시 파일은 보관되는 동안 업로드 실패를 다시 시도할 수 있는 근거가 된다. 재시도 범위를 파일 수명 안에 두고, 최종 성공이나 오류나 취소 뒤에는 정리한다. `Flux<DataBuffer>`를 임시 파일로 기록한다면 [[코드마다 다른 DataBuffer release|파일 기록 단계의 버퍼 해제 책임]]도 함께 확인한다.

파일로 내리지 않고 순수 스트리밍으로 가야 한다면 컨테이너를 바꾸는 방법이 있다. `multipart/mixed`처럼 경계가 순차적으로 나오는 형식이면 목록을 미리 몰라도 도착하는 대로 흘려보낼 수 있다.

압축 방식도 함께 볼 만하다. 이미 압축된 데이터는 재압축 이득이 작을 수 있으므로 파일별 크기와 CPU 비용을 비교한다. 묶는 것이 목적이라면 `STORED`도 후보인데, Java `ZipOutputStream`으로 STORED 엔트리를 쓸 때는 크기와 CRC를 미리 준비해야 한다.
