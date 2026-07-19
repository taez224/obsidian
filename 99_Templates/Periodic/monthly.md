---
created: <% moment(tp.file.title, "YYYY-MM").format("YYYY-MM-DD") %>
type: monthly
month: <% tp.file.title %>
tags:
  - type/timeline/monthly
---

# 📆 Monthly Review - <% moment(tp.file.title, "YYYY-MM").format("MMMM, YYYY") %>

  

> [!important] Highlight of the Month  
> 가장 기억에 남는 성과, 사건, 배운 점

---

## 🎯 **이번 달 주요 목표**
- [ ]

## 📋 이번 달 할 일

> [!todo] 이번 달 남은 Tasks
> ```tasks
> not done
> due this month
> sort by priority desc
> ```

> [!success] 이번 달 완료된 Tasks
> ```tasks
> done this month
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
> due before this month
> ```

---

## 📝 이번 달 작성/수정된 노트

```dataview
TABLE WITHOUT ID file.link as "노트", default(date(created), file.cday) as "생성일", file.mtime as "마지막 수정"
FROM ""
WHERE (startswith(file.folder, "01_") OR startswith(file.folder, "20_") OR startswith(file.folder, "30_"))
AND (
  dateformat(default(date(created), file.cday), "yyyy-MM") = "<% tp.file.title %>"
  OR dateformat(file.mtime, "yyyy-MM") = "<% tp.file.title %>"
)
SORT default(date(created), file.cday) DESC
```

---

## 🌱 Slipbox 성숙도 분포

> 이번 달 작성/수정된 영구 노트의 status. seedling이 많고 evergreen이 적으면 결정화 부채.

```dataview
TABLE WITHOUT ID
  status as "성숙도",
  length(rows) as "개수",
  rows.file.link as "노트"
FROM "01_Slipbox"
WHERE file.ext = "md" AND !startswith(file.name, "_")
AND (
  dateformat(default(date(created), file.cday), "yyyy-MM") = "<% tp.file.title %>"
  OR dateformat(file.mtime, "yyyy-MM") = "<% tp.file.title %>"
)
GROUP BY status
SORT length(rows) DESC
```

---

## 🚀 프로젝트 status 전환

### ✅ 이번 달 완료된 프로젝트

```dataview
TABLE WITHOUT ID
  file.link as "프로젝트",
  started as "시작",
  ended as "완료",
  status as "상태"
FROM "20_Projects"
WHERE status = "completed"
AND ended != null
AND dateformat(date(ended), "yyyy-MM") = "<% tp.file.title %>"
SORT date(ended) DESC
```

> [!todo]- 완료 후 처리
> - [ ] `40_Archive/`로 이동 검토
> - [ ] 회고에서 학습 추출 → Slipbox 승격 후보

### 🚨 프로젝트 허브 미갱신 (14일+)

> SSOT: [[_dashboard.base|_dashboard]] 의 "프로젝트 허브 미갱신 (14일+)" view embed. 허브의 현재 상태와 다음 액션을 갱신하고, 필요하면 on-hold / completed로 전환한다.

![[_dashboard.base#프로젝트 허브 미갱신 (14일+)]]

---

## 📚 이번 달 완독 도서

```dataview
TABLE WITHOUT ID
  file.link as "책",
  author as "저자",
  my_rate as "평점",
  finish_read_date as "완독일",
  book_note as "한줄평"
FROM "30_Resources/References/Books"
WHERE status = "완독"
AND finish_read_date != null
AND dateformat(date(finish_read_date), "yyyy-MM") = "<% tp.file.title %>"
SORT date(finish_read_date) DESC
```

> [!tip]- 완독 후 처리
> - [ ] 핵심 아이디어 1~2개 Slipbox로 승격
> - [ ] 책 노트에 `my_rate` 입력 (0~5, 0.1 단위)

---

## 🗑️ 30일+ 미처리 Inbox (결정 필요)

> SSOT: [[_inbox.base|_inbox]] 의 "🔴 결정 필요" view embed. **승격 or 삭제** 둘 중 하나만 선택.

![[_inbox.base#🔴 결정 필요 (30일+)]]

---

## 🗓 Notes 링크

> [!info] 이번 연도 Note
> [[<% moment(tp.file.title, "YYYY-MM").format("YYYY") %>|🗓 이번 연도]]

> [!summary] 이번 달 Weekly Notes
> ```dataview
> LIST
> FROM "10_Periodic Notes" AND #type/timeline/weekly
> WHERE month = "<% tp.file.title %>"
> SORT file.name ASC
> ```

---

## 📝 이번 달 회고

### 🎯 목표 달성도

> 이번 달 주요 목표 대비 결과. 잘 된 것 / 못 된 것 솔직히. 핑계 없이.

- 

### 💡 핵심 배운 점

> 1~3개로 압축. 추상적 깨달음보다 **다음 달에도 쓸 수 있는 형태**로.

- 

### 🛠️ 시스템 / 프로세스 개선

> 일하는 방식·도구·루틴 측면. 노트 시스템·코드 워크플로·시간 관리 모두 해당.

- 

### 🔮 다음 달 핵심 목표

> 1~3개. 측정 가능하게. 너무 많으면 하나도 못 끝낸다.

- [ ] 
