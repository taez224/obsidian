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

[![profile](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII=)](https://velog.io/@taez224/posts)

흔하지 않은 개발자

## 연관된 노트

- [[Jotai 04 - Write Only atom]] - 이전 글
- [[Jotai 06 - atom 구조화]] - 다음 글
