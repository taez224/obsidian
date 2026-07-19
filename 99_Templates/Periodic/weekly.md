---
created: <% moment(tp.file.title, "gggg-[W]WW").format("YYYY-MM-DD") %>
type: weekly
week: <% tp.file.title %>
month: <% moment(tp.file.title, "gggg-[W]WW").format("YYYY-MM") %>
tags:
  - type/timeline/weekly
---

# 📆 Weekly Review - <% moment(tp.file.title, "gggg-[W]WW").format("gggg [W]WW") %>


> [!important]  Highlight of the week  
> Highlight of the Week

---

## **🎯 이번 주 주요 목표**
- 

## **📋 이번 주 할 일**

> [!todo] 이번 주 남은 Tasks
> ```tasks
> not done
> due this week
> sort by priority desc
> ```

> [!success] 이번 주 완료된 Tasks
> ```tasks
> done this week
> sort by done desc
> ```

> [!question] No due date
> ```tasks
> not done
> no due date
> ```

> [!fail] Overdue
> ```tasks
> not done
> due before this week
> ```

---
## **✅ Checklist Summary**

```dataviewjs
const currentFolder = dv.current().file.folder;
// 라이브러리: moment 사용
const tasks = dv.pages(`"${currentFolder}"`)
    .file.tasks
    .filter(t => t.tags.includes("#routine/daily"));

// --- 주별 완료율 ---
const weeks = {};
tasks.forEach(t => {
    const week = moment(t.date).isoWeek(); // ISO week 기준
    if (!weeks[week]) weeks[week] = [];
    weeks[week].push(t);
});

dv.header(3, "📅 주별 완료율");
Object.keys(weeks).sort((a,b) => a-b).forEach(week => {
    const all = weeks[week];
    const completed = all.filter(t => t.completed).length;
    const percentage = all.length === 0 ? 0 : Math.round((completed / all.length) * 100);
    dv.paragraph(`Week ${week}: ${percentage}% (${completed} / ${all.length})`);
});
```


---

## **📝 이번 주 작성/수정된 노트**
```dataview
TABLE WITHOUT ID file.link as "노트", default(date(created), file.cday) as "생성일", file.mtime as "마지막 수정"
FROM ""
WHERE (startswith(file.folder, "01_") OR startswith(file.folder, "20_") OR startswith(file.folder, "30_"))
AND (
  dateformat(default(date(created), file.cday), "kkkk-'W'WW") = "<% tp.file.title %>"
  OR dateformat(file.mtime, "kkkk-'W'WW") = "<% tp.file.title %>"
)
SORT file.mtime DESC
```

---

## **🌱 Slipbox 승격 후보**

> 이번 주 발견한 "정제하면 영구 노트가 될 만한 아이디어"를 모은다.
> 정리 가이드: [[_inbox.base|_inbox]] 의 "🟡 정리 부채 (7일+)" view와 [[_global-health.base|_global-health]] 의 "📥 Inbox 정리 부채 (7일+)" view 함께 참조.

### 📥 Inbox에서 (7일+ 체류)

> 단일 진실 원천: [[_inbox.base|_inbox]] base의 "🟡 정리 부채 (7일+)" view를 embed.

![[_inbox.base#🟡 정리 부채 (7일+)]]

### 🔧 DevLog에서 (이번 주 작성, 재사용 가치 있는 인사이트)
```dataview
LIST
FROM "30_Resources/Development/DevLog/daily"
WHERE file.ext = "md"
AND dateformat(file.day, "kkkk-'W'WW") = "<% tp.file.title %>"
SORT file.day DESC
```

> [!tip] 승격 기준
> 1. **재사용 가능성**: 다른 맥락에서도 인용될 만한 개념인가?
> 2. **자기 언어로 정제 가능?**: 외부 인용 없이 본인 언어로 설명 가능?
> 3. **연결점**: 기존 Slipbox 노트와 최소 1개 이상 연결 가능?
> 3개 다 ✅면 → `01_Slipbox/`에 새 노트 작성 (`type: permanent`, `status: seedling`)

### 📰 이번 주 처리한 Clippings
```dataview
LIST
FROM "30_Resources/References/Clippings"
WHERE file.ext = "md"
AND status != "unread"
AND dateformat(file.mtime, "kkkk-'W'WW") = "<% tp.file.title %>"
SORT file.mtime DESC
```

---

## **🧹 주간 정리 체크리스트**

> 모든 대상이 아래 embed로 바로 보인다 — base 파일을 따로 열 필요 없음.

- [ ] Inbox 7일+ 체류 노트 분류 (승격/Resources/삭제) — 위 "📥 Inbox에서" embed 참조
- [ ] 프로젝트 허브 미갱신 → 현재 상태·다음 액션 갱신 또는 on-hold 전환

![[_global-health.base#🟢 프로젝트 허브 미갱신 (14일+)]]

- [ ] 고립된 Slipbox 노트에 최소 1개 링크 추가

![[01_Slipbox/_index.base#고립된 노트]]

- [ ] 이번 주 DevLog 훑어보고 Slipbox 승격 후보 1개 이상 선정
- [ ] Clippings `status: unread` 1개 이상 처리

![[_global-health.base#📰 오래된 Clippings (30일+)]]


## 🗓 Monthly Note 링크  

> [!info] 이번 달 Monthly Note
> [[<% moment(tp.file.title, "gggg-[W]WW").format("YYYY-MM") %>|🗓 이번 달]]

## 🗓 Daily Notes 링크  

> [!summary] 이번 주 Daily Notes
> ```dataview
> LIST
> FROM "10_Periodic Notes" AND #type/timeline/daily
> WHERE week = "<% tp.file.title %>"
> SORT file.name ASC
> ```
