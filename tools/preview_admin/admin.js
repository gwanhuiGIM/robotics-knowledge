// 로컬 미리보기(tools/preview.py)에서만 끼워 넣는 관리 UI. 공개 사이트에는 없다.
(() => {
  const token = window.RK_ADMIN_TOKEN;
  const slugOf = href => (href.match(/articles\/([a-z0-9][a-z0-9-]*)\.html/) || [])[1];
  const el = (tag, attrs = {}, text) => { const e = document.createElement(tag); Object.assign(e, attrs); if (text) e.textContent = text; return e; };
  const post = (url, data) => fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-Admin-Token": token }, body: JSON.stringify(data) })
    .then(r => r.json().then(j => (r.ok ? j : Promise.reject(new Error(j.error || r.status)))));
  const homeUrl = () => (location.pathname.includes("/articles/") ? "../index.html" : "index.html");

  // 1) 삭제 확인 창 — 무엇이 지워지는지 먼저 보여 준다.
  async function confirmDelete(slug) {
    const info = await fetch(`/__admin/info?slug=${slug}`).then(r => r.json());
    if (!info.slug) return alert("글 정보를 찾지 못했습니다: " + slug);
    const back = el("div", { className: "rk-back" });
    const box = el("div", { className: "rk-modal", role: "dialog", ariaModal: "true" });
    box.append(el("h2", {}, "이 글을 삭제할까요?"), el("p", { className: "t" }, info.title),
      el("p", { className: "note" }, "아래 파일을 _trash/ 폴더로 옮기고 미리보기를 다시 빌드합니다."));
    const ul = el("ul"); info.rels.forEach(f => ul.append(el("li", {}, f))); box.append(ul);
    if (info.dirty) box.append(el("p", { className: "note warn" }, "⚠ 커밋하지 않은 수정이 있는 파일입니다. 휴지통에는 남지만 git으로는 되돌릴 수 없습니다."));
    box.append(el("p", { className: "note" }, "삭제 직후 '되돌리기'로 복구할 수 있고, 공개 사이트에는 커밋·push 전까지 그대로 보입니다."));
    const cancel = el("button", {}, "취소"), go = el("button", { className: "rk-go" }, "삭제");
    const row = el("div", { className: "rk-row" }); row.append(cancel, go); box.append(row);
    back.append(box); document.body.append(back); cancel.focus();
    const close = () => back.remove();
    cancel.onclick = close;
    back.onclick = e => { if (e.target === back) close(); };
    back.onkeydown = e => { if (e.key === "Escape") close(); };
    go.onclick = async () => {
      go.disabled = cancel.disabled = true; go.textContent = "삭제 중…";
      try {
        const m = await post("/__admin/delete", { slug });
        sessionStorage.setItem("rk-last", JSON.stringify(m));
        location.href = homeUrl();
      } catch (e) { alert("삭제 실패: " + e.message); close(); }
    };
  }

  // 2) 삭제 뒤 홈에 결과·되돌리기·커밋 명령을 보여 준다.
  function toast() {
    let m; try { m = JSON.parse(sessionStorage.getItem("rk-last")); } catch { return; }
    if (!m) return;
    const t = el("div", { className: "rk-toast", role: "status" });
    t.append(el("div", {}, `‘${m.title}’ 삭제됨 — 로컬 파일만 바뀌었습니다. 공개 사이트 반영은 커밋·push 뒤.`));
    const row = el("div", { className: "row" });
    const undo = el("button", {}, "되돌리기"), copy = el("button", {}, "커밋 명령 복사"), ok = el("button", {}, "닫기");
    row.append(undo, copy, ok); t.append(row, el("code", {}, m.commit)); document.body.append(t);
    const done = () => { sessionStorage.removeItem("rk-last"); t.remove(); };
    ok.onclick = done;
    copy.onclick = () => navigator.clipboard.writeText(m.commit).then(() => (copy.textContent = "복사됨"));
    undo.onclick = async () => {
      undo.disabled = true;
      try { await post("/__admin/restore", { id: m.id }); done(); location.reload(); }
      catch (e) { alert("복구 실패: " + e.message + "\n수동 복구: python tools/preview.py --restore " + m.id); undo.disabled = false; }
    };
  }

  // 3) 버튼 배치 — 홈은 카드마다, 글 화면은 왼쪽 아래 배지.
  const badge = el("div", { className: "rk-badge" });
  badge.append(el("span", {}, "로컬 관리 모드"));
  const here = slugOf(location.pathname);
  if (here) {
    const b = el("button", { className: "rk-del" }, "이 글 삭제"); b.onclick = () => confirmDelete(here); badge.append(b);
  }
  document.body.append(badge);
  document.querySelectorAll(".item").forEach(card => {
    const a = card.querySelector('a[href*="articles/"]'); const slug = a && slugOf(a.getAttribute("href"));
    if (!slug) return;
    const b = el("button", { className: "rk-del", title: "이 글 삭제" }, "삭제"); b.onclick = () => confirmDelete(slug); card.append(b);
  });
  toast();
})();
