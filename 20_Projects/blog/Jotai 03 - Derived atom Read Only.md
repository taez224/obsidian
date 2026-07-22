---
title: Jotai Tutorial - Derived atom (Read Only atom)
created: 2023-03-05
published: 2023-03-05
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-Tutorial-Derived-atom-Read-Only-atom
series: Jotai tutorial
series_order: 3
summary: 기존 atom에서 값을 파생하는 Derived atom과 읽기 전용 atom의 동작 방식을 다룬다.
related:
  - "[[Jotai 02 - My first atom]]"
  - "[[Jotai 04 - Write Only atom]]"
---

# Jotai Tutorial - Derived atom (Read Only atom)

## 들어가며

다음 내용은 [jotai-tutorial(Read Only atoms)](https://jotai-tutorial.netlify.app/quick-start/readonly-atoms) 을 기반으로 하고 있습니다.

## 1\. Derived atom

[지난 포스트](https://velog.io/@taez224/Jotai-Tutorial-My-first-atom) 에서 atom에는 크게 2 종류가 있으며 그 중 하나가 **Primitive atom** 이라고 했다.  
다른 하나는 바로 **Derived atom** 으로 기존 atom에서 **파생** 된 atom이다.

Derived atom은 다시 다음과 같이 3 종류로 나뉠 수 있다.  
1\. Read Only atom  
2\. Write Only atom  
3\. Read Write atom

이번 글에서는 먼저 Read Only atom에 대해서 알아보자.

## 2\. Read Only atom

Read-only atom은 다른 atom(parent atom)의 값을 읽을 때 사용된다. 이름 그대로 read만 할 수 있으며 atom의 값을 직접 set하거나 변경할 수 없다. 즉, parent atom에 **의존적** 이다.

### 만들기

Derived atom을 만들기 위해선 atom()에 초기값이 아닌 **read function** 과 optional로 **write function** 을 넘겨주면 된다.

그럼, 직접 만들어 보자.

```javascript
// Read-only atom 만들기
const textAtom = atom('hello'); // primitive atom
const uppercaseAtom = atom(
  (get) => get(textAtom).toUpperCase()
); // derived atom (read-only atom)
```

textAtom은 hello 라는 문자열을 초기값으로 가지는 primitive atom이다.  
uppercaseAtom이 textAtom에서 파생 된 **Derived Atom** 이며 read function만 넘겨줬으니 **Read-only atom** 이 된다.

read function의 **get** 은 atom의 value를 읽으며 이는 **reactive** 하며 read dependencies는 **tracked** 된다. 즉, parent atom의 값이 바뀌면 derived atom도 update 된다.

우리가 만든 uppercaseAtom은 textAtom의 값에 toUpperCase()를 적용한 값을 담고 있는 atom이 되시겠다.

내친김에 하나 더 만들어보자.

```javascript
const textLenAtom = atom((get) => get(textAtom).length);
```

textLenAtom은 textAtom의 value의 길이를 값으로 가지는 read-only atom이다.

### 사용하기

사용 방법은 기존 atom과 같다. 단 Read-only atom이기 때문에 useAtom이 반환하는 배열의 2번째 값인 set function은 필요하지 않다.

```javascript
// Read-only atom 사용하기
const Uppercase = () => {
  const [uppercase] = useAtom(uppercaseAtom);
  return <div>Uppercase: {uppercase}</div>
}
```

마지막으로 역시 간단한 컴포넌트들을 만들어서 확인해보자

```javascript
import { atom, useAtom } from 'jotai';

// primitive atom 만들기
const textAtom = atom('hello');
// derived atom(Read-only) 만들기
const uppercaseAtom = atom((get) => get(textAtom).toUpperCase());
const textLenAtom = atom((get) => get(textAtom).length);;

// primitive atom 사용
const Input = () => {
  const [text, setText] = useAtom(textAtom);
  return <input value={text} onChange={(e) => setText(e.target.value)} />
}

// Read-only atom 사용
const CharCount = () => {
  const [len] = useAtom(textLenAtom);
  return <div>Length: {len}</div>
}

const Uppercase = () => {
  const [uppercase] = useAtom(uppercaseAtom);
  return <div>Uppercase: {uppercase}</div>
}

export default function Page() {
  return (
    <>
      <Input/>
      <CharCount/>
      <Uppercase/>
    </>
  )
}
```

![read-only atom](https://velog.velcdn.com/images/taez224/post/428e582c-9a28-4c37-9c15-3aa2092832c6/image.gif)

### 활용하기

```javascript
const friendsAtom = atom([ 
  { name: "John", online: true },
  { name: "David", online: false },
  { name: "Chloe", online: true } 
]);

const onlineFriendsAtom = atom(
  (get) => get(friendsAtom).filter((item) => item.online)
);
```

전체 friend의 배열을 담고있는 atom에서 online이 true인 friend만 filter한 배열을 값으로 가진 derived read only atom이다.

## 정리

```javascript
const primitiveAtom = atom(initialValue);
const derivedReadOnlyAtom = atom(readFunction);

const [value, setValue] = useAtom(primitiveAtom);
const [readValue] = useAtom(derivedReadOnlyAtom);
```

## 연관된 노트

- [[Jotai 02 - My first atom]] - 이전 글
- [[Jotai 04 - Write Only atom]] - 다음 글
