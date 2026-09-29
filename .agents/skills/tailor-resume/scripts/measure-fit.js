// 브라우저 창의 javascript 도구에 그대로 넣어 실행한다. 창 폭은 1100px이어야 한다.
// pretendardLoaded: Pretendard가 실제로 로드됐는지. false면 대체 폰트로 잰 값이므로 쓰지 않는다.
//   document.fonts.check()는 폰트 선언이 없거나 로딩에 실패해도 true를 돌려줄 수 있어 쓰지 않는다.
// spareMm: A4 인쇄 영역(277mm) 대비 남은 여유. 1쪽은 10mm 이상을 유지하고, 2쪽은 0mm 이상이어야 한다.
// lines: 쪽별 불릿의 줄 수. 불릿 한 줄은 약 4.8mm다.
const mm = 96 / 25.4;
JSON.stringify({
  width: innerWidth,
  pretendardLoaded: [...document.fonts].some(
    (font) => font.family.includes('Pretendard') && font.status === 'loaded',
  ),
  pages: [...document.querySelectorAll('article.page')].map((page) => {
    const style = getComputedStyle(page);
    const used = page.lastElementChild.getBoundingClientRect().bottom
      - page.getBoundingClientRect().top - parseFloat(style.paddingTop);
    return {
      spareMm: +(277 - used / mm).toFixed(1),
      lines: [...page.querySelectorAll('li')].map((li) => ({
        title: li.querySelector('strong')?.textContent ?? '',
        lines: Math.round(li.getBoundingClientRect().height / parseFloat(getComputedStyle(li).lineHeight)),
      })),
    };
  }),
});
