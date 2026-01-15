---
tags:
  - 개발/도구
  - blog
---


# [Mac] 유용한 터미널 툴 모음

저는 대체로 대체하는걸 좋아하는 사람입니다.

제가 `zsh`를 쓰므로 해당 기준으로 설명합니다.

---

## bat
> `cat` 대체

cat | bat |
---|---|
![](https://velog.velcdn.com/images/taez224/post/f5a56265-4fcd-4335-bfb9-3b6bf39c716c/image.png) | ![](https://velog.velcdn.com/images/taez224/post/ca79ead2-503d-4266-8327-62bb1e597317/image.png)



- **설치**: `brew install bat`
  아예 완전히 `cat`를 대체하고싶다면 `.zshrc`에 `alias cat="bat"` 를 박아버리자.

- **특징**: 위 이미지로 대체한다.
  `bat`는 여러 테마도 제공하므로 `bat --list-themes` 로 본인 취향의 테마를 찾아서 적용해보자 (위의 이미지는 기본 테마)


## lsd
> `ls` 대체

기존 | lsd 적용 후 |
---|---|
![ls](https://velog.velcdn.com/images/taez224/post/d7d0c24c-35a4-452a-9199-68efe044f970/image.png) | ![lsd](https://velog.velcdn.com/images/taez224/post/771b38c9-97c2-421b-9065-2b2eb8f349a1/image.png)



- **설치**: `brew install lsd`
  만약 icon이 깨진다면 [Nerd Fonts](https://www.nerdfonts.com) 를 설치하자
  필자는`alias` 로 박고 사용
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

- **특징**: `exa`나 `eza`도 유명하지만 `lsd`가 더 깔끔해보여서 사용

## fd
> `find` 대체

예시 | find  | fd |
---|---|---|
단어로 찾기 | ![](https://velog.velcdn.com/images/taez224/post/54c8e0a2-59d5-4997-a66c-7176e44b7ad8/image.png) | ![](https://velog.velcdn.com/images/taez224/post/65abc9df-74ff-4f18-8a3b-0f9d132287b4/image.png) |
확장자로 찾기 | ![](https://velog.velcdn.com/images/taez224/post/02d9c35f-40cb-455f-bcdc-32c2b386f39f/image.png) | ![](https://velog.velcdn.com/images/taez224/post/bcc8972d-5ac9-430e-9a85-7e0ef922b759/image.png)


- **설치**: `brew install fd`

- **특징**: `find`보다 명령어가 직관적이고 속도도 빠르고 이쁘게 나온다. 끝.




## ripgrep (rg)
> `grep` 대체

grep | ripgrep |
---|---|
![grep](https://velog.velcdn.com/images/taez224/post/2568443f-bd47-41b8-aa2e-4abcfb251031/image.png) | ![ripgrep](https://velog.velcdn.com/images/taez224/post/317d0f87-5fc8-4203-8f2a-d98dc063f7d5/image.png)

- **설치**: `brew install ripgrep`

- **특징**: `grep`보다 옵션도 직관적이고 속도도 더 빠르다. 별 설정 없이도 기본 출력 가독성 Good



## zoxide
> `cd` 대체
> ![](https://velog.velcdn.com/images/taez224/post/904c40de-04df-4044-8224-33be4ae7c142/image.gif)


- **설치**:
1. `brew install zoxide`
2. `.zshrc`에 아래 추가. 기본 명령어는 `z` 지만 완전 `cd`를 대체한다면 *alias* 적용
```bash
alias cd='z' # cd 대체
eval "$(zoxide init zsh)"
```
- **특징**: ~~위 이미지로 설명완료 로 넘어가려다가 설명 추가~~
	- 자주 이동하는 디렉토리를 기억한다. (`z`로 이동시 해당 디렉토리에 *point* 적립)
	- 그러면 추후 경로의 일부만 입력하면 가장 적합한(*point*가 높은) 디렉토리로 **점프**
	- *point* 기반으로 최근/자주 방문한 디렉토리가 우선권을 가진다.


---

## 😲 One More Thing


### fzf
> Fuzzy 검색 툴로 이미 너무 유명하고 수많은 활용법이 있지만
- `history | fzf` - `history` 에서 `fzf`를 통해 검색
  ![](https://velog.velcdn.com/images/taez224/post/af869476-68ec-446f-b715-b4a5aec5c59a/image.png)




- **설치**:
	1. `brew install fzf`
	2. `.zshrc`에 추가 - `eval "$(fzf --zsh)"`


- **특징**: 무궁무진하게 활용 가능. 예를 들어..

### zf (custom)
> 위에서 소개한 `zoxide`, `lsd`와 `fzf`의 조합으로 `ChatGPT`와 머리 맞대고 만든 커스텀 커맨드

1. **기본 컨셉**
	- `zoxide` → 자주 가는 디렉토리 기록/검색
	- `fzf` → 검색 UI
	- `lsd` → 디렉토리 내용 예쁘게 출력

2. **결합 아이디어**
	1. `zoxide`로 후보 디렉토리를 불러오고
	2. `fzf`로 선택 → `lsd`로 해당 디렉토리 미리보기
	3. 이동 및 `lsd`로 출력

3. **적용**
   `.zshrc`에 아래 함수 추가 - 커맨드 네임이라던지 중간 옵션값은 취향에 맞게 조절
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

> 결과
![](https://velog.velcdn.com/images/taez224/post/64c2d3ec-a1d8-4d46-88fe-a4fcc4ed5e26/image.gif)


---

- 링크 또는 참조:
	- https://gracefullight.dev/2019/05/27/install-lsd-on-mac/
	- https://elsainmac.tistory.com/896
    - [velog 링크](https://velog.io/@taez224/Mac-%EC%9C%A0%EC%9A%A9%ED%95%9C-%ED%84%B0%EB%AF%B8%EB%84%90-%ED%88%B4-%EB%AA%A8%EC%9D%8C)
