#!/usr/bin/env python3
"""빌드 자가검증. 사용: python tests/check.py [--site _site]

1) 렌더러 단위 시험 — tests/fixtures/visual-sample.md를 렌더해 수식·Mermaid·Alert·표·sanitize를 확인,
   tests/fixtures/layout-sample.md로 ChatGPT 레이아웃 태그(반복·속성 검증·sanitize·원문 표시 대체)를 확인,
   tests/fixtures/widget-sample.md로 ChatGPT 화면 위젯(Entity·Cite·AsyncImage·Chart)을 확인
   assets/ 아래 SVG 안전 검사(<script>·on* 속성·foreignObject·외부 href 거부)
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
    cat, has_q, item = card
    check(cat == "ROS 2" and 'mode-new_answer' in item and 'data-category="ROS 2"' in item, "홈 항목 라벨·분야")
    check(item.count("<a ") == 1 and '<a class="item-link"' in item and "<details" not in item.split("</a>")[0],
          "링크는 제목에만(<a> 안에 <details> 금지)")
    # [!PROMPT] → 홈 질문: 순서·여러 문단·escape, 코드 블록 안 예시와 NOTE는 제외
    _, _, (_, has_q, item), _ = build.render_article(ROOT / "tests/fixtures/prompt-sample.md", md, site, tpl)
    qs = re.findall(r'<blockquote class="q"><p[^>]*>(.*?)</p></blockquote>', item, re.S)
    check(has_q and qs == ["첫 질문 &amp; &lt;꺾쇠&gt;", "두 번째 질문 첫 문단\n\n두 번째 질문 둘째 문단",
                           "이 코드 설명해줘\n\nprint(1)"], f"질문 추출(질문 안 코드 포함): {qs}")
    check("질문 2개 더 보기" in item and "코드 블록 안" not in item and "참고는" not in item, "질문 추출 범위")
    try:
        build.validate({"title": "t", "category": "Systems", "content_mode": "new_answer",
                        "published": "2026-11-14", "summary": "s"}, site)
        check(False, "옛 분야 Systems가 통과하면 안 됨")
    except build.ArticleError as e:
        check("더 이상 쓰지 않음" in str(e), f"옛 분야 안내 문구: {e}")


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
    hrefs = re.findall(r'<a class="item-link" href="([^"]+)"', index)
    items = re.findall(r'<article class="item" data-category="([^"]+)".*?</article>', index, re.S)
    check(len(items) == len(hrefs), f"항목 {len(items)} != 링크 {len(hrefs)}")
    # 분야 칩 숫자 = 그 분야 실제 항목 수, 0개 분야 칩 없음. 항목은 모두 #list 한 목록 안(분야 섹션 없음, 2026-11-17)
    site = build.load_site()
    for key in site["categories"]:
        n = items.count(key)
        k = re.escape(build.html.escape(key))
        chip = re.search(r'data-filter="%s">[^<]*<b>(\d+)</b>' % k, index)
        if n == 0:
            check(chip is None, f"글 0개 분야가 홈에 나옴: {key}")
        else:
            check(chip is not None and int(chip.group(1)) == n, f"칩 숫자 불일치: {key}")
    lst = re.search(r'<div class="list" id="list">(.*?)<p id="empty"', index, re.S)
    check(lst is not None and lst.group(1).count('<article class="item"') == len(items), "목록 밖 항목 있음")
    dates = re.findall(r'<article class="item".*?<time>([^<]+)</time>', index, re.S)
    check(dates == sorted(dates, reverse=True), "홈 목록이 최신순이 아님")
    total = re.search(r'data-filter="all">[^<]*<b>(\d+)</b>', index)
    check(total is not None and int(total.group(1)) == len(items), "전체 칩 숫자 불일치")

    # GitHub에서 HTML을 지운 옛 글은 빌드가 홈에서 뺀다 — 검사도 HTML이 남은 항목만 센다.
    live_legacy = [c for c in build.yaml.safe_load((ROOT / "tools/legacy_cards.yml").read_text(encoding="utf-8"))["cards"]
                   if (ROOT / "articles" / f"{c['slug']}.html").exists()]
    # 질문이 그 글의 항목 안, 화면의 질문 상자에 순서대로 그대로 있는지(data-q에만 있거나 다른 글로 옮겨지면 실패)
    def shown_in(slug):
        for a in re.findall(r'<article class="item".*?</article>', index, re.S):
            if f'href="articles/{slug}.html"' in a:
                return [build.html.unescape(q) for q in re.findall(r'<blockquote class="q"><p[^>]*>(.*?)</p>', a, re.S)], a
        return None, ""
    for c in live_legacy:
        want = [q if isinstance(q, str) else q["text"] for q in c.get("questions") or []]
        got, a = shown_in(c["slug"])
        check(got == want, f"홈 질문 불일치: {c['slug']}")
        for q in c.get("questions") or []:
            if not isinstance(q, str) and q.get("note"):
                check(build.html.escape(q["note"]) in a, f"질문 단서 표시 없음: {c['slug']}")
        if not want:
            check("q-none" in a, f"질문 없음 표시 없음: {c['slug']}")
    md = build.make_md()
    for p in (ROOT / "content").glob("*.md"):
        env = {}
        md.render(build.split_front_matter(p.read_text(encoding="utf-8"), p)[1], env)
        got, _ = shown_in(p.stem)
        check(got == (env.get("prompts") or []), f"홈 질문 불일치(content): {p.stem}")
    legacy = len(live_legacy)
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


# 커밋된 SVG 안전 검사(계획 2026-11-18-link-import-simplify B-5). 공유 페이지에서 옮긴 SVG는 <img>로 쓰여 스크립트가
# 돌지 않지만, 파일을 직접 열면 실행될 수 있어 저장소에 두지 않는다. 같은 기준을 로컬 추출 도구(extract.js)도 쓴다.
SVG_BAD = [  # 2026-11-19 교차검증: 이름공간 script·<set>·숫자 엔티티·<style> @import 우회를 막으려 허용 쪽으로 좁힘
    (re.compile(r"<\s*(?:[\w-]+:)?(?:script|foreignObject|iframe|embed|object|style|set|animate\w*|image|handler|listener)\b", re.I), "위험 요소"),
    (re.compile(r"\son[a-z]+\s*=", re.I), "on* 속성"),
    (re.compile(r"""href\s*=\s*["']\s*(?!#)""", re.I), "내부(#) 아닌 href"),
    (re.compile(r"&#"), "숫자 엔티티"),
    (re.compile(r"""url\(\s*["']?\s*(?!#)""", re.I), "내부(#) 아닌 url()"),
    (re.compile(r"javascript:", re.I), "javascript:"),
]


