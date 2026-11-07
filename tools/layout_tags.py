"""ChatGPT 답변의 레이아웃 태그(<box>, <row>, <grid>, <icon>, {#each} …)를 HTML로 바꾼다.

ChatGPT 화면의 카드·흐름도는 Markdown 안에 섞인 JSX·Svelte 비슷한 태그로 쓰여 있다
(2026-11-07 답변 공유 링크 원본에서 확인). 이 형식은 OpenAI의 비공개 사양이라 바뀔 수 있으므로:
- 아는 태그는 사이트 CSS 클래스로 그린다(모양은 근사치, 내용·배치 구조는 원문 그대로).
- 모르는 태그는 상자로 감싸 안의 글자를 그대로 보여 주고 경고를 남긴다.
- 블록 전체를 해석하지 못하면 원문 소스를 그대로 보여 주고 경고를 남긴다.

보안: 태그 사이 글자는 markdown-it으로 렌더한 뒤 조각마다 sanitize한다. 이 모듈이 직접 만드는
속성(class, style, data-lucide, href)은 허용 목록·정규식으로 검증한 값만 쓴다.
"""
import html
import json
import re
import textwrap

# 줄 맨 앞에 오면 레이아웃 블록의 시작으로 보는 태그
BLOCK_TAGS = {"box", "row", "grid", "grid-item", "divider", "WritingBlock"}
KNOWN = BLOCK_TAGS | {"icon", "caption", "text", "badge", "Link"}
# 레이아웃 블록 안에서 만나도 태그가 아니라 글자(Markdown·HTML)로 넘기는 일반 HTML 태그
# (닫는 태그가 없는 void 요소 img·br·hr·wbr 포함 — 레이아웃 요소로 보면 짝이 안 맞아 블록 전체가 원문 표시로 떨어진다)
HTML_PASSTHROUGH = {"a", "b", "br", "code", "em", "i", "kbd", "s", "small", "span", "strong", "sub", "sup", "del",
                    "img", "hr", "wbr"}

TOKEN = re.compile(r"[a-z][a-z0-9-]*")
NUM = re.compile(r"\d{1,2}")
LENGTH = re.compile(r"\d{1,4}(?:\.\d+)?(?:px|%|rem|em)")
COLOR = re.compile(r"rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\)|#[0-9a-fA-F]{3,8}")
URL = re.compile(r"https?://[^\s\"'<>]+")
ENUM = {
    "align": {"start", "center", "end", "stretch", "baseline"},
    "justify": {"start", "center", "end", "between", "around", "evenly"},
    "radius": {"none", "sm", "md", "lg", "xl", "full"},
}


class LayoutError(Exception):
    pass


class Unclosed(LayoutError):
    """아직 닫히지 않음 — 다음 줄까지 읽으면 닫힐 수 있다."""


class Node:
    def __init__(self, kind, name="", attrs=None, text=""):
        self.kind, self.name, self.attrs, self.text = kind, name, attrs or {}, text
        self.children = []


# ---------------------------------------------------------------- 토큰화·트리
def _balanced(s, i):
    """s[i] == '{'일 때 짝이 맞는 '}' 다음 위치. 따옴표 안의 괄호는 센다에서 뺀다."""
    depth, q = 0, None
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\":
                i += 1
            elif c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise Unclosed("중괄호가 닫히지 않았습니다")


def _parse_tag(s, i):
    """s[i] == '<'. (name, attrs, selfclose, end) 또는 태그가 아니면 None."""
    m = re.compile(r"<([A-Za-z][\w-]*)").match(s, i)
    if not m:
        return None
    name, j, attrs = m.group(1), m.end(), {}
    while j < len(s):
        while j < len(s) and s[j].isspace():
            j += 1
        if s.startswith("/>", j):
            return name, attrs, True, j + 2
        if j < len(s) and s[j] == ">":
            return name, attrs, False, j + 1
        am = re.compile(r"[A-Za-z_][\w-]*").match(s, j)
        if not am:
            raise LayoutError(f"<{name}> 속성을 읽지 못했습니다")
        key, j = am.group(0), am.end()
        if j < len(s) and s[j] == "=":
            j += 1
            if j < len(s) and s[j] in "\"'":
                end = s.find(s[j], j + 1)
                if end < 0:
                    raise Unclosed(f"<{name} {key}> 따옴표가 닫히지 않았습니다")
                attrs[key] = ("str", s[j + 1:end])
                j = end + 1
            elif j < len(s) and s[j] == "{":
                end = _balanced(s, j)
                attrs[key] = ("expr", s[j + 1:end - 1].strip())
                j = end
            else:
                vm = re.compile(r"[^\s>/]+").match(s, j)
                if not vm:
                    raise LayoutError(f"<{name} {key}=> 값이 없습니다")
                attrs[key] = ("str", vm.group(0))
                j = vm.end()
        else:
            attrs[key] = ("bool", True)
    raise Unclosed(f"<{name}> 태그가 닫히지 않았습니다")


