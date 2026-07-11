---
title: Jotai - atoms in atom
created: 2023-04-08
published: 2023-04-08
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/Jotai-atoms-in-atom
series: Jotai tutorial
series_order: 7
summary: 여러 atom을 하나의 atom으로 다뤄 복수 도형과 복합 상태를 보존하는 패턴을 설명한다.
related:
  - "[[Jotai 06 - atom 구조화]]"
---

# Jotai - atoms in atom

## 들어가며

이번 포스트는 [Jotai - atom 구조화](https://velog.io/@taez224/Jotai-atom-%EA%B5%AC%EC%A1%B0%ED%99%94) 에서 이어지는 내용입니다.

Jotai의 creator인 Daishi Kato의 [egghead lesson](https://egghead.io/lessons/react-preserve-state-by-combining-multiple-jotai-atoms-into-one-atom) 을 바탕으로 하고 있으며 전체 코드는 [code sandbox](https://codesandbox.io/embed/jotai-tutorial-05-yml8m?fontsize=14&hidenavigation=1&module=%2Fsrc%2FSvgShapes.tsx&theme=dark) 에서 확인하실 수 있습니다.

## 하나의 도형

[지난 포스트](https://velog.io/@taez224/Jotai-atom-%EA%B5%AC%EC%A1%B0%ED%99%94) 에서 우리가 만든 결과물은 다음처럼 하나의 path만 표시가 되었다.  
![](https://velog.velcdn.com/images/taez224/post/ae0c1710-492f-448c-9b50-f687ab089738/image.gif)

## 여러 개의 도형

오늘 우리의 목표는 다중 경로를 나타내는 것이다. 그러기 위해서는 새로운 파일인 SvgShapes.tsx가 필요하다.

### SvgShapes.tsx 작성

```tsx
// SvgShapes.tsx
import { atom, useAtom } from "jotai";
import { Point, ShapeAtom } from "./types";

const shapeAtomsAtom = atom<ShapeAtom[]>([]);
```

shapeAtomsAtom은 atom의 배열을 값으로 가지는 atom으로 이름하여 `atoms in atom` 이다.

### SvgShape.tsx 수정

다음으로 SvgShape.tsx를 수정해보자.  
전역으로 정의된 atom 대신 props로 shapeAtom을 받아서 사용한다.

```tsx
// SvgShape.tsx

...

export const SvgShape = ({
  shapeAtom
}: {
  shapeAtom: ShapeAtom;
}) => {
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

addShapeAtom에서의 전역 atom을 사용하지 않고 대신 createShapeAtom 함수를 내보내서 다른 파일에서 사용할 수 있다.

```tsx
// SvgShape.tsx
export const createShapeAtom = (
  points: readonly Point[]
) => atom({ path: pointsToPath(points) });

...
```

### SvgShapes.tsx 수정

이제 다시 SvgShapes.tsx로 돌아가서 이를 가져와보자

```tsx
// SvgShapes.tsx
import { createShapeAtom, SvgShape } from "./SvgShape";

const shapeAtomsAtom = atom<ShapeAtom[]>([]);

export const addShapeAtom = atom(
  null,
  (_get, set, update: readonly Point[]) => {
    const shapeAtom = createShapeAtom(update);
    set(shapeAtomsAtom, (prev) => [
      ...prev,
      shapeAtom
    ]);
  }
);
```

addShapeAtom은 새로운 shapeAtom을 만들고 이를 shapeAtomsAtom에 추가해준다.

```tsx
// SvgShapes.tsx

...

export const SvgShapes = () => {
  const [shapeAtoms] = useAtom(shapeAtomsAtom);
  return (
    <g>
      {shapeAtoms.map((shapeAtom) => (
        <SvgShape
          key={\`${shapeAtom}\`}
          shapeAtom={shapeAtom}
        />
      ))}
    </g>
  );
};
```

SvgShapes는 shapeAtomsAtom의 shapeAtom 배열을 반복하는 새로운 컴포넌트다.

이제 기존의 SvgDots.tsx와 SvgRoot.tsx에서 새로 만든 컴포넌트를 가져다 쓰면 끝이다.

### SvgDots.tsx 수정

```tsx
// import { addShapeAtom } from "./SvgShape";
import { addShapeAtom } from "./SvgShapes";
```

### SvgRoot.tsx 수정

```tsx
// import { SvgShape } from "./SvgShape";
import { SvgShapes } from "./SvgShapes";
```

## 결과

![](https://velog.velcdn.com/images/taez224/post/8c15bd22-1101-4438-a32c-8e9c8ca547f3/image.gif)  
jotai와 `atoms in atom` 방법을 사용하여 여러 개의 atom을 다루는 방식을 알아보았다.

[![profile](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAASbSURBVHgB7Z0tTytBFIYP914BDiQ4cIADB0EhwYFE8ifq7g/hJ2CRSCQ4kOCobF3ruHk3maS5aSnbdnfPOe/7JE0oCTvTnmc+dvbMsNbr9b5M0PLLBDUSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAOX+MhPX1dTs+Prbt7W3b3d21jY2N6ndgPB7bYDCw4XBor6+v9vHxUb1nIL0Ae3t7dn5+XgV9FhABYuC1v79f/Q4SPD8/28vLi2UmrQA/Cfx34O/wwjXu7u7S9gi/z87O/loyELTr62vb2tqyZcFQcXp6Wv2MXiEb6SaBCDwEWDVFqmykEgABOjo6sqbAtbNJkEaAi4uLRoNfQBmXl5eWhRQCIChlnG6Dk5OTVstrkvACYKLXxJg/D5RZ1hEiE14ABGIVs/26IPgZeoHQAiDwbYz7s4AA0XuB0AIsusizKsrycmRCC+Dhyz84OLDIhBUAra/rHgCgDpGHgbAC7OzsmBc81aUuYQXY3Nw0L3iqS13CCtDFrd8sPNWlLsoIIkcCkBNWAE8JGpGTRcIKgPw9L3iqS13CCvD5+Wle8FSXuoQVAJm8HlK0UAfUJSqhJ4Fvb2/WNcgcjkxoAfDld936oieKhhYAwX96erKuwJ6B6Oni4dcBIEAXvQAC//j4aNEJLwCC30UgUGaGzSIpVgLRC7Q5FKCsLFvG0iwFPzw8tBIUlIGyspDqWcD9/X2jEuDaKCMT6R4GIUBNzAlwzWzBByl3ByNYaK23t7dLP6vHfT6u9/7+bhlZ6/V6X5YYpI0jebRu/mD2wBfSHxCBngAv9ASQ4PDwsErhwvvJE0JGo1EV9H6/72KFsS1SCDAZyFngnh2vVUwSUV4WQUILULZnlR06aMGYqDW1QDN56khZho6+Ghh2DoBgXF1dTZ3koZWvcqWubECdtg0NZUQ+QiakAGjxOA9gHhABj4wXeWyMHgX5/j85Zwi9AXoeD4+n6xJOAASk7nbwkjyCGT0meXg/mcWDYOMsIJwShtaO3mWRHT/odaINCaHmAIsEHyCQOP6tHAHXFKVukSQIsxK4aPDbBnWMdG5ACAHwhUYIfgHzEwwjEXAvQFdHwCzLzc1NiC1jrgXA2I31/Ijbr1HnCEfKuRagq/N/VgXuJLzPB9wKgMBnOITJu8RuBUDXnwHvQ4FLAbDkGrnr/x8MBV7vClwKEHHWPw+vn8mdANlaf8FrL+BOgIytv+Dxs7kSAC0kY+sveOwFXAnQ5bGvbdH0A6m6uBLAw8GPTePtaFk3AmTv/gtYF/A0DLgRgKH1Fzx9VjcCIBuHBU89nRsBkKrFgqfNJm5SwpBGVc7fz/CvWKZRUsk9bS1PvzVMfI+OiiVHApAjAciRAORIAHIkADkSgBwJQI4EIEcCkCMByJEA5EgAciQAORKAHAlAjgQgRwKQIwHIkQDkSAByJAA5EoAcCUCOBCBHApAjAciRAORIAHIkADkSgBwJQI4EIOcfGjV2tEfztqEAAAAASUVORK5CYII=)](https://velog.io/@taez224/posts)

흔하지 않은 개발자

이전 포스트

## 연관된 노트

- [[Jotai 06 - atom 구조화]] - 이전 글
