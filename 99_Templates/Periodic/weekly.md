---
tags:
  - type/timeline/weekly
month: <% tp.date.now("YYYY-MM") %>
---
<%*
const now = tp.date.now("YYYY-MM-DD");
const day = moment(now).day();  // 0=Sunday, 1=Monday, ..., 6=Saturday

// 이번 주 일요일 (주 시작)
const sunday = moment(now).subtract(day, 'days').format("YYYY-MM-DD");

// 이번 주 토요일 (주 끝)
const saturday = moment(sunday).add(6, 'days').format("YYYY-MM-DD");
%>
# 📆 Weekly Review - <% tp.date.now("gggg [W]WW") %>


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
>```tasks
not done
no due date

> [!fail] Overdue
> ```tasks
> not done
> due before this week

---
## **✅ Checklist Summary**

```dataviewjs
const currentFolder = dv.current().file.folder;
// 라이브러리: moment 사용
const tasks = dv.pages(`"${currentFolder}"`)
    .file.tasks
    .filter(t => t.tags.includes("#habit/daily"));

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
TABLE WITHOUT ID file.link as "노트", file.cday as "생성일", file.mtime as "마지막 수정"
FROM ""
WHERE (startswith(file.folder, "01_") OR startswith(file.folder, "20_") OR startswith(file.folder, "30_"))
AND (
  dateformat(file.cday, "yyyy-WW") = dateformat(this.file.cday, "yyyy-WW")
  OR dateformat(file.mtime, "yyyy-WW") = dateformat(this.file.cday, "yyyy-WW")
)
SORT file.mtime DESC
```


## 🗓 Monthly Note 링크  

> [!info] 이번 달 Monthly Note
> `=link(dateformat(date(this.file.name, "kkkk-'W'WW"), "yyyy-MM"))`

## 🗓 Daily Notes 링크  

> [!summary] 이번 주 Daily Notes
> ```dataview
> LIST
FROM "10_Periodic Notes" and #type/timeline/daily
WHERE week = "<%tp.date.now('YYYY')%>-W<%tp.date.now('ww')%>"
SORT file.name ASC
