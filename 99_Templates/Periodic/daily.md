---
created: <% moment(tp.file.title).format("YYYY-MM-DD") %>
type: daily
date: <% moment(tp.file.title).format("YYYY-MM-DD") %>
week: <% moment(tp.file.title).format("gggg-[W]WW") %>
tags:
  - type/timeline/daily
---

# 📅 <% moment(tp.file.title).format("MMMM Do, YYYY") %>

[[<% moment(tp.file.title).subtract(1, 'days').format("YYYY-MM-DD") %>|◀ 어제]] · [[<% moment(tp.file.title).format("gggg-[W]WW") %>|🗓 주간]] · [[<% moment(tp.file.title).add(1, 'days').format("YYYY-MM-DD") %>|내일 ▶]]

> [!note]  Capture  
> 오늘 남겨두고 싶은 생각이 있으면 Inbox에 적는다. 오늘의 기록은 여기에 남긴다.
> -

> [!important]  Highlight of the day  
> 

---

## ✅ Daily Checklist

- [ ] #routine/daily 8000+보 걷기
- [ ] #routine/daily 운동 or 링피트!


## **🎯 오늘의 주요 목표**
- [ ] 


## 📋 할 일

> [!todo] 오늘 Tasks
> ```tasks
> not done
> due on <% moment(tp.file.title).format("YYYY-MM-DD") %>
> sort by priority desc
> ```

> [!todo] 이번 주 Tasks
> ```tasks
> not done
> due after <% moment(tp.file.title).format("YYYY-MM-DD") %>
> due before <% moment(tp.file.title).add(7,'days').format("YYYY-MM-DD") %>
> ```

> [!todo] 한 달 내 Tasks
> ```tasks
> not done
> due after <% moment(tp.file.title).add(6,'days').format("YYYY-MM-DD") %>
> due before <% moment(tp.file.title).add(28,'days').format("YYYY-MM-DD") %>
> ```

> [!fail] Overdue
> ```tasks
> not done
> due before <% moment(tp.file.title).format("YYYY-MM-DD") %>
> ```

---

## 📥 처리 대기 (Inbox)

> 지금 다시 쓸 노트를 살펴본다. 아직 판단할 재료가 부족하면 그대로 둔다. 30일 넘은 항목은 [[_inbox.base|_inbox]] base의 🔴 뷰에서 다시 살펴볼 수 있다.

![[_inbox.base#🃏 분류 도우미 (한 장씩 처리)]]

---

## 📁 오늘 작성/수정한 노트

> [!summary] 오늘 작성/수정한 노트
> ```dataview
> TABLE WITHOUT ID file.link as "노트", default(date(created), file.cday) as "생성일", file.mtime as "마지막 수정"
> FROM ""
> WHERE (startswith(file.folder, "00_") OR startswith(file.folder, "01_") OR startswith(file.folder, "20_") OR startswith(file.folder, "30_"))
> WHERE dateformat(default(date(created), file.cday), "yyyy-MM-dd") = "<% tp.file.title %>" OR dateformat(file.mtime, "yyyy-MM-dd") = "<% tp.file.title %>"
> SORT file.mtime DESC
> ```


---

## 📝 오늘 회고

> [!done] 오늘 완료한 Tasks
> ```tasks
> done on <% moment(tp.file.title).format("YYYY-MM-DD") %>
> ```

### 🎯 오늘 한 일 
- 

### 🔮 **내일 계획**
- 
