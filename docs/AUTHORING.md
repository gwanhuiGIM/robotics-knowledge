# 글 작성 규약 (AUTHORING)

새 글을 쓰는 모든 경로(ChatGPT GitHub connector, Notion 예약 작업, 로컬 Claude Code·Codex)가 따르는 단일 규약이다. 허용 값(분류·답변 모드·필수 필드)의 원본은 [`tools/site.yml`](../tools/site.yml)이고, 이 문서는 값을 다시 적지 않고 그 파일을 가리킨다.

## 1. 어디에 쓰나

| 대상 | 위치 | 비고 |
|---|---|---|
| 글 원본 | `content/<slug>.md` | slug = 소문자·숫자·하이픈. 게시 URL은 `articles/<slug>.html` |
| 그림 파일 | `assets/img/<slug>/<이름>.png·svg` | 본문에서 `../assets/img/<slug>/<이름>.png`로 참조 |
| 홈 카드 | **쓰지 않는다** | 배포할 때 front matter로 자동 생성된다 |

- `index.html`은 더 이상 저장소 루트에 없다. 홈은 `tools/templates/index.html` + 각 글 front matter로 빌드된다. 기존 HTML 글(`articles/*.html`)의 카드는 `tools/legacy_cards.yml`에 원문 그대로 보존돼 있다.
- 새 글을 `articles/*.html`로 직접 쓰지 않는다. 기존 HTML 글과 같은 slug의 `content/*.md`를 만들면 빌드가 그 글을 제외하고 경고한다(옮길 때는 기존 HTML을 지우는 커밋과 함께).

## 2. 입력 경로

1. **ChatGPT GitHub connector(새 글 기본)**: GPT가 Markdown 원문을 `content/<slug>.md`로 직접 커밋한다. 그림은 base64 blob으로 `assets/img/<slug>/`에 커밋한다(2026-11-07 시험 브랜치에서 텍스트 바이트 일치·PNG 커밋 1건 확인). 글과 그림은 한 커밋으로 올리는 것을 권장한다.
   - 2026-11-07 시험(1건): GPT가 자기 이전 답변(레이아웃 태그 포함)을 커밋한 결과가 답변 공유 링크의 원본과 일치했다(끝의 후속 제안 목록 제외, 마지막 줄바꿈 1개 차이). GPT는 "두 부분으로 출력된 답변을 하나로 연결했다"고 밝혔다. 다만 첫 커밋은 인라인 코드 백틱을 `` \` ``로 바꿔 적었고, GPT가 파일을 다시 읽은 뒤 두 번째 커밋으로 고쳤다.
   - 그래서 **커밋 뒤 파일을 다시 읽어 원문과 대조하고, 다르면 고친 뒤 보고한다**(바뀐 곳과 최종 커밋 SHA 포함).
2. **로컬 보완**: GPT에게 "Markdown 원문을 바깥 백틱 4개 코드 블록 하나로 출력"하게 한 뒤 그 블록 내용을 받아 파일로 저장한다.
3. **쓰지 않는 방법**: 렌더링된 답변을 드래그 복사하거나 답변 복사 버튼으로 받은 텍스트. 2026-11-06~07에 답변 복사 버튼 2건·드래그 1건을 확인했는데, 모두 원문 Markdown과 달랐다(제목·표 구조 손실, Mermaid 원문 파손, 수식 역슬래시 변형, `**`·코드 언어명 소실 중 일부). 같은 복사 버튼이라도 답변에 따라 손실 양상이 달랐다.

## 3. front matter

```yaml
---
title: "ROS 2 QoS의 Reliability와 Durability 차이"   # 필수
category: Systems                  # 필수 — tools/site.yml categories 중 하나
content_mode: new_answer           # 필수 — tools/site.yml content_modes 중 하나 (아래 4절)
published: 2026-11-07              # 필수 — YYYY-MM-DD
updated: 2026-11-08                # 선택
summary: "카드와 글 상단에 보일 한두 문장"   # 필수 — 게시 시 작성, 화면에 '요약 · 게시 시 작성'으로 표시
card_label: "ROS 2 · QoS"          # 선택 — 카드 상단 분류 옆 짧은 라벨
tags: [ROS 2, QoS, DDS]            # 선택 — 카드 태그
keywords: "qos reliability durability dds 신뢰성"   # 선택 — 홈 검색어(화면에 안 보임)
jd: ["JD에서 이 개념이 나온 핵심 문장"]   # 선택 — 화면에 'JD 핵심 문장'으로 표시
source_note: "출처: …"             # 선택 — 글 맨 아래 출처 문구
---
```

- `jd`에는 **JD 핵심 문장만** 쓴다. 회사명·지원처·JD 전문은 쓰지 않는다(공개 저장소).
- `summary`·`jd`는 원문이 아니라 게시할 때 작성한 내용이다. 화면에서 점선 상자로 원문과 구분된다.

## 4. content_mode — 답변의 출처 상태

| 값 | 쓰는 경우 | 화면 라벨 |
|---|---|---|
| `original_qa` | 사용자 질문 + 실제로 확보한 ChatGPT 답변 원문(구조 포함) | 원문 Q&A |
| `new_answer` | 질문·주제만 받고 게시할 때 새로 작성한 답변 | 새로 생성한 답변 |
| `reconstructed` | 과거 답변이 있었지만 원문을 확보하지 못해 다시 구성한 답변 | 재구성 답변 |

- 답변 전체가 아니라 **일부 시각자료만** 다시 그렸다면 글 전체의 값은 바꾸지 않고, 그 그림 앞에 `> [!WARNING]`으로 "재구성 시각자료"임을 적는다.
- 확보하지 못한 원문을 원문처럼 쓰지 않는다(AGENTS.md 규칙 2·3).
- **기존 답변 원문을 게시해 달라는 요청**인데 원문을 확보하지 못했다면 `reconstructed`로 바꿔 게시하지 않는다. 게시를 멈추고 확인을 요청한다(OPERATIONS.md 3절 B, Notion 요청이면 `확인 필요`).

## 5. 본문 구조

```markdown
> [!PROMPT]
> 사용자가 실제로 입력한 질문 그대로

