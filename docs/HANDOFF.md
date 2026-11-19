# Robotics Knowledge Lab — Handoff

Purpose: keep a concise history of decisions and next steps for local and web agents.

See AGENTS.md and docs/OPERATIONS.md for the publishing rules.

## User's purpose
Build a growing Korean robotics study archive from ChatGPT Q&A. The highest priority is faithful preservation of the user's prompts and complete answers, including tables, code, diagrams, references and source provenance. A clean searchable website and autonomous publishing are supporting goals. Other agents must be able to continue the work without relying on an earlier live chat session.

## Conversation history — main questions and decisions
1. The user supplied Edge Computing and MES questions/answers. These became public article pages; Edge includes a three-question exchange on Jetson/PC distributed processing and real-world robots.
2. The user asked about improved readability: sticky table of contents, back navigation, fonts, and whether Figma was needed. We chose HTML/CSS/JS improvements first.
3. The user requested implementation. Shared reader CSS/JS was added to published pages for TOC, reading progress, top/back controls, responsive layout.
4. The user requested independent cross-checking and later supplied an audit report. Findings: search/category hiding bug, Edge TOC gaps, flattened Edge tables/chart, unlinked sources, hard-coded card count, possible mobile overflow.
5. The user requested audit corrections. Changes were committed; static code checks passed, but full live-browser/mobile regression remains separately unverified.
6. The user asked whether audit findings were sound. The confirmed software and content issues were judged valid; the mobile issue was treated as a candidate rather than proven defect.
7. The user asked how to grow the knowledge base. Decided to use explicit project-chat requests or Notion scheduled requests, with GitHub as the persistent content store.
8. The user asked to repurpose the old Notion Idea Research scheduled job into website publishing. The existing task was updated, not duplicated.
9. The user asked how to enter material. Chat: say '사이트에 게시해줘'. Notion: new row title '사이트 게시 | <question/topic>'. A question-only request permits generation of a new answer, clearly labeled; past GPT answers may only be represented as originals when the full source was actually obtained.
10. The user asked to store operating and agent rules. AGENTS.md, docs/OPERATIONS.md and README.md were created.
11. The user asked about cloned local repositories and web agents working together. We recommended shared Git, feature branches and PRs; handoff documentation is for context, not automatic file synchronization.
12. The user asked whether the handoff exists and for this session's intent and exchange history to be recorded. This document addresses that request.
13. (2026-11-07, local Claude Code session with the user) The site's core intent was restated as a JD / industry-technology knowledge site whose agent-generated visuals (tables, flowcharts, math, code, cards) must survive publishing. After a design exchange with ChatGPT, the user approved moving new articles to Markdown sources (`content/*.md`) built into HTML on deploy, with the homepage generated from front matter. Rules: [AUTHORING.md](AUTHORING.md). Input tests (small samples): the ChatGPT GitHub connector committed one Markdown sample byte-identical and one PNG to a test branch; the answer copy button (2 cases) and drag copy (1 case) produced altered Markdown, so they are not used as sources. Dev/Ops was migrated as the first pilot article; on 2026-11-08 its body was replaced with the original answer Markdown from the ChatGPT answer share link, whose cards and flowcharts are JSX-like layout tags (`<box>`, `<row>`, `<grid>`, `{#each}`) now rendered by `tools/layout_tags.py`.
14. (2026-11-14, local Claude Code session with the user) The user found the homepage hard to scan: it did not show which term/field each item was about or what the user had asked, and the left sidebar was awkward. User decisions: homepage = intro + field chips + per-field one-column list (left sidebar removed); `Systems` split into `ROS 2`, `Linux`, `Manufacturing`, `DevOps` (`Systems` is retired and an article using it is excluded from the build with a warning). Each item shows the user's question(s) verbatim: legacy questions copied into `tools/legacy_cards.yml`, Markdown questions taken from `> [!PROMPT]`. Legacy article pages were not edited, so their in-page chips may still say `Systems`.
15. (2026-11-14 decision, documented 2026-11-16) The user decided to remove the Notion route: the only publishing entry route is an explicit request in the ChatGPT project conversation, with GPT committing the Markdown source through the GitHub connector while preserving the original as much as possible. This supersedes entries 7-9 as far as Notion is concerned. Connector commits go directly to `main` (user decision 2026-11-16; a `post/<slug>`-branch rule considered on 2026-11-14 was dropped to avoid a merge per article — AUTHORING.md section 2, OPERATIONS.md section 3).
16. (2026-11-19, local Claude Code session with the user) After the 2026-11-16 connector article lost two sentences, six inline-code spans and five SVG figures among other content, the user retired the ChatGPT GitHub connector route. New route: the user gives a local Claude Code session a ChatGPT answer share link, an explicit publish request and the exact question (share links do not contain it); Claude Code extracts the body and SVG figures (and, in one case so far, code/chart data) from the share page and commits to `main` (two cases so far; answers with math untested). The user will remove the ChatGPT project instruction and the connector's write access. This supersedes entry 15 as far as the connector is concerned. Rules: AUTHORING.md section 2; plan: docs/plans/2026-11-18-link-import-simplify.md.

This is a curated paraphrased history, not a full original transcript. Never present it as a replacement for source Q&A.

## Operational source of truth and current structure
- Repository: https://github.com/gwanhuiGIM/robotics-knowledge
- Site: https://gwanhuigim.github.io/robotics-knowledge/
- content/*.md: new article sources (see docs/AUTHORING.md); tools/build.py builds the site and homepage on deploy
- tools/templates/index.html: homepage template (categories, keyword search); cards are generated
- articles/: legacy published HTML pages (some older material explicitly reconstructed, not original transcript)
- assets/reader.css and assets/reader.js: shared navigation and reading interface
- .github/workflows/static.yml: Pages deployment on main
- AGENTS.md: invariant agent rules; docs/OPERATIONS.md: operational procedure; docs/HANDOFF.md: current decisions/status

### Scheduled ingestion
Retired. A scheduled task (Robotics Knowledge Lab 게시 자동화) used to read Notion entries titled '사이트 게시 | 질문' and attempt publication. The user paused it on 2026-11-08 and confirmed on 2026-11-16 that it is still off; the user decided on 2026-11-14 not to resume it (entry 15). Do not treat Notion entries as publish requests. See docs/OPERATIONS.md section 3.

### Verification and future collaboration
- Confirm local git clone, branch and dirty state on the user's machine separately. Remote GitHub inspection cannot verify these.
- Check category/search empty results, TOC anchors, back/top buttons, mobile widths 360/390/760px, source accuracy, external references, GitHub deployment and actual rendered page.
- Implemented on 2026-11-07 (entry 13): Markdown source files in `content/`, front-matter metadata, shared article/home templates, a build self-check (`tests/check.py`). Still future work: migrating the remaining legacy HTML articles one by one, browser-level regression tests in CI.
- Site code changes (build, templates, CSS/JS, tests) go through a separate branch/PR; documentation-only changes and article commits go directly to `main` (user decision 2026-11-16; connector commits retired 2026-11-19, entry 16). Refresh current state before writing to shared files, and record verified work plus uncertainties. Never rewrite user Q&A merely to polish layout.

Updated: 2026-11-19 (entry 16; documentation only). Earlier: 2026-11-16 (entry 15 and the Scheduled ingestion paragraph). Earlier note, 2026-11-07: Entry 13 records the Markdown pipeline decision; local build, self-check and headless-Chrome checks passed on the feature branch, but GitHub Actions deployment and the scheduled job were not tested.