def parse(src):
    root = Node("root")
    stack = [root]
    buf, i = [], 0

    def flush():
        if buf:
            stack[-1].children.append(Node("text", text="".join(buf)))
            buf.clear()

    while i < len(src):
        c = src[i]
        if src.startswith("{#each", i):
            end = _balanced(src, i)
            m = re.fullmatch(r"\{#each\s+(.+)\s+as\s+([A-Za-z_]\w*)\s*\}", src[i:end], re.S)
            if not m:
                raise LayoutError("{#each … as 이름} 형식이 아닙니다")
            flush()
            node = Node("each", attrs={"list": m.group(1).strip(), "var": m.group(2)})
            stack[-1].children.append(node)
            stack.append(node)
            i = end
            continue
        if src.startswith("{/each}", i):
            flush()
            if stack[-1].kind != "each":
                raise LayoutError("{/each}의 짝이 없습니다")
            stack.pop()
            i += len("{/each}")
            continue
        if c == "<":
            cm = re.compile(r"</([A-Za-z][\w-]*)\s*>").match(src, i)
            if cm:
                name = cm.group(1)
                if name in HTML_PASSTHROUGH:
                    buf.append(cm.group(0))
                else:
                    flush()
                    if stack[-1].kind != "el" or stack[-1].name != name:
                        raise LayoutError(f"</{name}>의 짝이 맞지 않습니다")
                    stack.pop()
                i = cm.end()
                continue
            tag = _parse_tag(src, i)
            if tag:
                name, attrs, selfclose, end = tag
                if name in HTML_PASSTHROUGH:
                    buf.append(src[i:end])
                else:
                    flush()
                    node = Node("el", name, attrs)
                    stack[-1].children.append(node)
                    if not selfclose:
                        stack.append(node)
                i = end
                continue
        buf.append(c)
        i += 1
    flush()
    if len(stack) != 1:
        top = stack[-1]
        raise Unclosed(f"<{top.name or top.kind}>가 닫히지 않았습니다")
    return root


# ---------------------------------------------------------------- 값 해석
def _js_value(expr, scope):
    """{3}, {item.icon}, {{size:1,color:"…"}}, [{name:"…"}] 같은 JS 리터럴을 Python 값으로."""
    expr = expr.strip()
    m = re.fullmatch(r"([A-Za-z_]\w*)((?:\.\w+)*)", expr)
    if m and m.group(1) in scope:
        v = scope[m.group(1)]
        for k in filter(None, m.group(2).split(".")):
            v = v.get(k) if isinstance(v, dict) else None
        return v
    as_json = re.sub(r'([{,]\s*)([A-Za-z_$][\w$]*)\s*:', r'\1"\2":', expr)
    try:
        return json.loads(as_json)
    except ValueError:
        return None


def _attr(node, key, scope):
    kind, raw = node.attrs.get(key, (None, None))
    if kind == "expr":
        return _js_value(raw, scope)
    return raw


INTERP = re.compile(r"\{([A-Za-z_]\w*(?:\.\w+)+)\}")


def _interp(text, scope):
    def sub(m):
        v = _js_value(m.group(1), scope)
        return m.group(0) if v is None else str(v)
    return INTERP.sub(sub, text) if scope else text


