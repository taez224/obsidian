---
title: "Front-end에서의 Testing"
created: 2023-02-02
published: 2023-02-02
tags:
  - blog
  - 개발/프론트엔드
status: published
author: TaeZ
publication: Nextree 기술 블로그
source: https://www.nextree.io/peuronteuendeueseoyi-teseuting/
summary: 뷰 구현에서 시작해 테스트하기 어려운 괴물 컴포넌트가 생기는 문제를 짚고, 모델·비즈니스 로직·뷰·테스트를 분리하는 프론트엔드 개발 패턴을 제안한다.
---

# Front-end에서의 Testing

## I. 신입 개발자의 일상

시작하기에 앞서 아직 프론트가 낯선 입사 1년이 막 지난 한 사원의 프론트엔드 개발 흐름을 살펴보자.

1. figma 등을 통해 본인이 맡은 페이지의 모습을 확인한다.
2. 퍼블리셔 분이 만들어주신 컴포넌트를 일단 복붙하고 시작한다.
3. 나름 관심사에 따라 한 페이지를 몇 개의 컴포넌트로 나눈다.
4. 다시 각각을 container와 view로 구분한다.
5. 비즈니스 로직을 어떻게든 구현한다.
6. storybook을 통해 제대로 동작을 하는지 확인한다.
7. 뭔가 꺼림칙하지만 이정도면 됐다 싶으니 commit 한다.

꺼림칙함의 이유는 바로 일정한 규칙 없이, 그리고 검증 없이 컴포넌트 구현에 급급했기 때문이다.

이미 만들어진 화면이 있기에 자연스럽게 뷰에서 시작하게 되는데, 그러다보면 컨테이너 컴포넌트에 길고 긴 로직이 들어가게 되고, 그 결과 괴물 컴포넌트가 탄생되는 과정을 눈앞에서 목도하게 된다.

이렇게 만들어진 괴물 컴포넌트를 테스팅, 그리고 디버깅 하기란 상당히 까다롭다.

## II. 건강한 개발 패턴

그렇다면 어떤 개발 패턴을 가져가야 할까?

> 개발의 순서가 일정하며 동시에 그 과정에서 생산된 코드가 충분히 검증될 수 있는 방법이다.

> 1. 요구사항을 분석하고 모델을 정리한다.
> 2. 모델을 토대로 비즈니스 로직을 구현한다.
> 3. 비즈니스 로직을 검증하는 테스트 코드를 작성한다.
> 4. 뷰를 작성하고 사용자 이벤트와 비즈니스 로직을 잇는다.
> 5. (필요에 따라) 컴포넌트를 검증하는 테스트 코드를 작성한다.

I.과 II.의 결정적인 차이점은 개발을 컴포넌트에서 시작하지 않는다는 것이다.

컴포넌트에서 개발을 시작하게 되면 중요한 모델 정보와 그 모델을 조작하는 로직은 응집되지 않고 파편화되기 쉽상이다.

이는 결과적으로 단위 테스트가 어려워지는 것으로 연결되며 결국 테스트를 포기한 채 꺼림칙한 코드로 남겨지게 된다.  

> 우선 요구사항을 분석하고 모델을 정리한다.  
> 그 다음 데이터와 비즈니스 로직을 어디에 두어야 할 지 찾는다.
> 
> 중요한 로직은 테스트하기 쉬운 곳에 둬야 한다.  
> 그리고 뷰는 테스트하기 어려운 곳이다.
> 
> 그러므로 중요한 로직은 hooks를 통해 분리한다.
> 
> 이렇게 분리된 hooks로 데이터와 로직을 캡슐화 하고 관리할 수 있다.

  
많은 개발자들이 프론트엔드에서의 테스팅에 의구심을 가지는 것이 바로 UI 테스트의 어려움과 실용성 여부 때문일 것이다. 하지만 중요한 비즈니스 로직 만큼은 가능한한 테스트를 작성해야 한다.

우선 간단한 boolean 토글 커스텀훅 부터 시작해 카운터 컴포넌트까지 구현해보면서 프론트엔드에서의 테스트와 친숙해져보자.

## III. jest와 react-testing-library

### 1\. 준비

