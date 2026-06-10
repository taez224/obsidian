# Humanize Korean Strict Audit

- run_id: 2026-06-08-004
- file: `20_Projects/blog/AI로 개인은 빨라졌는데, 팀 진척은 그대로인 이유 v4.md`
- mode: strict
- result: audit only

## Judgment

치명적인 번역투는 많지 않지만, 회사 기술블로그 기준으로 문서체 한자어가 아직 꽤 남아 있습니다.

기술 용어 자체인 `Reviewability`, `Traceability`, `provenance`, `Absorptive Capacity`, `Workslop`, `Thin Harness, Fat Skills`는 보존 대상입니다. 문제는 이 용어를 둘러싼 한국어 문장이 `전가`, `유입`, `편입`, `반영`, `소요`, `제공하는 것`, `대입하면` 같은 표현으로 굳는 지점입니다.

## Highest Priority Fixes

1. `리뷰 가능성이란` -> `여기서 말하는 Reviewability는`
2. `해석 비용으로 전가됩니다` -> `해석 비용으로 넘어갑니다`
3. `외부에서 유입된 지식` -> `바깥에서 들어온 지식`
4. `저장소로 유입되지만` -> `저장소에 들어오지만`
5. `팀의 자산으로 편입되기 전` -> `팀의 자산이 되기 전`
6. `코드가 반영되기 전` -> `코드가 들어오기 전`
7. `환경을 제공하는 것` -> `환경`
