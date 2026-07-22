---
title: Jotai Tutorial - Write Only atom
created: 2023-03-07
published: 2023-03-07
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-Tutorial-Write-Only-atom
series: Jotai tutorial
series_order: 4
summary: 값을 구독하지 않고 다른 atom의 상태만 변경하는 Write Only atom의 사용법을 설명한다.
related:
  - "[[Jotai 03 - Derived atom Read Only]]"
  - "[[Jotai 05 - Read Write atom]]"
---

# Jotai Tutorial - Write Only atom

## 들어가며

이번 포스트는 [해당 링크](https://jotai-tutorial.netlify.app/quick-start/write-only-atoms) 를 바탕으로 작성되었습니다.

## 1\. Derived atom 복습

[지난 포스트](https://velog.io/@taez224/Jotai-Tutorial-Derived-atom-Read-Only-atom) 에서 다른 atom에서 파생 되는 atom의 종류 중 하나인 Read only atom에 대해서 알아보았다.  
atom 함수에 초기값이 아닌 get을 argument로 가지는 read function을 넘겨주면 get으로 다른 atom의 value를 읽는 Read only atom이 되며 parent atom이 update될 때 마다 derived atom에도 반영 됨을 확인했다.

이번 포스트에서는 Derived atom의 또다른 종류인 Write-only atom에 대해 알아보자.

## 2\. Write Only atom

Write-only atom은 이름 그대로 다른 atom의 값을 변경하는 atom이며 atom의 value는 가지고 있지 않는다. 이러한 제한은 해당 atom의 value를 subscribe할 필요가 없는 경우에 유용하며 re-rendering 문제를 피할 수 있다고 한다.

### 준비

이번에 만들 컴포넌트는 마우스 움직임에 따라 dot이 찍히는 SVG drawing component다. [해당 링크](https://egghead.io/lessons/react-derive-state-from-a-jotai-atom-in-react) 에서 코드 확인 및 테스트를 할 수 있다.

먼저 기본적인 primitive atom 부터 만들어 보자.

```typescript
type Point = [number, number];

const dotsAtom = atom<Point[]>([]);
```

dot의 위치를 나타내는 Point라는 type을 만들어 주고 dot의 위치들의 배열을 값으로 가지는 dotsAtom을 만들어 주었다.

```tsx
const SvgDots = () => {
    const [dots] = useAtom(dotsAtom);
      return (
      <g>
        {dots.map(([x, y], index) => (
          <circle cx={x} cy={y} r="2" fill="#aaa" key={index} />
        ))}
      </g>
  );
};
```
```tsx
const SvgRoot = () => {
    const [, setDots] = useAtom(dotsAtom);
      return (
      <svg
         width="100vw"
         height="100vh"
          viewBox="0 0 100vw 100vh"
        onMouseMove={(e) => {
          const p: Point = [e.clientX, e.clientY];
          setDots((prev) => [...prev, p]);
        }}
      >
        <rect width="100vw" height="100vh" fill="#eee" />
        <SvgDots />
      </svg>
  );
};
```

onMouseMove에서 setDots를 이용해 dotsAtom을 update하고 있다.  
이것을 Write-only atom으로 바꿔보자.

### Write atom 만들기

Write-only atom을 만들기 위해서는 atom의 첫 번째 인자로 null을 넘기고 두 번째 인자로 write function을 넘겨주면 된다.

```typescript
const handleMouseMoveAtom = atom(
    null,
      (get, set, update: Point) => {
      set(dotsAtom, (prev) => [...prev, update]);
    }
)
```

write function은 3개의 arguments를 갖는데 get함수와 set함수, 그리고 update 값이다.

get 함수는 Read only atom의 read function의 get과 마찬가지로 다른 atom의 value를 가져오는 함수이다.  
set 함수는 다른 atom의 값을 변경하는 함수이며 set(atom, value)의 형태로 사용한다.  
마지막 update는 atom을 update 하기 위해 받는 값이며  
위 handleMouseMoveAtom의 역할은 새로운 point를 받으면 기존 dotsAtom에 set 함수를 이용하여 해당 point를 추가한다.

그럼 SvgRoot에서 기존의 dotsAtom 자리에 새로 만든 handleMouseMoveAtom을 사용해보자.

```tsx
const SvgRoot = () => {
    // const [, setDots] = useAtom(dotsAtom);
      const [, handleMouseMove] = useAtom(handleMouseMoveAtom);
      return (
      <svg
        width="100vw"
          height="100vh"
          viewBox="0 0 100vw 100vh"
        onMouseMove={(e) => {
          // const p: Point = [e.clientX, e.clientY];
          // setDots((prev) => [...prev, p]);
          handleMouseMove([e.clientX, e.clientY]);
        }}
      >
        <rect width="100vw" height="100vh" fill="#eee" />
        <SvgDots />
      </svg>
  );
};
```

기존 onMouseMove prop의 setDots 내에서 이루어지던 로직이 handleMouseMoveAtom 내부로 옮겨진 것을 볼 수 있다.

![mouse-move](https://velog.velcdn.com/images/taez224/post/c47c6edb-675a-423d-b47a-ae5da56a2a4c/image.gif)

여기까지 진행이 됐다면 마우스의 움직임에 따라 canvas에 dot들이 찍힐텐데 마우스가 클릭되어 있을 때만 dot을 찍고싶다면 어떻게 해야할까?

먼저 새로운 atom 하나를 추가해보자.

```typescript
const isDrawingAtom = atom(false);
```

boolean atom으로 drawing 중인지 아닌지를 정의한다. 우리는 마우스가 클릭되어 있는 상태 여부에 따르기로 했으므로 다음과 같이 Write-only atom을 만들어 준다.

```typescript
const handleMouseDownAtom = atom(
    null,
      (get, set) => set(isDrawingAtom, true)
);

const handleMouseUpAtom = atom(
      null,
      (get, set) => set(isDrawingAtom, false)
);
```

그리고 기존 handleMouseMoveAtom을 다음과 같이 수정한다.

```typescript
const handleMouseMoveAtom = atom(
    null,
      (get, set, update: Point) => {
      if(get(isDrawingAtom)) {
          set(dotsAtom, (prev) => [...prev, update]);
      }
    }
)
```

get 함수로 isDrawingAtom의 값을 읽어서 true일 때만 새로운 dot을 dotsAtom의 값에 추가한다.

그럼 SvgRoot에 해당 atom을 추가하자.

```tsx
const SvgRoot = () => {
      const [, handleMouseMove] = useAtom(handleMouseMoveAtom);
      const [, handleMouseDown] = useAtom(handleMouseDownAtom);
      const [, handleMouseUp] = useAtom(handleMouseUpAtom);
      return (
      <svg
        width="100vw"
          height="100vh"
          viewBox="0 0 100vw 100vh"
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseMove={(e) => {
          handleMouseMove([e.clientX, e.clientY]);
        }}
      >
        <rect width="100vw" height="100vh" fill="#eee" />
        <SvgDots />
      </svg>
  );
};
```

![mouse-click](https://velog.velcdn.com/images/taez224/post/6f2b1d7f-298b-4d92-b75b-74e338bc7ac1/image.gif)  
이제 마우스가 클릭 상태일 때만 dot이 찍히는 것을 볼 수 있다.

## 정리

```typescript
const primitiveAtom = atom(initialValue);
const derivedReadOnlyAtom = atom(readFunction);
const derivedWriteOnlyAtom = atom(null, writeFunction);

const [value, setValue] = useAtom(primitiveAtom);
const [readValue] = useAtom(derivedReadOnlyAtom);
const [,updateValue] = useAtom(derivedWriteOnlyAtom);
```

## 참조

[https://jotai-tutorial.netlify.app/quick-start/writeonly-atoms](https://jotai-tutorial.netlify.app/quick-start/write-only-atoms)  
[https://egghead.io/lessons/react-prevent-rerenders-and-add-functionality-with-jotai-write-only-atoms](https://egghead.io/lessons/react-prevent-rerenders-and-add-functionality-with-jotai-write-only-atoms)

## 연관된 노트

- [[Jotai 03 - Derived atom Read Only]] - 이전 글
- [[Jotai 05 - Read Write atom]] - 다음 글
