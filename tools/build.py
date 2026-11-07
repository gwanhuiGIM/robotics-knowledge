#!/usr/bin/env python3
"""Robotics Knowledge Lab 정적 사이트 빌드.

content/*.md(front matter + Markdown) -> articles/<slug>.html, 홈 index.html 카드 목록 생성.
기존(legacy) HTML 글은 그대로 복사하고 홈 카드만 tools/legacy_cards.yml에서 가져온다.

사용: python tools/build.py --out _site
글 하나가 실패하면 그 글만 빼고 경고(::warning)를 남긴 뒤 나머지를 빌드한다.
"""
import argparse
import html
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from string import Template

import nh3
import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.texmath import texmath_plugin

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

# 배포에서 빼는 최상위 항목(제외 목록 방식 — 웹 에이전트가 새 폴더를 만들어도 조용히 빠지지 않게).
EXCLUDE_TOP = {".git", ".github", ".gitignore", "docs", "content", "tools", "tests", "AGENTS.md", "README.md"}
EXCLUDE_SUFFIX = {".txt", ".md", ".py", ".yml", ".yaml"}

ALERT_TYPES = {"NOTE": "참고", "TIP": "팁", "IMPORTANT": "중요", "WARNING": "주의", "CAUTION": "경고", "PROMPT": "사용자 질문"}
ALERT_RE = re.compile(r"^\[!(" + "|".join(ALERT_TYPES) + r")\][ \t]*(?:\n|$)")

KATEX = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css" '
         'integrity="sha384-5TcZemv2l/9On385z///+d7MSYlvIEw9FuZTIdZ14vJLqWphw7e7ZPuOiCHJcFCP" crossorigin="anonymous">\n')  # pragma: allowlist secret — 공개 CDN 파일의 SRI 해시
KATEX_JS = ('<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js" '
            'integrity="sha384-cMkvdD8LoxVzGF/RPUKAcvmm49FQ0oxwDF3BGKtDXcEc+T1b2N+teh/OJfpU0jr6" crossorigin="anonymous"></script>\n')  # pragma: allowlist secret
MERMAID_JS = ('<script defer src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js" '
              'integrity="sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I" crossorigin="anonymous"></script>\n')  # pragma: allowlist secret
ARTICLE_JS = '<script defer src="../assets/article.js"></script>\n'

ALLOWED_TAGS = {
    "a", "b", "blockquote", "br", "code", "del", "details", "div", "em", "figcaption", "figure",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "kbd", "li", "ol", "p", "pre", "s",
    "small", "span", "strong", "sub", "summary", "sup", "table", "tbody", "td", "tfoot", "th",
    "thead", "tr", "ul",
}
ALLOWED_ATTRS = {
    "*": {"class"},
    "a": {"href", "title"},
    "img": {"src", "alt", "title", "width", "height"},
    "th": {"style"}, "td": {"style"},
    "ol": {"start"},
}


class ArticleError(Exception):
    pass


def warn(path, msg):
    # GitHub Actions 주석 형식. 로컬에서도 그대로 읽힌다.
    print(f"::warning file={path}::{msg}", file=sys.stderr)


def load_site():
    return yaml.safe_load((TOOLS / "site.yml").read_text(encoding="utf-8"))


