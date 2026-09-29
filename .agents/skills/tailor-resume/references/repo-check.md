# 사내 저장소로 사실 확인하기

원장에 없는 사실을 코드로 확인할 때의 절차다. 저장소 경로는 `QRA·Gallery 기술 경력 원장.md`에 있다. 그 경로의 최상위에는 `.git`이 없으므로, `git`은 확인할 파일이 속한 저장소 안에서 실행한다.

1. 읽기만 한다. checkout, pull, stash를 하지 않는다.
2. `git branch --show-current`로 작업 트리의 브랜치를 먼저 본다.
3. main의 내용은 `git grep <패턴> origin/main`이나 `git show origin/main:<경로>`로 읽는다.
4. 커밋이 main에 들어갔는지는 `git branch -a --contains <sha>`로 커밋마다 따로 확인한다. main에 없는 커밋은 main 반영으로 쓰지 않는다.
5. `origin/main`은 마지막 fetch 시점 기준이다.

확인한 사실은 SKILL.md 6절대로 원장에 기록한다. 코드로 확인한 사실은 파일과 커밋을 적는다.
