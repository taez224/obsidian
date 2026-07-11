---
title: Jotai Tutorial의 Tutorial
created: 2023-03-05
published: 2023-03-05
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-Tutorial%EC%9D%98-Tutorial
series: Jotai tutorial
series_order: 1
summary: Jotai의 원자적 상태 관리 접근법과 공식 튜토리얼을 따라갈 연재의 범위를 소개한다.
related:
  - "[[Jotai 02 - My first atom]]"
---

# Jotai Tutorial의 Tutorial

## Jotai란?

> Primitive and flexible state management for React

[공식 홈페이지](https://jotai.org/) 에서 소개하기를 **리액트를 위한 간단하면서 유연한 상태 관리 라이브러리** 라고 한다.

또한 Recoil에서 영감을 받은 상향식 **원자적 접근법(atomic approach)** 을 적용했다고 하는데  
atom을 결합하여 state를 구축하고, atom의 종속성에 따른 자동 렌더링 최적화가 적용이 되며 이에 따라 React context의 추가 리렌더링 문제가 해결되며 memoization이 필요하지 않다고 한다.

Recoil을 사용해본 적이 없어서 위 문장이 아직 무슨 말인지 정확히 모르겠지만 대강 React context API의 단점을 보완했으며 state를 다루는데에 atom이라는 것을 사용하면서 보다 직관적으로 관리할 수 있을 것이라고 이해했다.

## Jotai Tutorial

글로 보는 것도 좋지만 코드로 보는게 조금 더 빨리 이해가 되는 사람들을 위해(=필자) 찾아보다가 Jotai 라이브러리의 사용 방법을 코드로 자세하게 설명하고 있는 [jotai-tutorial github](https://github.com/jotaijs/jotai-tutorial) 을 발견해서 하나하나씩 알아보려 한다.

해당 github의 내용은 다음 [링크](https://jotai-tutorial.netlify.app/) 에서 쉽게 확인할 수 있으며 글을 작성하는 현재 jotai v2.0.2 기준으로 설명하고 있다.

## 설치

만약 jotai 설치부터 진행하고 싶다면 먼저 인스톨하자.

```c
# npm
npm i jotai

# yarn
yarn add jotai

# pnpm
pnpm install jotai
```

[![profile](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII=)](https://velog.io/@taez224/posts)

흔하지 않은 개발자

다음 포스트

## 연관된 노트

- [[Jotai 02 - My first atom]] - 다음 글