def svg_problems(text):
    return [name for rx, name in SVG_BAD if rx.search(text)]


def svg_check():
    # 검사기가 실제로 잡는지 먼저 본다(변이 4종 + 정상 1종)
    ok = ('<svg xmlns="http://www.w3.org/2000/svg" style="color:red"><rect x="1" fill="url(#g)"/>'
          '<use href="#a"/><text font-family="&quot;Segoe UI&quot;">a</text></svg>')
    check(svg_problems(ok) == [], "SVG 검사 오탐: 정상 SVG")
    for bad in ('<svg><script>alert(1)</script></svg>', '<svg onload="x()"></svg>',
                '<svg><foreignObject></foreignObject></svg>', '<svg><image href="https://e.x/a.png"/></svg>',
                '<svg><s:script>a</s:script></svg>', '<svg><set attributeName="href" to="javascript:x"/></svg>',
                '<svg><a href="&#106;avascript:x">a</a></svg>', '<svg><style>@import url(https://e.x/a.css)</style></svg>',
                '<svg><rect fill="url(http://e.x/a)"/></svg>'):
        check(svg_problems(bad), f"SVG 검사 놓침: {bad}")
    for p in sorted((ROOT / "assets").rglob("*.svg")):
        found = svg_problems(p.read_text(encoding="utf-8", errors="replace"))
        check(not found, f"SVG 안전 검사 실패: {p.relative_to(ROOT)} → {', '.join(found)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site")
    a = ap.parse_args()
    unit()
    layout_unit()
    widget_unit()
    svg_check()
    if a.site:
        site_check((ROOT / a.site).resolve())
    for f in fails:
        print("FAIL:", f)
    print("PASS" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
