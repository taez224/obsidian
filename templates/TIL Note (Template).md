---
uuid: <% moment(tp.file.title).format("YYYYMMDDHHmmss") %>
title: "TIL: {{date}}"
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
updated: <% tp.file.last_modified_date("YYYY-MM-DDTHH:mm:ss") %>
alias: 
- "<% moment(tp.file.title).format("MMMM Do, YYYY") %>"
- "<% moment(tp.file.title).format("dddd Do MMMM, YYYY") %>"
tags: ["TIL"]
---
# [[<% tp.file.title %>|<% moment(tp.file.title).format("MMMM Do, YYYY") %>]]


## Title
<% tp.file.cursor() %>


## 🎯 Daily Checklist

- [ ] 아침 운동
- [ ] 간식 안먹기
- [ ] 정시 퇴근


## 🏷️ Category/Tags
- #programming
- #<language_or_technology>


## 📋 Summary
- Brief overview of what was learned.


## 📝 Details


## 🔗 Links/References
- [Title of Source](URL)


```dataview
LIST
FROM #type/timeline/daily
WHERE week = [[<%tp.date.now("YYYY")%>-W<%tp.date.now("ww")%>]]
```

---

## 📇 Additional Metadata
- 🗂 Type:: #type/timeline/daily 
- 🗓️ Week:: [[<% moment(tp.file.title).format("YYYY-[W]ww") %>]]