```
yarn add -D jest @types/jest ts-jest jest-environment-jsdom @testing-library/react @testing-library/react-hooks react-test-renderer
```
- `jest`: JS 테스팅 라이브러리
- `react-testing-library`: React DOM 테스팅 라이브러리
- `react-test-renderer`: React 컴포넌트를 JS 객체로 렌더링 하는 렌더러 제공

### 2\. useToggle()

먼저 toggle 기능에 쓸 수 있는 useToggle을 구현해보고, 실제로는 이런 간단한 로직에 테스트코드까지 작성할 필요는 없겠지만  
연습삼아 테스트코드까지 작성해보자.

#### 2.1. custom hook 작성

```typescript
// useToggle.ts
function useToggle(defaultValue = false): [boolean, () => void, Dispatch<SetStateAction<boolean>>] {
  const [value, setValue] = useState(defaultValue);

  const toggle = useCallback(() => setValue(x => !x), []);

  return [value, toggle, setValue];
}

export default useToggle;
```

#### 2.2. test code 작성

```typescript
// useToggle.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import useToggle from '../useToggle';

test('Toggle Test', () => {
  // renderHook()에 Reack Hook을 호출하는 콜백을 인자로 넘기면 result를 담고 있는 객체를 반환
  const { result } = renderHook(() => useToggle());

  const [initialValue, toggle] = result.current; // result.current 값을 통해 전달된 콜백에서 반환하는 최신 값 반영

  expect(initialValue).toBe(false); // 초기 값은 false

  act(() => toggle()); // act()를 통해 훅과 상호작용하는 단위를 적용. 여기서는 toggle 함수 실행

  const [toggledValue] = result.current; // result.current 값을 통해 다시 최신 값 가져오기
  expect(toggledValue).toBe(true); // toggle 된 값은 true
})
```
- `test()`: 테스트 코드를 실행하기 위한 API. 하나의 테스트 케이스. `it()` 으로도 작성할 수 있다.
- `renderHook()`: 제공받은 콜백 함수를 호출하는 테스트 컴포넌트를 렌더링한다.
	- `result`: renderHook에 제공 된 콜백의 결과값을 담고 있다.
		- `result.current` 를 통해 hook의 최신 return 값을 가져올 수 있다.
- `expect()`: 테스트 할 대상을 넣는 API. matchers와 함께 사용한다.
- `toBe()`: 검증할 값과 기대 값이 같을 것이다 라는 것을 확인하기 위한 matcher
- `act()`: 제공받은 콜백 함수를 실행시켜 테스트 컴포넌트에 적용한다.

---

