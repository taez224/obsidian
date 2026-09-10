---
created: 2026-01-15
slug: mac-terminal-tools
summary: macOS에서 자주 쓰는 터미널 명령어를 대체할 도구와 조합 방식을 정리한다.
tags:
  - 개발/도구
---


# [Mac] 유용한 터미널 툴 모음

자주 쓰는 명령어를 더 나은 도구로 바꿔 써 보자.

`zsh` 기준으로 설치와 설정을 적는다.

---

## bat
> `cat` 대체

cat | bat |
---|---|
![](https://velog.velcdn.com/images/taez224/post/f5a56265-4fcd-4335-bfb9-3b6bf39c716c/image.png) | ![](https://velog.velcdn.com/images/taez224/post/ca79ead2-503d-4266-8327-62bb1e597317/image.png)



- **설치**: `brew install bat`
  `cat`을 완전히 대체하려면 `.zshrc`에 `alias cat="bat"`를 지정한다.

- **특징**: 위 이미지로 대체한다.
  `bat`는 여러 테마도 제공하므로 `bat --list-themes`로 원하는 테마를 찾아 적용한다 (위 이미지는 기본 테마).


## lsd
> `ls` 대체

기존 | lsd 적용 후 |
---|---|
![ls](https://velog.velcdn.com/images/taez224/post/d7d0c24c-35a4-452a-9199-68efe044f970/image.png) | ![lsd](https://velog.velcdn.com/images/taez224/post/771b38c9-97c2-421b-9065-2b2eb8f349a1/image.png)



- **설치**: `brew install lsd`
  아이콘이 깨진다면 [Nerd Fonts](https://www.nerdfonts.com)를 설치한다.
  `alias`로 지정해 사용한다.
```bash
    # 기본 ls 대체 (숨김 파일 안 보임)
	alias ls='lsd --group-dirs first'

	# la: 숨김 파일 포함 + 간략 보기
	alias la='lsd -a --group-dirs first'

	# ll: 숨김 파일 포함 + 상세 보기
	alias ll='lsd -alh --group-dirs first'

	# lt: 트리 구조로 보기 (lt2: 2 depth)
	alias lt='lsd --tree --group-dirs first'
	alias lt2='lsd --tree --depth 2 --group-dirs first'
```

- **특징**: `exa`나 `eza`도 유명하지만 `lsd`가 더 깔끔해 보여 사용한다.

## fd
> `find` 대체

예시 | find  | fd |
---|---|---|
단어로 찾기 | ![](https://velog.velcdn.com/images/taez224/post/54c8e0a2-59d5-4997-a66c-7176e44b7ad8/image.png) | ![](https://velog.velcdn.com/images/taez224/post/65abc9df-74ff-4f18-8a3b-0f9d132287b4/image.png) |
확장자로 찾기 | ![](https://velog.velcdn.com/images/taez224/post/02d9c35f-40cb-455f-bcdc-32c2b386f39f/image.png) | ![](https://velog.velcdn.com/images/taez224/post/bcc8972d-5ac9-430e-9a85-7e0ef922b759/image.png)


- **설치**: `brew install fd`

- **특징**: `find`보다 명령어가 직관적이고 빠르며 출력도 보기 좋다.




## ripgrep (rg)
> `grep` 대체

grep | ripgrep |
---|---|
![grep](https://velog.velcdn.com/images/taez224/post/2568443f-bd47-41b8-aa2e-4abcfb251031/image.png) | ![ripgrep](https://velog.velcdn.com/images/taez224/post/317d0f87-5fc8-4203-8f2a-d98dc063f7d5/image.png)

- **설치**: `brew install ripgrep`

- **특징**: `grep`보다 옵션이 직관적이고 빠르며, 별도 설정 없이도 기본 출력이 읽기 좋다.



## zoxide
> `cd` 대체
> ![](https://velog.velcdn.com/images/taez224/post/904c40de-04df-4044-8224-33be4ae7c142/image.gif)


- **설치**:
1. `brew install zoxide`
2. `.zshrc`에 아래를 추가한다. 기본 명령어는 `z`이며, `cd`를 완전히 대체하려면 별칭을 지정한다.
```bash
alias cd='z' # cd 대체
eval "$(zoxide init zsh)"
```
- **특징**: 자주 이동하는 디렉토리를 기억한다.
	- 자주 이동하는 디렉토리를 기억한다. (`z`로 이동시 해당 디렉토리에 *point* 적립)
	- 그러면 추후 경로의 일부만 입력하면 가장 적합한(*point*가 높은) 디렉토리로 **점프**
	- *point* 기반으로 최근/자주 방문한 디렉토리가 우선권을 가진다.


---

## 😲 One More Thing


### fzf
> Fuzzy 검색 도구다. 활용 범위가 넓지만, 여기서는 간단한 예만 든다.
- `history | fzf`: `history`에서 `fzf`로 검색
  ![](https://velog.velcdn.com/images/taez224/post/af869476-68ec-446f-b715-b4a5aec5c59a/image.png)




- **설치**:
	1. `brew install fzf`
	2. `.zshrc`에 `eval "$(fzf --zsh)"`를 추가한다.


- **특징**: 활용 범위가 넓다. 여기서는 한 가지 예만 든다.

### zf (custom)
> 앞서 소개한 `zoxide`, `lsd`, `fzf`를 조합해 만든 커스텀 명령어다.

1. **기본 개념**
	- `zoxide` → 자주 가는 디렉토리 기록/검색
	- `fzf` → 검색 UI
	- `lsd` → 디렉토리 내용 예쁘게 출력

2. **결합 아이디어**
	1. `zoxide`로 후보 디렉토리를 불러오고
	2. `fzf`로 선택 → `lsd`로 해당 디렉토리 미리보기
	3. 이동 및 `lsd`로 출력

3. **적용**
   `.zshrc`에 아래 함수를 추가한다. 명령어 이름과 옵션 값은 필요에 맞게 조정한다.
```bash
# zoxide + fzf + lsd 미리보기
zf() {
  local dir
  # zoxide query + fzf with lsd preview
  dir=$(zoxide query -l | fzf \
    --prompt="📂 Select directory: " \
    --height=60% \
    --reverse \
    --preview 'lsd --tree --depth 2 --group-dirs first --color=always --icon=always {}' \
    --preview-window=right:40%:wrap)

  # 선택 취소시 종료
  [[ -z "$dir" ]] && return

  # 이동 알림 및 이동
  echo "📁 Moving to: $dir"
  z "$dir" || return
  # 이동 후 lsd 출력
  lsd --group-dirs first
}
```

> 실행 결과
![](https://velog.velcdn.com/images/taez224/post/64c2d3ec-a1d8-4d46-88fe-a4fcc4ed5e26/image.gif)


---

- 링크 또는 참조:
	- https://gracefullight.dev/2019/05/27/install-lsd-on-mac/
	- https://elsainmac.tistory.com/896
    - [velog 링크](https://velog.io/@taez224/Mac-%EC%9C%A0%EC%9A%A9%ED%95%9C-%ED%84%B0%EB%AF%B8%EB%84%90-%ED%88%B4-%EB%AA%A8%EC%9D%8C)