# ---------------------------------------------------------------- 렌더
class Renderer:
    def __init__(self, md, env, clean):
        self.md, self.env, self.clean = md, env, clean
        self.warnings = []

    def block_md(self, text):
        text = textwrap.dedent(text).strip()
        return self.clean(self.md.render(text, self.env)) if text else ""

    def inline_md(self, text):
        text = " ".join(text.split())
        return self.clean(self.md.renderInline(text, self.env)) if text else ""

    def children(self, node, scope, inline=False):
        out, buf = [], []

        def flush():
            if buf:
                t = "".join(buf)
                out.append(self.inline_md(t) if inline else self.block_md(t))
                buf.clear()

        for ch in node.children:
            if ch.kind == "text":
                buf.append(_interp(ch.text, scope))
            else:
                flush()
                out.append(self.node(ch, scope))
        flush()
        return "".join(out)

    def box_props(self, node, scope):
        cls, style = [], []
        for key, prefix in (("gap", "gap"), ("padding", "pad")):
            v = _attr(node, key, scope)
            if v is not None and NUM.fullmatch(str(v)):
                cls.append(f"lt-{prefix}-{v}")
        for key, prefix in (("align", "al"), ("justify", "jc"), ("radius", "r")):
            v = _attr(node, key, scope)
            if v in ENUM[key]:
                cls.append(f"lt-{prefix}-{v}")
        bg = _attr(node, "background", scope)
        if isinstance(bg, str):
            if COLOR.fullmatch(bg):
                style.append(f"background-color:{bg}")
            elif TOKEN.fullmatch(bg):
                cls.append(f"lt-bg-{bg}")
        bd = _attr(node, "border", scope)
        if bd is True:
            cls.append("lt-bd")
        elif isinstance(bd, dict):
            size, color = bd.get("size", 1), bd.get("color")
            if isinstance(size, (int, float)) and 0 <= size <= 8:
                style.append(f"border:{size:g}px solid")
                if isinstance(color, str) and COLOR.fullmatch(color):
                    style.append(f"border-color:{color}")
        elif isinstance(bd, str) and COLOR.fullmatch(bd):
            cls.append("lt-bd")
            style.append(f"border-color:{bd}")
        w = _attr(node, "width", scope)
        if isinstance(w, str) and LENGTH.fullmatch(w):
            style.append(f"width:{w};flex:none")
        fl = _attr(node, "flex", scope)
        if fl is not None and NUM.fullmatch(str(fl)):
            cls.append(f"lt-flex-{fl}")
        return cls, style

    def wrap(self, tag, cls, style, inner):
        s = f' style="{html.escape(";".join(style))}"' if style else ""
        return f'<{tag} class="{" ".join(cls)}"{s}>{inner}</{tag}>'

    def node(self, node, scope):
        if node.kind == "each":
            items = _js_value(node.attrs["list"], scope)
            if not isinstance(items, list):
                raise LayoutError(f"{{#each}} 목록을 읽지 못했습니다: {node.attrs['list'][:60]}")
            return "".join(self.children(node, {**scope, node.attrs["var"]: it}) for it in items)
        name = node.name
        if name in ("box", "row", "grid", "grid-item"):
            cls, style = self.box_props(node, scope)
            base = {"box": "lt-box", "row": "lt-row", "grid": "lt-grid", "grid-item": "lt-grid-item"}[name]
            if name == "grid":
                cols = _attr(node, "columns", scope)
                if cols is not None and str(cols) in {"1", "2", "3", "4", "5", "6"}:
                    cls.append(f"lt-cols-{cols}")
            return self.wrap("div", [base] + cls, style, self.children(node, scope))
        if name == "icon":
            icon = _attr(node, "name", scope)
            if not (isinstance(icon, str) and TOKEN.fullmatch(icon)):
                return ""
            cls = ["lt-icon"]
            for key in ("size", "color"):
                v = _attr(node, key, scope)
                if isinstance(v, str) and TOKEN.fullmatch(v):
                    cls.append(f"lt-icon-{key}-{v}")
            return f'<i class="{" ".join(cls)}" data-lucide="{icon}" aria-hidden="true"></i>'
        if name == "caption":
            return f'<div class="lt-caption">{self.children(node, scope, inline=True)}</div>'
        if name in ("text", "badge"):
            base = "tx" if name == "text" else "badge"
            cls = [base]
            for key in ("color", "size", "weight"):
                v = _attr(node, key, scope)
                if isinstance(v, str) and TOKEN.fullmatch(v):
                    cls.append(f"{base}-{key}-{v}")
            return f'<span class="{" ".join(cls)}">{self.children(node, scope, inline=True)}</span>'
        if name == "divider":
            return '<hr class="lt-divider">'
        if name == "WritingBlock":
            return f'<div class="lt-writing">{self.children(node, scope)}</div>'
        if name == "Link":
            url, title = _attr(node, "url", scope), _attr(node, "title", scope)
            label = html.escape(str(title or url or ""))
            if isinstance(url, str) and URL.fullmatch(url):
                return f'<a href="{html.escape(url, quote=True)}" rel="noopener noreferrer">{label}</a>'
            return label
        self.warnings.append(f"모르는 레이아웃 태그 <{name}> — 안의 글자만 표시")
        return f'<div class="lt-unknown">{self.children(node, scope)}</div>'


