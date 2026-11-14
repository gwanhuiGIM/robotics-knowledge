#!/usr/bin/env python3
"""빌드 자가검증. 사용: python tests/check.py [--site _site]

1) 렌더러 단위 시험 — tests/fixtures/visual-sample.md를 렌더해 수식·Mermaid·Alert·표·sanitize를 확인,
   tests/fixtures/layout-sample.md로 ChatGPT 레이아웃 태그(반복·속성 검증·sanitize·원문 표시 대체)를 확인,
   tests/fixtures/widget-sample.md로 ChatGPT 화면 위젯(Entity·Cite·AsyncImage·Chart)을 확인
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


def layout_unit():
    """ChatGPT 레이아웃 태그(tools/layout_tags.py) — tests/fixtures/layout-sample.md."""
    site = build.load_site()
    md = build.make_md()
    tpl = Template((ROOT / "tools/templates/article.html").read_text(encoding="utf-8"))
    _, page, _, _ = build.render_article(ROOT / "tests/fixtures/layout-sample.md", md, site, tpl)
    body = page.split('<div class="art-body">', 1)[1].split('<footer class="art-foot">', 1)[0]
    check(body.count('class="lt-root"') == 5, "정상 레이아웃 블록 5개")
    check(body.count("data-lucide=") == 3 and all(f'data-lucide="{n}"' in body for n in ("hammer", "check-check", "scan-search")),
          "{#each} 3회 반복 + 아이콘 이름 치환")
    check(all(f'<span class="tx tx-size-xs">{n}</span>' in body for n in ("빌드", "테스트", "코드 검사")), "{item.name} 글자 치환")
    check('class="lt-grid lt-gap-2 lt-cols-3"' in body and 'class="lt-row lt-al-center lt-jc-between"' in body, "grid·row 속성")
    check("<strong>CI 단계</strong>" in body and '<span class="badge">Integration</span>' in body, "태그 사이 Markdown·badge")
    check('style="background-color:rgba(30,110,200,0.07);border:1px solid;border-color:rgba(30,110,200,0.2);width:100px;flex:none"' in body,
          "rgba 배경·테두리·폭")
    check("position" not in body and "red;" not in body, "검증 안 된 style 값은 버림")
    check("<script" not in body and "onerror" not in body and 'href="javascript:' not in body, "레이아웃 안 sanitize")
    check('<div class="lt-unknown"><p>모르는 태그 안 글자</p>' in body, "모르는 태그는 글자 표시")
    check('<div class="lt-writing"><p>예시 문장 <strong>강조</strong></p>' in body, "WritingBlock")
    check('<span class="math-inline">v=\\omega r</span>' in body and "katex.min.js" in page, "레이아웃 안 수식")
    check('<a href="https://example.com/doc" rel="noopener noreferrer">예시 문서</a>' in body, "문단 안 <Link>")
    check("&lt;box gap={3}&gt;코드 블록 안 태그는 그대로" in body, "코드 블록 안 태그는 변환하지 않음")
    check('class="lt-fallback"' in body and "닫히지 않은 블록 원문" in body, "닫히지 않은 블록은 원문 표시")
    check("<h2>다음 절</h2>" in body and "<p>닫히지 않은 블록 뒤 문단도 살아 있어야 함</p>" in body, "닫히지 않은 블록이 뒤 내용을 삼키지 않음")
    check("@@LAYOUT" not in body, "자리표시 잔존 없음")
    check('<div class="lt-box"><p>잘못된 속성 타입</p>' in body, "배열·객체 속성 값은 버리고 블록은 렌더")
    check('<code class="language-html">&lt;icon name="hammer"/&gt;' in body, "레이아웃 안 코드 fence는 글자")
    check("&lt;box&gt;목록 안 코드 블록&lt;/box&gt;" in body, "목록 안 코드 fence는 변환하지 않음")
    check('<code>&lt;Link url="https://example.com/raw" title="코드 안 링크"/&gt;</code>' in body, "인라인 코드 안 <Link>는 그대로")
    check("<h2>상자 안 제목</h2>\n<p>상자 안 내용</p>" in body, "닫힌 블록 안 제목에서 블록이 끊기지 않음")
    check('<span class="tx">a,b:c</span>' in body, "{#each} 문자열 안 콤마·콜론")
    check("<p>후속 일반 문단도 살아 있어야 함</p>" in body, "닫히지 않은 블록이 뒤 일반 문단을 삼키지 않음")
    check("lucide.min.js" in page, "아이콘 스크립트 포함")


# 태그가 렌더되지 않고 글자로 새어 나온 흔적(코드·수식 밖): <Name attr="…"·attr={…}> 또는 <Name/>
# 속성 값이 따옴표·중괄호로 시작할 때만 잡는다 — 부등식(a<b x=1)을 오탐하지 않게.
LEAK = re.compile(r"&lt;[A-Za-z][\w-]*(?:\s+[A-Za-z_][\w-]*=(?:\{|&quot;|\"|')|\s*/&gt;)")
CODE = re.compile(r"<pre[\s>].*?</pre>|<code[\s>].*?</code>|<span class=\"math-inline\">.*?</span>|<div class=\"math-display\">.*?</div>", re.S)


def leaks(body):
    """코드·수식 밖에 글자로 남은 태그, 짝을 잃은 굵게 표시(**) 목록.
    못 잡는 것: 블록 밖의 따옴표 속성 태그(<Foo value="…"/>)는 sanitize가 경고 없이 지운다."""
    text = CODE.sub("", body)
    return LEAK.findall(text) + re.findall(r"<p>\*\*</p>", text)


def widget_unit():
    """ChatGPT 화면 위젯 — tests/fixtures/widget-sample.md."""
    site = build.load_site()
    md = build.make_md()
    tpl = Template((ROOT / "tools/templates/article.html").read_text(encoding="utf-8"))
    _, page, _, _ = build.render_article(ROOT / "tests/fixtures/widget-sample.md", md, site, tpl)
    body = page.split('<div class="art-body">', 1)[1].split('<footer class="art-foot">', 1)[0]
    check(not leaks(body), f"위젯 태그가 글자로 남음: {leaks(body)[:3]}")
    check("turn" not in CODE.sub("", body), "Cite 출처 id는 지움")
    check("<strong>Anvil Robotics OpenYAM</strong>" in body, "**<Entity/>** → 굵은 value")
    check("<p>들여쓴 설명 문단입니다.</p>" in body and "<pre><code>들여쓴" not in body, "Entity 뒤 들여쓴 문단이 코드 블록이 되지 않음")
    check("블록 밖 개체 Out*Side Robot 끝." in body, "블록 밖 Entity → value(Markdown 특수문자 그대로)")
    check("<p>블록 밖 문단 <strong>굵게</strong>입니다.</p>" in body, "블록 밖 Cite 삭제")
    check("AsyncImage" not in CODE.sub("", body) and "robot a" not in body, "AsyncImage·AsyncImageGroup 삭제")
    check('<th>1세대</th><td>22.6</td>' in body and '<th>Sage</th><td>340.3</td>' in body and "개입 간격 (초)" in body,
          "Chart → 데이터 표")
    check("<figcaption>자료: 예시 &lt;b&gt;</figcaption>" in body, "Chart footer 이스케이프")
    check('<div class="lt-caption">캡션 글자</div>' in body, "caption 안 Cite 삭제")
    check('<code>&lt;Cite ref="code"/&gt;</code>' in body, "인라인 코드 안 위젯은 그대로")
    check('class="lt-unknown"' not in body, "위젯이 모르는 태그 상자로 떨어지지 않음")
    check("Lt&amp;Gt &lt;b&gt;" in body, "Entity value의 &·< 는 한 번만 이스케이프")
    check(not leaks("<p>a&lt;b x=1 이고 c&lt;d</p><span class=\"math-inline\">a&lt;b c=d</span>"), "부등식·수식은 누출로 보지 않음")


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
        # 총수만 맞는 거짓 PASS를 막는다: content 글마다 페이지와 홈 카드가 각각 있어야 한다.
        check(p.is_file(), f"생성 글 없음(빌드에서 제외됐을 수 있음): {p.name}")
        check(f"articles/{md.stem}.html" in hrefs, f"홈 카드 없음: {md.stem}")
        if p.is_file():
            t = p.read_text(encoding="utf-8")
            check("../assets/reader.js" in t and "../assets/reader.css" in t, f"reader 자산 누락: {p.name}")
            found = leaks(t.split('<div class="art-body">', 1)[-1])
            check(not found, f"태그가 글자로 남음: {p.name} → {found[:3]}")
            check('class="lt-unknown"' not in t, f"모르는 레이아웃 태그가 있음(빌드 ::warning 확인): {p.name}")
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
    layout_unit()
    widget_unit()
    if a.site:
        site_check((ROOT / a.site).resolve())
    for f in fails:
        print("FAIL:", f)
    print("PASS" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
