# 게시 경로를 "공유 링크 → Claude 추출"로 바꾸고 GPT 전용 부분 걷어 내기

작성 2026-11-18 12:55 · 개정 2026-11-19 14:11(계획 검증 반영 — devils-advocate 단독, Codex는 사용 한도로 미실행) · 상태: 승인됨(사용자 "q1o" 2026-11-19) · A 완료(d82b89a·a8c3ec3, OPERATIONS 6절 8번만 wide merge 뒤) · B 완료(2026-11-19 15:08, 단 B-2의 위젯 JSON 변환은 미구현 — 감지하면 멈추고 손으로 옮김 — 도구·`/knowledge` 명령은 로컬 `.claude/`, `tests/check.py` SVG 검사 69c9a22 브랜치 `feat/knowledge-svg-check`, AUTHORING 2절 안내 2899cf0)

## 배경
- 사용자 결정(2026-11-18): 저장소 구조는 유지하고, ChatGPT가 직접 올리는 경로 대신 Claude가 답변 공유 링크에서 원문을 추출해 올린다(사용자 "q3o", 그 전 "직접 올리는데 원문보존이 안된다는 뜻 아닌지").
- 근거(표본이 작다 — 양쪽 다 1~2건): GPT 직접 게시 3건 중 그림이 많은 1건(11-16 경로계획, 4a13423)에서 문장 2개·인라인 코드 6곳·SVG 5개가 빠지고 그림이 흐름도로 바뀜. 링크 추출 2건(a7a9f04 멀티스레딩, 434030b 신입 C++·Python): 멀티스레딩 글은 본문 줄 누락 0·화면 순서와 그림 위치 일치(세션 대조 기록, 대조에 쓴 사본은 scratchpad 정리로 소실). 434030b는 접힌 질문 카드·공고 링크·배지를 화면 DOM에서 복원해야 했다.
- 링크 방식에서 알려진 한계: 공유 링크에 사용자 질문이 없다. 본문 사본에 카드 레이아웃 태그·외부 링크·배지·접힌 항목이 없다(11-07에는 공유 링크 원본에 레이아웃 태그가 있었다 — AUTHORING 6절, 형식이 바뀐 것으로 보임). 본문 사본은 코드 빈 줄을 잃을 수 있다(코드는 위젯 JSON 기준). 차트는 사이트에서 표로만 보인다. **수식이 있는 답변은 링크 방식으로 시험한 적이 없다**(2건 모두 수식 0줄).

## 할 일 (두 갈래로 나눠 각각 끝낼 수 있게)
### A. 문서 정리 — main 직접 커밋(문서만 바뀜)
1. 대상 전수: `grep -rn -i "connector\|ChatGPT 프로젝트" AGENTS.md docs/*.md`로 목록을 만든 뒤 고친다. 최소 AGENTS 규칙 1, AUTHORING 서두·2절·6절 끝 connector 문장·8절, OPERATIONS 입력 경로(23행 "공유 URL만으로 재현 어려움" 포함)·6절, HANDOFF entry 15·46행, state.md 상시 규칙의 connector 근거. 끝나면 같은 grep이 0건(또는 예비 경로 문구만)인지 확인.
2. 새 게시 규칙: 게시 요청 = "공유 링크 + 명시적 게시 요청(또는 `/knowledge`)". 질문 원문은 사용자에게 "원문 그대로" 따로 받고, PROMPT에 넣은 경계를 보고에 보인다. 질문을 못 받으면 멈추고 묻는다.
3. AUTHORING 3절 "회사명·지원처는 쓰지 않는다"의 적용 범위(jd 필드만인지)를 434030b 사용자 결정("q1x q2x")과 맞춘다.
4. 순서: `feat/wide-layout-delete`가 AGENTS·AUTHORING·OPERATIONS·HANDOFF를 고치므로 그 브랜치 merge 뒤에 하거나, 겹치는 줄을 먼저 확인한다.

### B. 추출 도구 — 브랜치
1. 출발점: 다른 세션이 만든 로컬 초안 `.claude/knowledge/extract.js`·`check_lines.py`(node playwright-core)와 이 계획의 `tools/import_share.py`(python) 중 **하나만** 남긴다(아래 Q). 두 초안의 입력 선택자(`data-octane-input` vs `conversationState`)를 같은 링크에서 함께 찍어 대조한다.
2. 추출 항목: 본문 사본, data URI SVG(위치는 직전 텍스트로 찾고 0회·2회 이상 일치면 멈춤), 위젯 JSON(code_block → 코드 fence, visualization → `<Chart>`), 외부 링크(`a[href^=http]`)·배지·접힌 항목, 수식(사본이 평탄화돼 있으면 KaTeX DOM의 TeX 주석에서 추출 — 추정, 먼저 경로계획 링크로 확인).
3. 멈춤 조건(exit≠0): 선택자 미발견, messages 수≠1 또는 `/share/` 링크(여러 턴), 로그인·봇 차단 문구, 화면에 그림이 있는데 추출 0, data URI가 아닌 외부 이미지(목록과 "권한 확인 전 미게시" NOTE 초안만 출력).
4. 원문 사본 보존: page.html·본문 사본·위젯 JSON을 slug별로 scratchpad가 아닌 **로컬 전용 위치**(커밋 제외 — scratchpad는 정리로 사라짐, 11-19 실제 소실)에 남긴다 — AGENTS 규칙 4. 위치는 아래 Q.
5. SVG 검사: `<script>`·`on*` 속성·`foreignObject`·외부 href가 있으면 거부(import와 `tests/check.py` 둘 다). 색은 `currentColor`만 바꾸고, 연한 채움 칸이 있는 그림은 자동 변환하지 않고 표시만 한다.
6. 검사 출력: 원문 줄 포함 검사(이스케이프·표 구분선 정규화 뒤 — 줄 일치율을 손실 지표로 쓰지 않는다), 잘라낸 후속 제안 목록 전문, 화면 순서 대조(공유 페이지 vs 빌드 결과).
7. 실행 환경: CI의 `tools/requirements.txt`에 playwright를 넣지 않는다. python이면 `uv run --with playwright`, node면 기존 초안 방식.

## 검증
- 경로계획 공유 링크(수식 있음)와 멀티스레딩 링크를 다시 받아(네트워크 접속 — 실행 때 사용자 승인) 위치·SVG 본문·코드가 현재 글과 같은지 본다. 색 처리·파일 이름 차이는 제외.

## 범위 밖
- 옛 HTML 글(`articles/*.html`) md 이전.
- 차트를 그래프로 그리는 렌더러 변경(차트가 많은 답변이 오면 다시 검토).

## 사용자 결정 대기
- connector를 예비 경로로 남길지 지울지. 지우면 ChatGPT 프로젝트 지시문 제거와 GitHub connector 쓰기 권한 해제를 사용자가 해야 경로가 실제로 닫힌다.
- 추출 도구를 node 초안(`/knowledge`)으로 합칠지 python으로 새로 쓸지.
- 원문 사본 보관 위치.
- 수식이 평탄화된 답변이면 게시를 멈출지.