def make_md():
    md = (MarkdownIt("commonmark", {"html": True})
          .enable("table").enable("strikethrough")
          # $100, $HOME 같은 문장을 수식으로 오인하지 않도록 엄격 옵션.
          .use(dollarmath_plugin, allow_space=False, allow_digits=False, allow_labels=False)
          # \( \), \[ \] 구분자 — Markdown 이스케이프로 역슬래시가 지워지기 전에 수식으로 잡는다.
          .use(texmath_plugin, delimiters="brackets"))

    def math_inline(self, tokens, idx, options, env):
        return f'<span class="math-inline">{html.escape(tokens[idx].content)}</span>'

    def math_block(self, tokens, idx, options, env):
        env["has_math"] = True
        return f'<div class="math-display">{html.escape(tokens[idx].content.strip())}</div>\n'

    def math_inline_any(self, tokens, idx, options, env):
        env["has_math"] = True
        return math_inline(self, tokens, idx, options, env)

    for name in ("math_inline", "math_inline_double"):
        md.add_render_rule(name, math_inline_any)
    for name in ("math_block", "math_block_eqno", "math_block_label"):
        md.add_render_rule(name, math_block)

    default_fence = md.renderer.rules["fence"]

    def fence(self, tokens, idx, options, env):
        tok = tokens[idx]
        lang = tok.info.strip().split(" ")[0] if tok.info else ""
        if lang == "mermaid":
            env["has_mermaid"] = True
            # 원문 코드를 그대로 두고 브라우저에서 그림으로 바꾼다. 실패하면 이 코드가 그대로 보인다.
            return f'<pre class="mermaid-src"><code class="language-mermaid">{html.escape(tok.content)}</code></pre>\n'
        return default_fence(tokens, idx, options, env)

    md.add_render_rule("fence", fence)

    def alerts(state):
        toks = state.tokens
        for i, t in enumerate(toks):
            if t.type != "blockquote_open" or i + 2 >= len(toks):
                continue
            inline = toks[i + 2]
            if toks[i + 1].type != "paragraph_open" or inline.type != "inline":
                continue
            m = ALERT_RE.match(inline.content)
            if not m:
                continue
            kind = m.group(1)
            t.attrSet("class", f"alert alert-{kind.lower()}")  # 라벨 글자는 article.css의 ::before
            inline.content = inline.content[m.end():]

    md.core.ruler.before("inline", "alerts", alerts)
    return md


CUSTOM_TAG_RE = re.compile(r"<(text|badge)((?:\s+[a-z-]+=\"[^\"<>]*\")*)\s*>|</(text|badge)\s*>")
ATTR_RE = re.compile(r'([a-z-]+)="([^"<>]*)"')


def convert_custom_tags(s):
    """ChatGPT 답변의 <text color size>, <badge color>를 span으로 바꾼다(코드 블록 안은 이미 escape되어 무관)."""
    def sub(m):
        if m.group(3):
            return "</span>"
        tag = m.group(1)
        classes = ["badge" if tag == "badge" else "tx"]
        for k, v in ATTR_RE.findall(m.group(2) or ""):
            if k in ("color", "size") and re.fullmatch(r"[a-z0-9-]+", v):
                classes.append(f"{'badge' if tag == 'badge' else 'tx'}-{k}-{v}")
        return f'<span class="{" ".join(classes)}">'
    return CUSTOM_TAG_RE.sub(sub, s)


def sanitize(s):
    return nh3.clean(
        s, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS,
        url_schemes={"http", "https", "mailto"},
        filter_style_properties={"text-align"},
        link_rel="noopener noreferrer",
    )


def split_front_matter(text, path):
    if not text.startswith("---\n"):
        raise ArticleError("front matter(--- 로 시작)가 없습니다")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ArticleError("front matter 끝(---)이 없습니다")
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        raise ArticleError("front matter가 key: value 형식이 아닙니다")
    return meta, text[end + 5:]


def as_date(v, field):
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return v
    raise ArticleError(f"{field}는 YYYY-MM-DD 형식이어야 합니다: {v!r}")


def validate(meta, site):
    missing = [f for f in site["required_fields"] if not meta.get(f)]
    if missing:
        raise ArticleError(f"필수 필드 누락: {', '.join(missing)}")
    if meta["category"] not in site["categories"]:
        raise ArticleError(f"category 허용 값 아님: {meta['category']!r} (허용: {list(site['categories'])})")
    if meta["content_mode"] not in site["content_modes"]:
        raise ArticleError(f"content_mode 허용 값 아님: {meta['content_mode']!r} (허용: {list(site['content_modes'])})")
    meta["published"] = as_date(meta["published"], "published")
    if meta.get("updated"):
        meta["updated"] = as_date(meta["updated"], "updated")
    for f in ("tags", "jd"):
        v = meta.get(f) or []
        if isinstance(v, str):
            v = [v]
        if not all(isinstance(x, str) for x in v):
            raise ArticleError(f"{f}는 문자열 목록이어야 합니다")
        meta[f] = v


