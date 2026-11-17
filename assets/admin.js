// 관리 모드: 주소 끝에 ?admin 을 붙여 한 번 열면 이 브라우저에 기억되고(?admin=off 로 끔),
// 홈 카드·글 화면에 '삭제' 버튼이 보인다. 버튼은 GitHub의 그 파일 삭제 화면을 열 뿐이고,
// 실제 삭제 권한은 GitHub이 확인한다(저장소 쓰기 권한이 없는 사람은 지울 수 없다).
(() => {
  const REPO = "https://github.com/gwanhuiGIM/robotics-knowledge", BRANCH = "main";
  const p = new URLSearchParams(location.search);
  try {
    if (p.get("admin") === "off") localStorage.removeItem("rk-admin");
    else if (p.has("admin")) localStorage.setItem("rk-admin", "1");
    if (localStorage.getItem("rk-admin") !== "1") return;
  } catch { return; }

  const css = document.createElement("style");
  css.textContent = `.rk-badge{position:fixed;left:16px;bottom:16px;z-index:200;display:flex;gap:8px;align-items:center;background:#2a1d1f;border:1px solid #6b3a40;color:#f0c9cd;border-radius:10px;padding:8px 12px;font:13px/1.4 system-ui,"Noto Sans KR",sans-serif;box-shadow:0 4px 20px #0006}
.rk-del{border:1px solid #8a3d45;background:#3a2226;color:#ffd5d9!important;border-radius:8px;padding:4px 10px;font:13px/1.4 system-ui,"Noto Sans KR",sans-serif;cursor:pointer;text-decoration:none!important;white-space:nowrap}
.rk-del:hover,.rk-del:focus-visible{background:#5a2a30}
.rk-off{background:none;border:0;color:#c79aa0;font:inherit;cursor:pointer;text-decoration:underline}
.item{position:relative}.item>.rk-del{position:absolute;right:0;top:20px;font-size:12px;opacity:.55}.item:hover>.rk-del,.item>.rk-del:focus-visible{opacity:1}`;
  document.head.append(css);

  const link = (src, title, text) => {
    const a = document.createElement("a");
    a.className = "rk-del"; a.textContent = text; a.target = "_blank"; a.rel = "noopener";
    a.href = `${REPO}/delete/${BRANCH}/${src}`;
    a.title = `GitHub에서 ${src} 삭제 화면 열기 — '${title}'`;
    a.onclick = e => {
      if (!confirm(`'${title}' 글을 삭제할까요?\n\nGitHub 삭제 화면(${src})이 새 탭으로 열립니다.\n거기서 'Commit changes'를 눌러야 실제로 지워지고, 1~2분 뒤 사이트에 반영됩니다.`)) e.preventDefault();
    };
    return a;
  };

  const badge = document.createElement("div");
  badge.className = "rk-badge";
  badge.innerHTML = '<span>관리 모드</span>';
  const off = document.createElement("button");
  off.className = "rk-off"; off.textContent = "끄기";
  off.onclick = () => { try { localStorage.removeItem("rk-admin"); } catch {} location.href = location.pathname; };

  const m = location.pathname.match(/\/articles\/([a-z0-9][a-z0-9-]*)\.html$/);
  if (m) {
    // Markdown에서 만든 글은 템플릿의 .art-head가 있다 → 원본은 content/<slug>.md
    const src = document.querySelector(".art-head") ? `content/${m[1]}.md` : `articles/${m[1]}.html`;
    const h1 = document.querySelector("h1");
    badge.append(link(src, h1 ? h1.textContent.trim() : m[1], "이 글 삭제"));
  }
  document.querySelectorAll(".item[data-src]").forEach(card => {
    const h = card.querySelector("h3");
    card.append(link(card.dataset.src, h ? h.textContent.trim() : card.dataset.src, "삭제"));
  });
  badge.append(off);
  document.body.append(badge);
})();
