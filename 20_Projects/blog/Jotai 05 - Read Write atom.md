---
title: Jotai Tutorial - Read Write atom
created: 2023-03-26
published: 2023-03-26
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-Tutorial-Read-Write-atom
series: Jotai tutorial
series_order: 5
summary: 읽기와 쓰기를 함께 정의하는 Read Write atom으로 상태 변경 로직을 구성하는 방법을 다룬다.
related:
  - "[[Jotai 04 - Write Only atom]]"
  - "[[Jotai 06 - atom 구조화]]"
---

# Jotai Tutorial - Read Write atom

## 들어가며

이번 포스트는 [지난 포스트](https://velog.io/@taez224/Jotai-Tutorial-Write-Only-atom-Read-Write-atom) 에서 이어지는 글입니다.

## 지난 포스트 복습

```typescript
// Primitive atom
const dotsAtom = atom([]);
const isDrawingAtom = atom(false);

// Write only atom
const handleMouseDownAtom = atom(
    null,
      (get, set) => set(isDrawingAtom, true)
);

const handleMouseUpAtom = atom(
      null,
      (get, set) => set(isDrawingAtom, false)
);

const handleMouseMoveAtom = atom(
    null,
      (get, set, update: Point) => {
      if(get(isDrawingAtom)) {
          set(dotsAtom, (prev) => [...prev, update]);
      }
    }
)
```
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

![](https://velog.velcdn.com/images/taez224/post/6f2b1d7f-298b-4d92-b75b-74e338bc7ac1/image.gif)

## Read Write atom

이전 포스트까지 잘 따라오셨다면 이번 포스트는 쉬어가는 시간이다.  
Read only atom과 Write onle atom을 합쳐놓은 것이 바로 Read Write atom이다.

Read Write atom의 기본 형태는 다음과 같다.

```typescript
const priceAtom = atom(10)
const readWriteAtom = atom(
      (get) => get(priceAtom) * 2,
      (get, set, newPrice: number) => {
        set(priceAtom, newPrice / 2)
     }
)
```

atom()의 첫 번째 파라미터로 get을 argument로 가지는 read function을 넘기고  
두 번째 파라미터로 get, set, update 를 argument로 가지는 write function을 넘기면 된다.

위의 readWriteAtom은 priceAtom \* 2에 해당하는 값을 가지고 있고  
newPrice를 set 할 시 newPrice/2 에 해당하는 값을 priceAtom에 set 한다.

사실 여기서 설명은 끝이지만 뭔가 심심하니 이전 포스트에서 만든 Write only atom들 중 하나를 Read Write atom으로 바꿔보자.

### 만들기

```typescript
// Write Only atom
const handleMouseMoveAtom = atom(
    null,
      (get, set, update: Point) => {
      if(get(isDrawingAtom)) {
          set(dotsAtom, (prev) => [...prev, update]);
      }
    }
)
```

위의 handleMouseMoveAtom에 read function을 추가해주면 Read Write atom이 된다.  
대충 현재 찍혀있는 dot 들의 개수를 가져오는 함수를 넣어보자.

```typescript
// Read Write atom
const handleMouseMoveAtom = atom(
    (get) => get(dotsAtom).length,
      (get, set, update: Point) => {
      if(get(isDrawingAtom)) {
          set(dotsAtom, (prev) => [...prev, update]);
      }
    }
)
```

그리고 SvgRoot를 다음과 같이 바꿔주면..

```tsx
const SvgRoot = () => {
  const [, handleMouseUp] = useAtom(handleMouseUpAtom);
  const [, handleMouseDown] = useAtom(handleMouseDownAtom);
  // Read Write Atom 사용하기
  const [dotsCount, handleMouseMove] = useAtom(handleMouseMoveAtom);
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
      <text x="3" y="12" font-size="12px">
        dots: {dotsCount}
      </text>
      <SvgDots />
    </svg>
  );
};
```

![](https://velog.velcdn.com/images/taez224/post/69565d9e-c501-40d9-a401-32139d2d0eaa/image.gif)

## 정리

```typescript
const primitiveAtom = atom(initialValue);
const derivedReadOnlyAtom = atom(readFunction);
const derivedWriteOnlyAtom = atom(null, writeFunction);
const derivedReadWriteAtom = atom(readFunction, writeFunction);

const [value, setValue] = useAtom(primitiveAtom);
const [readValue] = useAtom(derivedReadOnlyAtom);
const [,updateValue] = useAtom(derivedWriteOnlyAtom);
const [readVal, updateVal] = useAtom(derivedReadWriteAtom);
```

## 참조

[https://jotai-tutorial.netlify.app/quick-start/read-write-atoms](https://jotai-tutorial.netlify.app/quick-start/read-write-atoms)  
[https://egghead.io/lessons/react-prevent-rerenders-and-add-functionality-with-jotai-write-only-atoms](https://egghead.io/lessons/react-prevent-rerenders-and-add-functionality-with-jotai-write-only-atoms)

## 연관된 노트

- [[Jotai 04 - Write Only atom]] - 이전 글
- [[Jotai 06 - atom 구조화]] - 다음 글