- 성공적으로 테스트를 통과하면 다음과 같은 화면이 나타난다.![](https://honey-domain-126.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F73cf0aae-4514-4d91-968b-62195225d597%2Ftoggle_test_success.png?id=f4e3305a-4b05-4ca3-aadd-24e763b82a6d&table=block&spaceId=decfb3a8-b848-4282-95f3-1afb8423d6eb&width=1720&userId=&cache=v2)
- 기대값과 실제값이 다르다면 다음과 같은 통지표를 받게 된다.![](https://honey-domain-126.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F883882f8-6f54-4a26-879d-6a9866c184aa%2Ftoggle_test_failed.png?id=4ac272c6-2093-4d77-a599-0f97c6b7d8b2&table=block&spaceId=decfb3a8-b848-4282-95f3-1afb8423d6eb&width=1700&userId=&cache=v2)

---

### 3\. useCounter()와 Counter 컴포넌트

다음으로 Counter 로직과 컴포넌트를 구현하고 테스트해보자.

#### 3.1. custom hook 작성

```typescript
// useCounter.ts
import { Dispatch, SetStateAction, useState } from 'react';

interface UseCounterOutput {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
  setCount: Dispatch<SetStateAction<number>>;
}

function useCounter(initialValue = 0): UseCounterOutput {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount(x => x + 1);
  const decrement = () => setCount(x => x - 1);
  const reset = () => setCount(initialValue);

  return {
    count,
    increment,
    decrement,
    reset,
    setCount,
  }
}

export default useCounter;
```

#### 3.2. hook test code 작성

```typescript
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react-hooks'
import useCounter from '../useCounter';

describe('카운터 테스트', () => { // test group

  test('1. 초기값 없이 카운트 증가', () => {
    const { result } = renderHook(() => useCounter()); // useCounter test

    expect(result.current.count).toBe(0); // 초기값은 0
    
    act(() => {
        result.current.increment(); // call increment() 
    })

    expect(result.current.count).toBe(1); // 값이 1 증가
  });

  test('2. 초기값 포함 카운트 감소', () => {
    const initialValue = 5;
    const {result} = renderHook(() => useCounter(initialValue)); 

    expect(result.current.count).toBe(initialValue); // 초기 값 확인

    act(() => {
        // call decrement() 2 times
        result.current.decrement();
        result.current.decrement();
    })

    expect(result.current.count).toBe(initialValue - 2); // 2 감소 확인
  });
});
```
- `describe()`: 테스트 코드들을 그룹화한다.

---

`Group test 결과`

![](https://honey-domain-126.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F6cbab12a-5255-4dc8-8d33-f305a2520d69%2FuseCounter_test.png?id=7dbce7bb-43aa-48e9-a39d-ba32da495402&table=block&spaceId=decfb3a8-b848-4282-95f3-1afb8423d6eb&width=1350&userId=&cache=v2)

---

#### 3.3. 컴포넌트와 storybook 작성

```typescript
// Counter.tsx
import React from 'react';
import { Button, ButtonGroup } from '@mui/material';
import useCounter from '../../hooks/useCounter';

interface Props {
  initialValue?: number
}

function Counter({ initialValue = 0 }: Props) {
  const { count, setCount, increment, decrement, reset } = useCounter(initialValue);

  const multiplyBy2 = () => setCount((x: number) => x * 2);

  return (
    <>
      <p><b>Count is <span data-testid='count'>{count}</span></b></p> <br/> // data-testid 사용
      <ButtonGroup>
        <Button variant="contained" color="primary" onClick={increment}>Increment</Button>
        <Button variant="contained" color="error" onClick={decrement}>Decrement</Button>
        <Button variant="contained" color="success" onClick={reset}>Reset</Button>
        <Button variant="contained" color="secondary" onClick={multiplyBy2}>Multiply by 2</Button>
      </ButtonGroup>
    </>
  )
}
export default Counter;
```
- `data-testid`: testing-library에서 해당 DOM을 쿼리하기 위한 testid 부여
```typescript
// Counter.stories.tsx
/* eslint-disable import/no-unresolved */
import { ComponentMeta, ComponentStory } from '@storybook/react';
import * as React from 'react';
import Counter from '../../components/Counter';

export default {
  //
  title: 'component/Countdown',
  component: Counter,
// @ts-ignore
} as ComponentMeta<typeof Counter>;

// @ts-ignore
const Template: ComponentStory<typeof Counter> = (args) => {

  return (
    <div>
      <Counter {...args} />
    </div>
  );
};

export const DefaultCounter = Template.bind({});
DefaultCounter.args = {
  initialValue: 0
};
DefaultCounter.storyName = 'counter';
```
- `storybook 화면`

![counter](https://media1.giphy.com/media/GIXrCtJthkOXIwsIej/giphy.gif?cid=790b7611014a9cfb3cff1bba541b8cb08cbaebf81cfd2c6a&rid=giphy.gif&ct=g)

#### 3.4. Storybook test code

```typescript
import React from 'react';
import { composeStories } from '@storybook/testing-react';
import * as stories from '../2-counter.stories';
import { fireEvent, render } from '@testing-library/react';

describe('Counter Test', () => {

  // 스토리를 렌더링 가능하도록 처리
  const {DefaultCounter} = composeStories(stories);

  it('should increase count without initial value', async () => {
    // DOM을 선택할 수 있는 쿼리 함수 제공
    const {getByRole, getByTestId} = render(<DefaultCounter/>); // render DefaultCounter story

    // data-testid로 쿼리
    const count = getByTestId('count');

    expect(count).toBeDefined(); // 'count'가 정의되어 있음을 확인
    expect(count.textContent).toBe(String(0)); // 'count'의 값이 0임을 확인
    
    // role과 name을 기준으로 쿼리 
    const incrementButton = getByRole('button', {name: 'Increment'}); // query Increment button

    fireEvent.click(incrementButton); // click increment button

    const afterIncrementCount = getByTestId(\`count\`); // 클릭 후 다시 'count' 쿼리

    expect(afterIncrementCount.textContent).toBe(String(1)); // 값이 1임을 확인
  });
});
```
- `composeStories()`: story를 가져와서 테스트할 수 있게 한다.
- `render()`: story를 렌더링한 결과를 query할 수 있는 함수들을 제공한다.
- `getBy*()`: 쿼리 조건에 일치하는 DOM 엘리먼트 하나를 선택한다.
	- `getByRole()`: 특정 role 값을 가지고 있는 엘리먼트 선택 (option으로 세부 query 가능)
		- `getByTestId()`: data-testid 값을 기준으로 선택
- `fireEvent.[eventName](DOM, option?)`: 사용자가 발생시킬 수 있는 이벤트를 발생시켜 준다.

`예시)` 다음과 같은 방법으로 Counter 컴포넌트를 테스트 할 수 있다.

```typescript
describe('Counter Test', () => {
    
  const {DefaultCounter} = composeStories(stories);
  
  const callFuncTimes = (fn: () => void, times = 1) => {
    //
    if (times < 1) return;
    for (let i = 0; i < times; i++ ) {
      fn();
    }
  }
  const clickButtonTimes = (button:HTMLElement) => (times = 1) => {
    callFuncTimes(() => fireEvent.click(button), times);
  }

  it('should decrease count with initial value', async () => {
    const {getByRole, getByTestId} = render(<DefaultCounter initialValue={5}/>);

    const count = getByTestId('count');

    expect(count).toBeDefined();
    const expectCount = (expectedCount: number) => expect(count.textContent).toBe(String(expectedCount));
    expectCount(5);

    const decrementButton = getByRole('button', {name: 'Decrement'});
    clickButtonTimes(decrementButton)(3);

    const afterDecrementCount = getByTestId(\`count\`);
    expectCount(5 - 3);
  });

  test('multiply 버튼 테스트', () => {
    const {getByRole, getByTestId} = render(<DefaultCounter initialValue={5}/>);
    const count = getByTestId('count');

    const multiplyButton = getByRole('button', { name: 'Multiply by 2' });
    clickButtonTimes(multiplyButton)(2);

    const afterMultiplyCount = getByTestId(\`count\`);
    expect(afterMultiplyCount.textContent).toBe(String(5 * 2 * 2));
  });

  test('reset 버튼 테스트', () => {
    const initialValue = 5;
    const {getByRole, getByTestId} = render(<DefaultCounter initialValue={initialValue}/>);
    const count = getByTestId('count');

    const getButtonByName = (name: string) => getByRole('button', { name });
    const resetButton = getButtonByName('Reset');
    const clickResetButton = clickButtonTimes(resetButton);
    clickResetButton(3);

    const expectCount = (expectedCount: number) => expect(count.textContent).toBe(String(expectedCount));
    expectCount(initialValue);

    const multiplyButton = getButtonByName('Multiply by 2');
    clickButtonTimes(multiplyButton)(3);
    clickResetButton();
    expectCount(initialValue);

  });
});
```

---

`Counter test 결과`

![](https://honey-domain-126.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fc4d53204-0d8c-4ec0-bece-94d3427f70fd%2F4.counter_test_success.png?id=699a3c3c-5903-4f39-941d-279b455258a1&table=block&spaceId=decfb3a8-b848-4282-95f3-1afb8423d6eb&width=830&userId=&cache=v2)

---

### 4\. yarn test

yarn test를 실행하면 모든 테스트가 수행된다.

![](https://honey-domain-126.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F0411b0ec-745b-449f-aea7-b98e1fa847b4%2Fyarn_jest.png?id=ef630ca3-3b6c-4a6e-8a25-b2ad186f6b72&table=block&spaceId=decfb3a8-b848-4282-95f3-1afb8423d6eb&width=1230&userId=&cache=v2)

## IV. 못다한 이야기

다음 주제들은 시간과 여백이 부족해 이번에 싣지 못하였다.

- interval 관련 훅인 useInterval()과 setTimeout이 포함된 로직의 test 방법
- 위 훅들과 useInterval()까지 포함된 useCountdown() 훅과 컴포넌트의 테스트
- storybook을 통한 interaction test
- API를 통해 서버에서 데이터를 가져오는 로직이 포함되어있을 때 API 모킹하는 방법
