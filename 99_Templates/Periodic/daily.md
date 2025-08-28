---
type:
  - daily
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("gggg-[W]WW") %>
tags:
  - "#type/timeline/daily"
---

# 📅 <% moment(tp.file.title).format("MMMM Do, YYYY") %>

> [!note]  Capture  
> - (아이디어, 링크 등 빠르게 기록)

> [!important]  Highlight of the day  
> 

---

## ✅ Daily Checklist

- [ ] #task/daily Inbox or Slipbox 노트 작성
- [ ] #task/daily 8000+보 걷기
- [ ] #task/daily 운동 or 링피트!


## **🎯 오늘의 주요 목표**
- [ ] 


## 📋 할 일

> [!todo] 오늘 Tasks
> ```tasks
not done
due on {{date:YYYY-MM-DD}}
sort by priority desc

> [!todo] 이번 주 Tasks
> ```tasks
not done
due after {{date:YYYY-MM-DD}}
due before <% moment(tp.date.now()).add(7,'days').format("YYYY-MM-DD") %>

> [!todo] 한 달 내 Tasks
> ```tasks
not done
due after <% moment(tp.date.now()).add(6,'days').format("YYYY-MM-DD") %>
due before <% moment(tp.date.now()).add(28,'days').format("YYYY-MM-DD") %>

> [!fail] Overdue
> ```tasks
not done
due before {{date:YYYY-MM-DD}}

---

## 📁 오늘 작성/수정한 노트

> [!summary] 오늘 작성/수정한 노트
> ```dataview
TABLE WITHOUT ID file.link as "노트", file.cday as "생성일", file.mday as "마지막 수정"
from ""
where (startswith(file.folder, "00_") or startswith(file.folder, "01_") or startswith(file.folder, "20_") or startswith(file.folder, "30_"))
where date(file.cday) = date({{date:YYYY-MM-DD}}) or date(file.mday) = date({{date:YYYY-MM-DD}})
SORT file.mtime DESC
>```


---

## 📝 오늘 회고

> [!done] 오늘 완료한 Tasks
> ```tasks
> done on {{date:YYYY-MM-DD}}
> ```

### 🎯 오늘 한 일 
- 

### 🔮 **내일 계획**
- 