# ---------------------------------------------------------------- 원문에서 블록 찾기
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
START = re.compile(r"^ {0,3}<(" + "|".join(sorted(BLOCK_TAGS, key=len, reverse=True)) + r")[\s/>]")
LINK_INLINE = re.compile(r"<Link\s([^<>]*?)/?>")


HEADING = re.compile(r"^#{1,6}\s")


def _open(text):
    """블록 후보 text가 아직 열려 있으면 True. 다른 해석 오류는 여기서 블록을 끝내고 렌더 단계에서 원문 표시로 처리한다."""
    try:
        parse(text)
    except Unclosed:
        return True
    except LayoutError:
        pass
    return False


def _link_to_md(m):
    try:
        tag = _parse_tag(m.group(0), 0)
    except LayoutError:
        return m.group(0)
    if not tag:
        return m.group(0)
    attrs = tag[1]
    url = attrs.get("url", (None, ""))[1]
    title = attrs.get("title", (None, url))[1] or url
    title = re.sub(r"([\[\]\\])", r"\\\1", str(title))
    if isinstance(url, str) and URL.fullmatch(url):
        return f"[{title}]({url})"
    return title


def extract(body, nonce):
    """레이아웃 블록을 자리표시 문단으로 바꾼다. (바뀐 Markdown, [블록 원문…])."""
    lines = body.split("\n")
    out, blocks, i, fence = [], [], 0, None
    while i < len(lines):
        line = lines[i]
        fm = FENCE.match(line)
        if fence:
            out.append(line)
            if fm and fm.group(1)[0] == fence[0] and len(fm.group(1)) >= len(fence) and not line.strip()[len(fm.group(1)):].strip():
                fence = None
            i += 1
            continue
        if fm:
            fence = fm.group(1)
            out.append(line)
            i += 1
            continue
        if START.match(line):
            j = i + 1
            # 닫히지 않은 블록이 글 끝까지 삼키지 않도록 Markdown 제목 줄 앞에서 멈춘다.
            while j < len(lines) and not HEADING.match(lines[j]) and _open("\n".join(lines[i:j])):
                j += 1
            blocks.append("\n".join(lines[i:j]))
            out += ["", f"@@LAYOUT-{nonce}-{len(blocks) - 1}@@", ""]
            i = j
            continue
        out.append(LINK_INLINE.sub(_link_to_md, line))
        i += 1
    return "\n".join(out), blocks


def render_blocks(html_body, blocks, nonce, md, env, clean):
    """자리표시 문단을 레이아웃 HTML로 바꾼다. 해석 실패 블록은 원문 소스를 보인다. (html, 경고 목록)."""
    warnings = []
    for n, src in enumerate(blocks):
        r = Renderer(md, env, clean)
        try:
            frag = f'<div class="lt-root">{r.children(parse(src), {})}</div>'
            env["has_icons"] = env.get("has_icons") or "data-lucide=" in frag
            warnings += r.warnings
        except LayoutError as e:
            warnings.append(f"레이아웃 블록 {n + 1} 해석 실패({e}) — 원문 소스를 표시")
            frag = ('<div class="lt-fallback"><p class="lt-fallback__note">레이아웃 태그를 해석하지 못해 원문 소스를 그대로 표시합니다.</p>'
                    f'<pre><code>{html.escape(src)}</code></pre></div>')
        token = f"@@LAYOUT-{nonce}-{n}@@"
        placeholder = f"<p>{token}</p>" if f"<p>{token}</p>" in html_body else token
        if placeholder not in html_body:
            raise LayoutError(f"레이아웃 블록 {n + 1}의 자리를 찾지 못했습니다")
        html_body = html_body.replace(placeholder, frag, 1)
    return html_body, warnings
