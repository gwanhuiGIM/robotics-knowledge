#!/usr/bin/env python3
"""로컬 미리보기 + 글 삭제(관리) 서버. 공개 사이트에는 영향이 없다.

사용: python tools/preview.py [--port 8000]
  1) _preview/에 사이트를 빌드하고 http://127.0.0.1:<port>/ 에서 보여 준다(이 PC에서만 접속 가능).
  2) 보내는 HTML에만 관리 스크립트를 끼워 넣어 홈 카드·글 화면에 '삭제' 버튼을 보인다.
     빌드 결과(_site)와 GitHub Pages에는 버튼이 없다.
  3) 삭제하면 파일을 _trash/<시각>-<slug>/로 옮기고(지우지 않음) 다시 빌드한다.
     화면의 '되돌리기'나 `python tools/preview.py --restore <id>`로 복구한다.
  4) 공개 사이트 반영은 사용자가 커밋·push한 뒤다. 서버는 git 조작을 하지 않는다.
"""
import argparse
import json
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

import build

ROOT = build.ROOT
OUT = ROOT / "_preview"
TRASH = ROOT / "_trash"
LEGACY = ROOT / "tools" / "legacy_cards.yml"
ADMIN_DIR = Path(__file__).resolve().parent / "preview_admin"
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
TOKEN = secrets.token_urlsafe(24)  # 실행마다 새로 만든다 — 다른 웹사이트가 이 서버로 요청을 보내도 거부


def rebuild():
    build.build(OUT)


# ---------- 글 하나가 차지하는 파일 ----------
def legacy_cards_text():
    return LEGACY.read_text(encoding="utf-8")


def legacy_block(text, slug):
    """legacy_cards.yml에서 '  - slug: <slug>'로 시작하는 항목의 (시작, 끝) 문자 위치와 다음 항목 slug."""
    starts = [m for m in re.finditer(r"^  - slug: (\S+)\n", text, re.M)]
    for i, m in enumerate(starts):
        if m.group(1) == slug:
            end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
            nxt = starts[i + 1].group(1) if i + 1 < len(starts) else None
            return m.start(), end, nxt
    return None


def describe(slug):
    """slug의 제목·대상 파일·미커밋 여부. 없으면 None."""
    md, html_ = ROOT / "content" / f"{slug}.md", ROOT / "articles" / f"{slug}.html"
    files, title, legacy = [], slug, False
    if md.exists():
        files.append(md)
        meta = yaml.safe_load(md.read_text(encoding="utf-8").split("---", 2)[1]) or {}
        title = meta.get("title", slug)
    elif html_.exists():
        files.append(html_)
        for c in yaml.safe_load(legacy_cards_text())["cards"]:
            if c["slug"] == slug:
                title, legacy = c["title"], True
    else:
        return None
    img = ROOT / "assets" / "img" / slug
    if img.is_dir():
        files.append(img)
    rels = [str(p.relative_to(ROOT)) for p in files] + (["tools/legacy_cards.yml (이 글 항목만)"] if legacy else [])
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", *[str(p) for p in files]],
                           capture_output=True, text=True).stdout.strip()
    return {"slug": slug, "title": title, "files": files, "rels": rels, "legacy": legacy, "dirty": bool(dirty)}


