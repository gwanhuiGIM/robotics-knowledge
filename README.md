# Robotics Knowledge Lab

한국어 로보틱스 학습 Q&A를 축적하는 GitHub Pages 지식 아카이브입니다.

- **웹사이트:** https://gwanhuigim.github.io/robotics-knowledge/
- **게시 콘텐츠:** [articles/](articles/)
- **에이전트 작업 지침:** [AGENTS.md](AGENTS.md)
- **운영 경위·게시 절차·자동화·감사·인수인계:** [docs/OPERATIONS.md](docs/OPERATIONS.md)

## 콘텐츠 우선 원칙

사용자가 제공한 **질문·답변 전문 및 표·코드·수식·출처·시각화**를 가능한 한 충실히 보존합니다. 과거 답변을 실제로 확보하지 못했을 때는 새로 생성한 답변을 원문으로 표시하지 않습니다.

## 게시 요청 방법

- **ChatGPT 프로젝트:** Robotics Domain Knowledge 대화에서 명시적으로 `사이트에 게시해줘` 요청.
- 게시 글이 원격 `main`에 올라가면 배포 workflow가 돌고, 빌드를 통과한 글이 사이트에 반영됩니다(커밋 성공과 게시 성공은 따로 확인). Notion 예약 경로는 쓰지 않습니다(2026-11-14 결정).

## 현행 사이트 구조

- `content/*.md` — 새 글 원본(Markdown). 작성 규약: [docs/AUTHORING.md](docs/AUTHORING.md)
- `tools/build.py` — 배포 시 `_site/` 생성(새 글 HTML·홈 카드 자동 생성). ChatGPT 레이아웃 태그는 `tools/layout_tags.py`
- `tools/templates/index.html` — 홈(소개글·분야 칩·검색·분야별 질문 목록) 템플릿
- `articles/` — 기존 HTML 학습 문서
- `assets/` — 공통 읽기 UI(`reader.*`), Markdown 글 스타일·수식·다이어그램(`article.*`), 그림(`img/`)
- `.github/workflows/static.yml` — `main` push 시 빌드·자가검증·GitHub Pages 배포

콘텐츠나 레이아웃을 변경하는 에이전트는 먼저 [AGENTS.md](AGENTS.md)를 읽고 [운영 문서](docs/OPERATIONS.md)를 따르세요.
