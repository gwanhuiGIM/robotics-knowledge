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
- **Notion 예약 작업:** Idea Inbox - GPT의 새 항목 제목을 `사이트 게시 | 질문 또는 학습 주제`로 작성. 질문만 입력했다면 예약 작업이 새 답변 생성과 게시를 시도합니다. 종단간 자동 게시 성공 여부는 실행마다 별도 확인합니다.

## 현행 사이트 구조

- `index.html` — 카드·카테고리·검색
- `articles/` — 공개 학습 문서
- `assets/reader.css`, `assets/reader.js` — 공통 읽기 UI
- `.github/workflows/static.yml` — `main` GitHub Pages 배포

콘텐츠나 레이아웃을 변경하는 에이전트는 먼저 [AGENTS.md](AGENTS.md)를 읽고 [운영 문서](docs/OPERATIONS.md)를 따르세요.