# ---------- 삭제 · 복구 ----------
def delete(slug):
    d = describe(slug)
    if not d:
        raise ValueError(f"글이 없습니다: {slug}")
    tid = time.strftime("%Y%m%d-%H%M%S") + "-" + slug
    box = TRASH / tid
    box.mkdir(parents=True)
    manifest = {"id": tid, "slug": slug, "title": d["title"], "files": [], "legacy": None}
    for p in d["files"]:
        rel = p.relative_to(ROOT)
        (box / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(box / rel))
        manifest["files"].append(str(rel))
    if d["legacy"]:
        text = legacy_cards_text()
        s, e, nxt = legacy_block(text, slug)
        manifest["legacy"] = {"block": text[s:e], "before": nxt}
        LEGACY.write_text(text[:s] + text[e:], encoding="utf-8")
    (box / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    git_paths = [f for f in manifest["files"]] + (["tools/legacy_cards.yml"] if d["legacy"] else [])
    msg = f"content: 글 삭제 — {d['title']} ({slug})"
    manifest["commit"] = f"git add -- {' '.join(git_paths)} && git commit -m {shlex.quote(msg)}"
    return manifest


def restore(tid):
    if not re.fullmatch(r"\d{8}-\d{6}-[a-z0-9][a-z0-9-]*", tid):
        raise ValueError("잘못된 휴지통 id")
    box = TRASH / tid
    m = json.loads((box / "manifest.json").read_text(encoding="utf-8"))
    for rel in m["files"]:
        if (ROOT / rel).exists():
            raise ValueError(f"같은 이름이 이미 있어 복구를 멈췄습니다: {rel}")
    for rel in m["files"]:
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(box / rel), str(ROOT / rel))
    if m["legacy"]:
        text = legacy_cards_text()
        pos = legacy_block(text, m["legacy"]["before"]) if m["legacy"]["before"] else None
        at = pos[0] if pos else len(text)  # 원래 다음 항목 앞, 없으면 맨 끝
        LEGACY.write_text(text[:at] + m["legacy"]["block"] + text[at:], encoding="utf-8")
    shutil.rmtree(box)
    return m


# ---------- HTTP ----------
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path.startswith("/__admin/"):
            name = path.removeprefix("/__admin/")
            if name == "info":
                slug = self.path.partition("slug=")[2].split("&")[0]
                d = describe(slug) if SLUG.fullmatch(slug) else None
                return self.send_json(200 if d else 404, {k: v for k, v in (d or {}).items() if k != "files"})
            f = ADMIN_DIR / name
            if name in ("admin.js", "admin.css") and f.exists():
                body = f.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/javascript" if name.endswith(".js") else "text/css")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                return self.wfile.write(body)
            return self.send_error(404)
        local = Path(self.translate_path(self.path))
        if local.is_dir():
            local = local / "index.html"
        if local.suffix == ".html" and local.exists():
            inject = (f'<link rel="stylesheet" href="/__admin/admin.css"><script>window.RK_ADMIN_TOKEN="{TOKEN}"</script>'
                      '<script defer src="/__admin/admin.js"></script>')
            body = local.read_text(encoding="utf-8").replace("</body>", inject + "</body>", 1).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        return super().do_GET()

    def do_POST(self):
        # 이 PC의 이 서버 페이지에서 보낸 요청만 받는다(토큰 + Origin 확인).
        origin = self.headers.get("Origin", "")
        host = self.headers.get("Host", "")
        if self.headers.get("X-Admin-Token") != TOKEN or origin not in (f"http://{host}", ""):
            return self.send_json(403, {"error": "권한 없음(로컬 미리보기 페이지에서만 삭제 가능)"})
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/__admin/delete" and SLUG.fullmatch(data.get("slug", "")):
                m = delete(data["slug"])
            elif self.path == "/__admin/restore":
                m = restore(data.get("id", ""))
            else:
                return self.send_json(400, {"error": "잘못된 요청"})
            rebuild()
            return self.send_json(200, m)
        except Exception as e:
            return self.send_json(400, {"error": str(e)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--restore", metavar="ID", help="_trash/<ID>를 복구하고 끝낸다")
    a = ap.parse_args()
    if a.restore:
        m = restore(a.restore)
        print(f"복구함: {m['title']} ({', '.join(m['files'])})")
        return
    rebuild()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), partial(Handler, directory=str(OUT)))
    print(f"로컬 미리보기: http://127.0.0.1:{a.port}/  (삭제 버튼은 이 주소에서만 보입니다, Ctrl+C로 종료)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())