def render_article(path, md, site, tpl):
    slug = path.stem
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise ArticleError("파일 이름은 소문자·숫자·하이픈만 씁니다(slug)")
    meta, body_md = split_front_matter(path.read_text(encoding="utf-8"), path)
    validate(meta, site)
    env = {}
    body = sanitize(convert_custom_tags(md.render(body_md, env)))
    esc = html.escape
    summary_box = (f'<section class="gen-box"><div class="gen-label">요약 · 게시 시 작성</div>'
                   f'<p>{esc(meta["summary"])}</p></section>\n')
    jd_box = ""
    if meta["jd"]:
        items = "".join(f"<li>{esc(x)}</li>" for x in meta["jd"])
        jd_box = f'<section class="gen-box jd-box"><div class="gen-label">JD 핵심 문장</div><ul>{items}</ul></section>\n'
    head_extra = KATEX if env.get("has_math") else ""
    tail_extra = (KATEX_JS if env.get("has_math") else "") + (MERMAID_JS if env.get("has_mermaid") else "") + ARTICLE_JS
    page = tpl.substitute(
        title=esc(meta["title"]),
        summary_attr=esc(meta["summary"], quote=True),
        category_label=esc(site["categories"][meta["category"]]),
        card_label=(" · " + esc(meta["card_label"])) if meta.get("card_label") else "",
        content_mode=meta["content_mode"],
        mode_label=esc(site["content_modes"][meta["content_mode"]]),
        published=meta["published"],
        updated=(f" · 갱신 {meta['updated']}" if meta.get("updated") else ""),
        summary_box=summary_box, jd_box=jd_box,
        body=body,
        source_note=esc(meta.get("source_note") or ""),
        head_extra=head_extra, tail_extra=tail_extra,
    )
    card = make_card(slug, meta, site)
    return slug, page, card, meta["published"]


def make_card(slug, meta, site):
    esc = html.escape
    search = " ".join([meta.get("keywords") or "", " ".join(meta["tags"]), " ".join(meta["jd"])]).lower()
    label = site["categories"][meta["category"]] + ((" · " + meta["card_label"]) if meta.get("card_label") else "")
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in meta["tags"])
    return (f'<a class="article" data-category="{esc(meta["category"])}" data-search="{esc(search)}" '
            f'href="articles/{slug}.html"><div class="category">{esc(label)}'
            f'<span class="mode mode-{meta["content_mode"]}">{esc(site["content_modes"][meta["content_mode"]])}</span></div>'
            f'<h2>{esc(meta["title"])}</h2><p>{esc(meta["summary"])}</p>{tags}</a>')


def copy_static(out):
    for item in ROOT.iterdir():
        if item.name in EXCLUDE_TOP or item.name == out.name or item.name.startswith("."):
            continue
        if item.is_file() and item.suffix in EXCLUDE_SUFFIX:
            continue
        dst = out / item.name
        if item.is_dir():
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)


def build(out):
    site = load_site()
    md = make_md()
    tpl = Template((TOOLS / "templates" / "article.html").read_text(encoding="utf-8"))
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    copy_static(out)
    (out / "articles").mkdir(exist_ok=True)

    cards = []  # (date, order, html)
    legacy = yaml.safe_load((TOOLS / "legacy_cards.yml").read_text(encoding="utf-8"))["cards"]
    for i, c in enumerate(legacy):
        cards.append((c["date"], i, c["html"]))

    built, failed = [], []
    for path in sorted((ROOT / "content").glob("*.md")):
        rel = path.relative_to(ROOT)
        try:
            slug, page, card, published = render_article(path, md, site, tpl)
            if (ROOT / "articles" / f"{slug}.html").exists():
                raise ArticleError(f"articles/{slug}.html(legacy)과 이름이 겹칩니다")
            (out / "articles" / f"{slug}.html").write_text(page, encoding="utf-8")
            cards.append((published, len(cards), card))
            built.append(str(rel))
        except Exception as e:  # 글 하나의 실패가 사이트 전체 배포를 막지 않게 한다
            warn(rel, f"이 글은 배포에서 제외됨 — {e}")
            failed.append(str(rel))

    cards.sort(key=lambda c: (c[0], -c[1]), reverse=True)
    index = (TOOLS / "templates" / "index.html").read_text(encoding="utf-8")
    index = index.replace("<!--CARDS-->", "\n".join(c[2] for c in cards))
    (out / "index.html").write_text(index, encoding="utf-8")
    print(f"built {len(built)} article(s), {len(cards)} card(s), failed {len(failed)}")
    for f in failed:
        print(f"  failed: {f}")
    return built, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    a = ap.parse_args()
    out = (ROOT / a.out).resolve()
    if out == ROOT or ROOT not in out.parents:
        sys.exit("--out은 저장소 안의 하위 폴더여야 합니다")
    build(out)


if __name__ == "__main__":
    main()
