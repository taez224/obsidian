---
cssclasses:
  - width-100
---

```dataviewjs
// 1️⃣ Dataview 페이지 가져오기 (정렬: 별점 -> 생성일)
const currentFolder = dv.current().file.folder;
const pages = dv.pages(`"${currentFolder}"`)
    .where(p => p.file.name != dv.current().file.name)
    .sort(p => [p.my_rate ?? 0, p.file.cday], 'desc');

// 2️⃣ 카드 컨테이너 생성
const container = document.createElement("div");
container.className = "book-cards";

// 3️⃣ 카드 생성
pages.forEach(p => {
    const titleDisplay = p.file.name.length > 30 ? p.file.name.slice(0,30) + "..." : p.file.name;
    const rate = p.my_rate ?? 0;

    // 카드
    const card = document.createElement("div");
    card.className = "book-card";

    // 이미지
    const img = document.createElement("img");
    img.src = p.cover_url ?? "";
    img.alt = "표지";
    img.addEventListener("click", () => {
        app.workspace.openLinkText(p.file.path, "/", true);
    });
    card.appendChild(img);

    // 콘텐츠
    const content = document.createElement("div");
    content.className = "content";
    card.appendChild(content);
    
    // 제목 (링크 포함)
	const titleDiv = document.createElement("div");
	titleDiv.className = "title";
	
	const titleLink = document.createElement("a");
	titleLink.textContent = titleDisplay;
	titleLink.href = "#"; 
	titleLink.style.textDecoration = "none"; 
	titleLink.style.color = "inherit"; 
	titleLink.addEventListener("click", (e) => {
	    e.preventDefault();
	    app.workspace.openLinkText(p.file.path, "/", true);
	});
	titleDiv.appendChild(titleLink);
	content.appendChild(titleDiv);
	
	// 별점 + 한줄평
	const ratingNoteWrapper = document.createElement("div");
	ratingNoteWrapper.className = "rating-note-wrapper";
	ratingNoteWrapper.style.display = "flex";
	ratingNoteWrapper.style.flexDirection = "column";
	ratingNoteWrapper.style.gap = "0.25rem";

    // 별점
    const ratingDiv = document.createElement("div");
    ratingDiv.className = "rating";

    if (rate) {
        for (let i = 1; i <= 5; i++) {
            const fillPercent = Math.max(Math.min(rate - (i - 1), 1), 0) * 100;
            
            const starSpan = document.createElement("span");
            starSpan.className = "star";
            starSpan.textContent = "★";

            const filled = document.createElement("span");
            filled.className = "filled";
            filled.textContent = "★";
            filled.style.width = `${fillPercent}%`;

            starSpan.appendChild(filled);
            ratingDiv.appendChild(starSpan);
        }
        const numText = document.createElement("span");
        numText.textContent = ` ${rate}`;
        ratingDiv.appendChild(numText);
    } else {
        ratingDiv.textContent = "별점 없음";
    }
    ratingNoteWrapper.appendChild(ratingDiv);

    // 한줄평
    const noteDiv = document.createElement("div");
    noteDiv.className = "note";
    noteDiv.textContent = p.book_note ?? "";
    ratingNoteWrapper.appendChild(noteDiv);
    
    content.appendChild(ratingNoteWrapper);

    // 메타
    const metaDiv = document.createElement("div");
    metaDiv.className = "meta";
    if (p.author) {
        const authorDiv = document.createElement("div");
        authorDiv.className = "author";
        authorDiv.textContent = p.author;
        metaDiv.appendChild(authorDiv);
    }
    if (p.publisher || p.publish_date) {
        const pubDiv = document.createElement("div");
        pubDiv.className = "publisher"
        pubDiv.textContent = `${p.publisher ?? ""} / ${p.publish_date ? dv.date(p.publish_date).toFormat("yyyy-MM-dd") : ""}`;
        metaDiv.appendChild(pubDiv);
    }
    if (p.status || p.start_read_date || p.finish_read_date) {
        const statusDiv = document.createElement("div");
        statusDiv.className = "status";
        statusDiv.textContent = `${p.status ?? ""} / ${p.start_read_date ? dv.date(p.start_read_date).toFormat("yyyy-MM-dd") : ""} ~ ${p.finish_read_date ? dv.date(p.finish_read_date).toFormat("yyyy-MM-dd") : ""}`;
        metaDiv.appendChild(statusDiv);
    }
    content.appendChild(metaDiv);

    // 카드 컨테이너에 추가
    container.appendChild(card);
});

// 4️⃣ DataviewJS에 container 삽입
dv.container.appendChild(container);
```

	