> [!NOTE]
> 원문 상태 설명(예: 표의 레이아웃만 정리, 문장은 바꾸지 않음)

# 답변 제목(원문에 있으면 그대로)

답변 본문…
```

- 질의가 여러 번이면 `> [!PROMPT]`와 답변을 순서대로 반복한다.
- 원문을 손질했다면 무엇을 바꿨는지 `> [!NOTE]`에 적는다.

## 6. 지원 문법

| 요소 | 쓰는 법 | 주의 |
|---|---|---|
| 표 | GFM 표 | 칸 안의 `|`(수식 포함)는 `\|`로 쓴다. 안 쓰면 칸이 잘려 뒤 내용이 사라진다 |
| 코드 | ` ```python ` 처럼 언어명을 붙인 fence | 언어명이 class로 남는다 |
| 수식 | 인라인 `$…$` 또는 `\(…\)`, 블록 `$$…$$` 또는 `\[…\]` | `$100`, `$HOME`처럼 `$` 바로 뒤 공백·숫자는 수식으로 보지 않는다. KaTeX로 그리고, 실패하면 TeX 원문이 보인다 |
| 흐름도 | ` ```mermaid ` fence | 브라우저에서 그림으로 바뀐다. 문법 오류면 원문 코드와 오류 문구가 보인다 |
| 알림 상자 | `> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`, `[!PROMPT]` | `[!…]` 줄 끝에 다른 글자나 `\`를 붙이지 않는다 |
| 카드 | 아래 HTML | 정보 구조가 있는 비교·단계에만. 단순 안내는 알림 상자 |
| 강조 태그 | `<badge color="success">수용</badge>`, `<text color="secondary" size="xs">…</text>` | ChatGPT 답변에 나오는 태그. color: success·warning·danger·info |
| 레이아웃 태그 | ChatGPT 답변 원문의 `<box>`·`<row>`·`<grid>`·`<grid-item>`·`<icon>`·`<caption>`·`<divider>`·`<WritingBlock>`·`<Link>`, `{#each … as item}` | 아래 "레이아웃 태그" 참고. 원문 그대로 두면 빌드가 상자·행·격자로 그린다 |
| 그림 | `![대체 텍스트](../assets/img/<slug>/x.png)` | 대체 텍스트 필수. 외부 이미지는 출처·이용 권한 확인 |
| 접기 | `<details><summary>제목</summary>` + 빈 줄 + 내용 + 빈 줄 + `</details>` | 원문 텍스트를 함께 남길 때 |

카드:

```html
<div class="visual-grid">
<div class="visual-card"><div class="visual-card__title">Dev</div><div class="visual-card__sub">Development</div><div class="visual-card__body"><p>설명</p></div></div>
<div class="visual-card"><div class="visual-card__title">Ops</div><div class="visual-card__body"><p>설명</p></div></div>
</div>
```

- HTML은 허용 목록만 남고 나머지는 지워진다(`<script>`, `onclick` 같은 속성, `javascript:` 링크, `style`(표 정렬 제외)). 허용 목록: `tools/build.py`의 `ALLOWED_TAGS`·`ALLOWED_ATTRS`.
- 카드 HTML 블록 안에서는 Markdown 문법이 적용되지 않는다. 코드는 `<code>`로 쓴다.

### 레이아웃 태그 (ChatGPT 화면의 카드·흐름도)

ChatGPT 화면의 카드·흐름도·"Writing" 상자는 답변 원문 Markdown 안에 JSX 비슷한 태그로 들어 있다(2026-11-07 답변 공유 링크 원본에서 확인). **원문을 고치지 않고 그대로 커밋한다.** 빌드(`tools/layout_tags.py`)가 다음처럼 처리한다.

- `<box>`·`<row>`·`<grid>`·`<grid-item>`·`<divider>`·`<WritingBlock>`·`<AsyncImage>`·`<AsyncImageGroup>`·`<Chart>`로 시작하는 줄부터 그 태그가 닫히는 줄까지를 한 블록으로 읽는다. 코드 fence(목록 안 포함)와 인라인 코드 안의 태그는 바꾸지 않는다. 끝까지 닫히지 않으면 들여쓰지 않은 다음 일반 줄(제목·문단) 앞에서 블록을 끊는다.
- 속성 `gap`·`padding`·`radius`·`align`·`justify`·`background`·`border`·`width`·`flex`·`columns`는 정해진 값(숫자, 색 `rgba()`·`#hex`, 이름 토큰)만 반영하고 나머지는 버린다. 태그 사이 글자는 Markdown(굵게·수식 등)으로 렌더한다.
- `<icon name="…">`은 lucide 아이콘 이름이다. CDN(lucide 0.469.0)을 못 불러오면 아이콘 자리만 비고 글자는 그대로다.
- `<Link url title/>`은 문단 안에서도 링크로 바뀐다. `http`·`https` 주소만 링크가 된다.
- ChatGPT 화면 위젯(2026-11-14 BC·DAgger 글 원문에서 확인): `<Entity value=…/>`는 value 글자로, `<Cite …/>`(출처 id `turn…`, 사이트에서 열 수 없음)는 지우고, `<AsyncImage>`·`<AsyncImageGroup>`(화면 표시 때 검색어로 불러오는 그림 — 원문에 그림 파일이 없음)은 지우고, `<Chart content={…}/>`는 원문 데이터를 표로 보인다. `<Entity>`·`<Cite>`는 블록 밖 문단에서도 같다. 차트 모양(막대)은 재현하지 않는다.
- 레이아웃 블록 **안의 모르는 태그**는 상자로 감싸 안의 글자만 보이고, **해석하지 못한 블록**은 원문 소스를 그대로 보인다. 둘 다 Actions에 `::warning`을 남기고 글은 배포된다. 블록 **밖**의 모르는 태그는 일반 HTML처럼 허용 목록 검사에서 태그만 지워지고 글자는 남지만, `{…}` 속성을 가진 JSX식 태그는 HTML로 인식되지 않아 태그 글자가 그대로 보일 수 있다(2026-11-14 확인: `refs={["…"]}`처럼 중괄호 안에 따옴표·공백이 있으면 글자로 노출, `gap={3}`처럼 단순하면 지워짐). `tests/check.py --site`는 코드·수식 밖에 글자로 남은 태그, 짝 잃은 `**`, 생성 글의 모르는 레이아웃 태그 상자를 실패로 잡는다. 블록 밖 따옴표 속성 태그가 조용히 지워지는 것은 못 잡는다. Actions의 check 단계는 `continue-on-error`라 실패해도 배포는 진행된다 — merge 전에 로컬에서 돌린다.
- 모양(아이콘·색·여백)은 ChatGPT 화면과 비슷하게까지다. 이 태그 형식은 공개 문서를 찾지 못한 형식이라 바뀔 수 있다.

## 7. 게시 전 확인

로컬에서(⚠️ uv 사용 예):

```bash
uv run --no-project --with-requirements tools/requirements.txt python tools/build.py --out _site
uv run --no-project --with-requirements tools/requirements.txt python tests/check.py --site _site
python3 -m http.server 8799 --directory _site   # 브라우저로 http://127.0.0.1:8799/ 확인
```

- connector 게시도 배포 workflow에서 같은 빌드·검사가 돈다. 글 하나가 규약을 어기면 그 글만 배포에서 빠지고 Actions에 `::warning`이 남는다 — **커밋 성공 ≠ 게시 성공**이므로 Actions 결과와 실제 페이지를 따로 확인한다(AGENTS.md 규칙 9).
- 중복 확인: 같은 주제·같은 질문의 글이 `content/`나 `tools/legacy_cards.yml`에 이미 있는지 먼저 본다.

## 8. ChatGPT 프로젝트 지시문에 넣을 포인터

규약을 지시문에 복사하지 말고 아래처럼 가리키기만 한다(복사본은 저장소와 어긋난다).

```text
사이트 게시 요청을 받으면 GitHub 저장소 gwanhuiGIM/robotics-knowledge의 docs/AUTHORING.md와 AGENTS.md를 connector로 먼저 읽고 그대로 따른다.
새 글은 content/<slug>.md(Markdown 원문 + front matter)로만 커밋한다. 커밋 뒤 파일을 다시 읽어 원문과 대조하고, 다르면 고친 뒤 바뀐 곳과 최종 커밋 SHA를 보고한다. 새 글을 articles/*.html로 만들거나 홈 카드(tools/templates/index.html, tools/legacy_cards.yml)를 직접 고치지 않는다. 기존 HTML 글의 수정은 사용자가 요청했을 때만 AGENTS.md 규칙대로 한다.
```
