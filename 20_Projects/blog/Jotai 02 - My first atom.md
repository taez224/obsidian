---
title: Jotai Tutorial - My first atom
created: 2023-03-05
published: 2023-03-05
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-Tutorial-My-first-atom
series: Jotai tutorial
series_order: 2
summary: Primitive atom을 만들고 읽고 쓰는 Jotai의 가장 기본적인 상태 관리 방식을 설명한다.
related:
  - "[[Jotai 01 - Tutorial의 Tutorial]]"
  - "[[Jotai 03 - Derived atom Read Only]]"
---

# Jotai Tutorial - My first atom

## 들어가며

다음 내용은 [jotai-tutorial](https://jotai-tutorial.netlify.app/quick-start/intro) 을 기반으로 하고 있습니다.

## 1\. atom 만들기

Jotai에서의 atom은 작고 독립적인 상태의 조각이며 이상적으로 하나의 atom에는 매우 작은 하나의 데이터가 포함되어야 한다.

그럼 드디어 우리의 첫 번째 atom을 만들어 보자.

```javascript
// atom 만들기
import { atom } from 'jotai';
const countAtom = atom(0);
```

축하한다! 당신은 jotai의 세계에 훌륭하게 입성했다.

### Primitive atom

jotai에서는 크게 atom을 2 종류로 분류할 수 있는데 그 중 하나가 방금 우리가 만든 primitive atom이다.  
atom 함수에 초기값을 지정해서 넣어주면 끝이다.  
primitive atom은 boolean, number, string, object, array, set, map 등등의 값을 가질 수 있다.

```javascript
// 여러가지 atom들
const friendAtom = atom({ name: "John", online: false });
const citiesAtom = atom([ "Seoul", "Busan", "Jeju" ]);
const nestedObjAtom = atom({ friend1: { name: "Jane", age: 18 } });
```

위의 countAtom은 0을 초기값으로 가지는 atom인 것이다.

## 2\. atom 사용하기

atom을 사용하는 방법은 React의 useState와 매우 유사하다. 다른 점이라면 지역적이 아니라 **전역적으로 접근 가능(globally accessible)** 하다는 것!

```javascript
// atom 사용하기
const [count, setCount] = useAtom(countAtom);
```

useAtom(atom)은 **atom의 value** 와 **atom의 value를 set 할 수 있는 함수** 를 배열의 형태로 return 한다.

그럼 간단한 Counter 컴포넌트를 만들어보자.

```javascript
export default function Page() {
  const [count, setCount] = useAtom(countAtom);
  const onClick = () => setCount(prev => prev + 1);
  return (
    <div>
      <h1>{count}</h1>
      <button onClick={onClick}>Click</button>
    </div>
  )
}
```

![jotai-counter](https://velog.velcdn.com/images/taez224/post/7f6a04e1-c575-402d-ac1c-b13e8905df44/image.gif)

## 정리

Jotai를 사용하는 가장 큰 이유 중 하나는 전역 상태 관리를 쉽게 할 수 있다는 점이다.  
React의 useState와 유사한 방식으로 사용할 수 있어 React에 익숙하다면 쉽게 jotai를 사용할 수 있다.

## 연관된 노트

- [[Jotai 01 - Tutorial의 Tutorial]] - 이전 글
- [[Jotai 03 - Derived atom Read Only]] - 다음 글
