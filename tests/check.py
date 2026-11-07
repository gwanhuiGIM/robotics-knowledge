#!/usr/bin/env python3
"""빌드 자가검증. 사용: python tests/check.py [--site _site]

1) 렌더러 단위 시험 — tests/fixtures/visual-sample.md를 렌더해 수식·Mermaid·Alert·표·sanitize를 확인
2) 사이트 시험(--site) — 홈 카드 href가 모두 존재, 카드 수 = 기존 카드 + 생성 글, 생성 글에 reader 자산 포함
실패하면 종료 코드 1. 배포를 막지 않으려면 workflow에서 continue-on-error로 둔다.
"""
import argparse
import re
import sys
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def unit():
    site = build.load_site()
    md = build.make_md()
    tpl = Template((ROOT / "tools/templates/article.html").read_text(encoding="utf-8"))
    slug, page, card, _ = build.render_article(ROOT / "tests/fixtures/visual-sample.md", md, site, tpl)
    body = page.split('<div class="art-body">', 1)[1].split('<footer class="art-foot">', 1)[0]
    n_inline = body.count('class="math-inline"')
    check(n_inline == 3, f"인라인 수식 3개 기대(v=ωr, x|y, E=mc²): {n_inline}")
    check(body.count('class="math-display"') == 2, "블록 수식 2개($$, \\[) 기대")
    check(r"\omega r" in body, "TeX 역슬래시 보존(\\omega)")
    check("x|y" in body, "표 안 \\| 수식이 칸을 자르지 않아야 함")
    check("$100" in body and "$HOME" in body and "$(find pkg)" in body, "$100·$HOME·$(..)이 수식으로 오인되면 안 됨")
    check('<pre class="mermaid-src"><code class="language-mermaid">flowchart LR\n  A[센서] --&gt; B[인식]\n</code></pre>' in body,
          "Mermaid 원문 보존")
    check('class="language-python"' in body, "코드 언어 class 보존")
    check('class="alert alert-note"' in body and "[!NOTE]" not in body, "Alert 변환")
    check("<strong>굵게</strong>" in body, "굵게")
    check("<script" not in body and "onclick" not in body and 'href="javascript:' not in body,
          "sanitize: script·onclick·javascript: 링크 제거")
    check('class="visual-card"' in body, "카드 class 보존")
    check('<span class="badge badge-color-success">수용</span>' in body, "<badge> 변환")
    check('<span class="tx tx-color-secondary tx-size-xs">' in body, "<text> 변환")
    check('href="https://example.com"' in body, "정상 링크 유지")
    check("katex.min.js" in page and "mermaid.min.js" in page and "reader.js" in page and "article.js" in page, "필요 스크립트 포함")
    check("JD 핵심 문장" in page and "요약 · 게시 시 작성" in page, "요약·JD 상자")
    check('mode-new_answer' in card and 'data-category="Systems"' in card, "카드 라벨")


def site_check(out):
    index = (out / "index.html").read_text(encoding="utf-8")
    hrefs = re.findall(r'<a class="article"[^>]*href="([^"]+)"', index)
    legacy = len(build.yaml.safe_load((ROOT / "tools/legacy_cards.yml").read_text(encoding="utf-8"))["cards"])
    content = len(list((ROOT / "content").glob("*.md")))
    check(len(hrefs) == legacy + content, f"카드 수 {len(hrefs)} != 기존 {legacy} + 생성 {content}")
    check(len(hrefs) == len(set(hrefs)), "중복 카드")
    for h in hrefs:
        check((out / h).is_file(), f"카드 링크 대상 없음: {h}")
    for md in (ROOT / "content").glob("*.md"):
        p = out / "articles" / f"{md.stem}.html"
        if p.is_file():
            t = p.read_text(encoding="utf-8")
            check("../assets/reader.js" in t and "../assets/reader.css" in t, f"reader 자산 누락: {p.name}")
            for src in re.findall(r'<img [^>]*src="([^"]+)"', t):
                if not src.startswith("http"):
                    check((p.parent / src).resolve().is_file(), f"이미지 없음: {p.name} → {src}")
    for bad in ("docs", "AGENTS.md", "content", "tools", "connector-write-test.txt"):
        check(not (out / bad).exists(), f"배포 제외 대상이 포함됨: {bad}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site")
    a = ap.parse_args()
    unit()
    if a.site:
        site_check((ROOT / a.site).resolve())
    for f in fails:
        print("FAIL:", f)
    print("PASS" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
