---
title: Jotai - atom 구조화
created: 2023-03-26
published: 2023-03-26
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-atom-%EA%B5%AC%EC%A1%B0%ED%99%94
series: Jotai tutorial
series_order: 6
summary: 작은 atom을 역할별로 나누고 조합해 Jotai 상태와 기능을 구조화하는 방법을 정리한다.
related:
  - "[[Jotai 05 - Read Write atom]]"
  - "[[Jotai 07 - atoms in atom]]"
---

# Jotai - atom 구조화

## 들어가며

이번 포스트는 jotai atom의 의미와 derived atom들의 종류와 기본적인 사용법을 알고있다는 가정 하에 작성 된 글입니다. 위 내용에 대해 익숙하지 않으시다면 [이전 Jotai tutorial 시리즈](https://velog.io/@taez224/series/Jotai-tutorial) 를 먼저 읽고 오시는 것을 추천드립니다.

이번 포스트의 내용은 jotai를 개발한 Daishi Kato의 [egghead lesson](https://egghead.io/lessons/react-structure-jotai-atoms-and-add-functionality-to-a-react-app) 을 바탕으로 하고 있으며 전체 코드는 [code sandbox](https://codesandbox.io/embed/jotai-tutorial-04-6fkir) 에서 확인하실 수 있습니다.

## 튜토리얼은 끝났다

[지난 포스트](https://velog.io/@taez224/Jotai-Tutorial-Read-Write-atom) 로 jotai의 기초는 끝났다고 볼 수 있겠다. 이번 포스트 부터는 보다 실전적이거나 테크닉이 들어간 jotai 활용법을 알아 보자.

## 튜토리얼 요약

튜토리얼 시리즈에서 우리는 SVG 캔버스에 dot을 찍는 app을 하나의 파일에 모두 작성했다.  
이제 튜토리얼을 졸업했으니 이 코드들을 나누어서 구조화 해보자.

## atom 구조화란?

![](https://velog.velcdn.com/images/taez224/post/f87cc0aa-3e71-41a0-ac05-d5e058ffa011/image.png)  
요즘 핫한 Chat GPT에게 물어봤는데 생각보다 더 설명을 그럴듯하게 해주었다.  
...  
...  
뭔가 더 적으려다 GPT님 말을 반복하는 것 같아서 그냥 다음으로 넘어가겠다....

구조화에 여러가지 방법이 있지만 여기서는 기능 별 컴포넌트로 나누고 연관된 컴포넌트 파일에 atom을 정의하는 방식을 선택하겠다. 이렇게 하면 다른 컴포넌트에서 쓰이는 atom만 export할 수 있게 된다.

### 타입 정의

먼저 타입을 정의하는 types.ts를 만들자.

```typescript
// types.ts
export type Point = readonly [number, number];
```

Point는 읽기 전용인 \[number, number\] tuple type이다.

### SvgDots.tsx

```tsx
// SvgDots.tsx
import { atom, useAtom } from "jotai";

import { Point } from "./types";

const dotsAtom = atom<readonly Point[]>([]);

export const addDotAtom = atom(
  null,
  (_get, set, update: Point) => {
    set(dotsAtom, (prev) => [...prev, update]);
  }
);

export const SvgDots = () => {
  const [dots] = useAtom(dotsAtom);
  return (
    <g>
      {dots.map(([x, y]) => (
        <circle cx={x} cy={y} r="2" fill="#aaa" />
      ))}
    </g>
  );
};
```

튜토리얼 시리즈에서 만든 점을 찍는 SvgDots를 SvgDots.tsx로 분리시켰다.  
dotsAtom은 SvgDots 내부에서만 쓰이므로 export하지 않았고 dotsAtom에서 파생된 addDotAtom은 export 시켜줬다.

### SvgRoot.tsx

```tsx
// SvgRoot.tsx
import { atom, useAtom } from "jotai";

import { Point } from "./types";
import { addDotAtom, SvgDots } from "./SvgDots";

const drawingAtom = atom(false);

const handleMouseDownAtom = atom(
  null,
  (get, set) => {
    set(drawingAtom, true);
  }
);

const handleMouseUpAtom = atom(null, (get, set) => {
  set(drawingAtom, false);
});

const handleMouseMoveAtom = atom(
  null,
  (get, set, update: Point) => {
    if (get(drawingAtom)) {
      set(addDotAtom, update);
    }
  }
);

export const SvgRoot = () => {
  const [, handleMouseUp] = useAtom(handleMouseUpAtom);
  const [, handleMouseDown] = useAtom(handleMouseDownAtom);
  const [, handleMouseMove] = useAtom(handleMouseMoveAtom);
  return (
    <svg
      width="200"
      height="200"
      viewBox="0 0 200 200"
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseMove={(e) => {
        handleMouseMove([e.clientX, e.clientY]);
      }}
    >
      <rect width="200" height="200" fill="#eee" />
      <SvgDots />
    </svg>
  );
};
```

### App.tsx

```tsx
import { SvgRoot } from "./SvgRoot";

const App = () => (
  <>
    <SvgRoot />
  </>
);

export default App;
```

튜토리얼에서 봤던 친구들이다. 기능 역시 동일하다.  
![](https://velog.velcdn.com/images/taez224/post/6faae30c-8fb4-41cb-b0a8-97f48aff8640/image.gif)

## 점에서 선으로

이제 점은 볼만큼 봤으니 선을 만들어 보자.  
그 역할은 새로운 SvgShape.tsx에게 맡기자.

### SvgShape.tsx

```tsx
// SvgShape.tsx
import { atom, useAtom } from "jotai";

import { Point } from "./types";

const pointsToPath = (points: readonly Point[]) => {
  let d = "";
  points.forEach((point) => {
    if (d) {
      d += \` L ${point[0]} ${point[1]}\`;
    } else {
      d = \`M ${point[0]} ${point[1]}\`;
    }
  });
  return d;
};

const shapeAtom = atom({ path: "" });

export const addShapeAtom = atom(
  null,
  (_get, set, update: readonly Point[]) => {
    set(shapeAtom, { path: pointsToPath(update) });
  }
);

export const SvgShape = () => {
  const [shape] = useAtom(shapeAtom);
  return (
    <g>
      <path
        d={shape.path}
        fill="none"
        stroke="black"
        strokeWidth="3"
      />
    </g>
  );
};
```

갑자기 이게 뭔가 당황하지 말고 찬찬히 살펴보자.

```tsx
// primitive atom
const shapeAtom = atom({ path: "" });
```

먼저 선의 경로를 값으로 가지는 shapeAtom이다.

```tsx
// Write only atom
export const addShapeAtom = atom(
  null,
  (_get, set, update: readonly Point[]) => {
    set(shapeAtom, { path: pointsToPath(update) });
  }
);
```

addShapeAtom은 Point들을 받아서 path로 변환시켜주는 atom이다.  
pointsToPath(points)는 그냥 그 역할을 하는 함수인가보다 하고 넘어가자.  
SvgShape 컴포넌트는 shapeAtom의 값으로 path를 그려주는 컴포넌트가 되시겠다.

### SvgDots.tsx 수정

```tsx
// SvgDots.tsx
...
import { addShapeAtom } from "./SvgShape";

...
...

export const commitDotsAtom = atom(
  null,
  (get, set) => {
    set(addShapeAtom, get(dotsAtom));
    set(dotsAtom, []);
  }
);
```

SvgDots에 commitDotsAtom을 추가했다.  
이 Write only atom은 dotsAtom의 값을 addShapeAtom에 set 해주고 dotsAtom을 초기화 시킨다.  
즉 dotsAtom의 point들을 path로 바꿔주고 point들을 지워준다는 것  
그럼 이제 SvgRoot에 추가해보자.

### SvgRoot.tsx 수정

```tsx
import { SvgShape } from "./SvgShape";
import { addDotAtom, commitDotsAtom, SvgDots } from "./SvgDots";
/*
    중략
*/
const handleMouseUpAtom = atom(null, (get, set) => {
  set(drawingAtom, false);
  set(commitDotsAtom, null);
});
/*
    중략
*/
export const SvgRoot = () => {
  const [, handleMouseUp] = useAtom(handleMouseUpAtom);
  const [, handleMouseDown] = useAtom(handleMouseDownAtom);
  const [, handleMouseMove] = useAtom(handleMouseMoveAtom);
  return (
    <svg
      width="200"
      height="200"
      viewBox="0 0 200 200"
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseMove={(e) => {
        handleMouseMove([e.clientX, e.clientY]);
      }}
    >
      <rect width="200" height="200" fill="#eee" />
      {/* SvgShape 추가 */}
      <SvgShape />
      <SvgDots />
    </svg>
  );
};
```

onMouseUp 되는 순간 point들이 path로 바뀌어야 하니까 해당 atom에 commitDotsAtom을 setter(write function)에 넣어주었다.

자, 이제 생각한 대로 동작 하는지 캔버스에 그려보자

![](https://velog.velcdn.com/images/taez224/post/aeb1cfb9-8510-4fa2-a211-c59985842c80/image.gif)

## 참조

[https://egghead.io/lessons/react-structure-jotai-atoms-and-add-functionality-to-a-react-app](https://egghead.io/lessons/react-structure-jotai-atoms-and-add-functionality-to-a-react-app)  
[https://codesandbox.io/embed/jotai-tutorial-04-6fkir](https://codesandbox.io/embed/jotai-tutorial-04-6fkir)

[![profile](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII=)](https://velog.io/@taez224/posts)

흔하지 않은 개발자

## 연관된 노트

- [[Jotai 05 - Read Write atom]] - 이전 글
- [[Jotai 07 - atoms in atom]] - 다음 글
