
```dataview
TABLE WITHOUT ID "![|50](" + cover_url + ")" as "표지", file.link as "제목", author as "저자", publisher as "출판사", publish_date as "출판일", finish_read_date as "읽은 날짜", status as "상태", my_rate as 별점, book_note as "한줄평"
FROM "30_Resources/References/Books"
WHERE file.name != this.file.name
SORT my_rate DESC
```
