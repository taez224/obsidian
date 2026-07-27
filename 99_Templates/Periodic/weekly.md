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
> 3. **연결점**: 관계를 설명할 수 있는 기존 Slipbox 노트가 있으면 연결. 적합한 연결이 없어도 승격을 막지 않음
> 1·2가 ✅면 → 새 노트 또는 기존 노트 보강 후보로 검토. 적용은 `review-zettelkasten`·`permanent-note` 기준

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
- [ ] 프로젝트 허브 미갱신 → `sweep-project-context`로 근거를 대조하고 현재 상태·다음 액션 갱신 또는 on-hold 전환 검토

![[_global-health.base#🟢 프로젝트 허브 미갱신 (14일+)]]

- [ ] 고립된 Slipbox 노트 검토 → 관계를 설명할 수 있을 때만 링크

![[01_Slipbox/_index.base#고립된 노트]]

- [ ] 이번 주 DevLog에서 재사용 가능한 판단이 생겼다면 Slipbox 승격 후보로 검토
- [ ] 실제로 읽었거나 곧 사용할 Clippings가 있다면 처리

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
