/* content/*.md에서 생성한 글: 수식(KaTeX)과 Mermaid를 브라우저에서 그린다.
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
  function run() { renderMath(); renderMermaid(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
