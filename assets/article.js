/* content/*.md에서 생성한 글: 수식(KaTeX)·Mermaid·레이아웃 아이콘(lucide)을 브라우저에서 그린다.
   라이브러리를 못 불러오거나 그리기에 실패하면 원문(TeX·Mermaid 코드)을 그대로 둔다. */
(function () {
  "use strict";
  function renderMath() {
    if (!window.katex) return;
    document.querySelectorAll(".math-inline, .math-display").forEach(function (el) {
      var tex = el.textContent;
      try {
        window.katex.render(tex, el, { displayMode: el.classList.contains("math-display"), throwOnError: true });
        el.classList.add("katex-ok");
      } catch (e) {
        el.textContent = tex;
        el.title = "수식 렌더 실패: " + e.message;
      }
    });
  }
  function renderMermaid() {
    var blocks = document.querySelectorAll("pre.mermaid-src");
    if (!blocks.length || !window.mermaid) return;
    window.mermaid.initialize({ startOnLoad: false, theme: "dark", securityLevel: "strict" });
    blocks.forEach(function (pre, i) {
      var src = pre.textContent;
      window.mermaid.render("mmd-" + i, src).then(function (r) {
        var fig = document.createElement("div");
        fig.className = "mermaid-figure";
        fig.setAttribute("role", "img");
        fig.innerHTML = r.svg; // mermaid가 securityLevel strict로 만든 SVG
        pre.replaceWith(fig);
      }).catch(function (e) {
        var note = document.createElement("div");
        note.className = "mermaid-error";
        note.textContent = "다이어그램 렌더 실패 — 원문 코드를 표시합니다: " + (e && e.message ? e.message : e);
        pre.parentNode.insertBefore(note, pre);
        var stray = document.getElementById("dmmd-" + i);
        if (stray) stray.remove();
      });
    });
  }
  function renderIcons() {
    // ChatGPT 레이아웃 태그의 <icon> → lucide SVG. 라이브러리가 없으면 빈 자리로 둔다(장식 요소).
    if (!window.lucide || !document.querySelector("i[data-lucide]")) return;
    try { window.lucide.createIcons({ icons: window.lucide.icons }); } catch (e) { /* 아이콘만 빠진다 */ }
  }
  function foldNotes() {
    // 게시 메모(참고·주의)는 원문 답변이 아니라 게시자의 대조·재구성 설명이라 기본으로 접는다.
    // 마크업만 바꾸고 글자는 그대로 둔다(JS가 없으면 펼친 채로 보인다).
    document.querySelectorAll(".art-body blockquote.alert-note, .art-body blockquote.alert-warning").forEach(function (bq) {
      var d = document.createElement("details");
      d.className = "alert-fold";
      var s = document.createElement("summary");
      var b = document.createElement("b");
      b.textContent = bq.classList.contains("alert-note") ? "참고" : "주의";
      var first = bq.querySelector("p");
      var strong = first && first.querySelector("strong");
      var hint = (strong ? strong.textContent : (first ? first.textContent : "")).replace(/[:：]\s*$/, "").trim();
      if (hint.length > 48) hint = hint.slice(0, 48) + "…";
      s.appendChild(b);
      s.appendChild(document.createTextNode(hint));
      d.appendChild(s);
      bq.parentNode.insertBefore(d, bq);
      d.appendChild(bq);
    });
  }
  function run() { foldNotes(); renderMath(); renderMermaid(); renderIcons(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
