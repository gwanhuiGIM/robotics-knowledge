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
13. (2026-11-07, local Claude Code session with the user) The site's core intent was restated as a JD / industry-technology knowledge site whose agent-generated visuals (tables, flowcharts, math, code, cards) must survive publishing. After a design exchange with ChatGPT, the user approved moving new articles to Markdown sources (`content/*.md`) built into HTML on deploy, with the homepage generated from front matter. Rules: [AUTHORING.md](AUTHORING.md). Input tests (small samples): the ChatGPT GitHub connector committed one Markdown sample byte-identical and one PNG to a test branch; the answer copy button (2 cases) and drag copy (1 case) produced altered Markdown, so they are not used as sources. Dev/Ops was migrated as the first pilot article.

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
Previously configured task: Robotics Knowledge Lab 게시 자동화, ID 6a95f0a1d2048191b0cdc1f9aa03eedd. At last confirmed setup it uses Asia/Seoul 00:00, 12:00, 15:00, 18:00. Input is the existing Notion Idea Inbox - GPT data source; an explicit '사이트 게시 | 질문' request authorizes a newly generated explanatory answer and site publication. Preserve existing answer only if its actual full text is available. Check duplicate articles and public data risks, then update article, index and original Notion request with result. Always re-check the automation's active configuration; success of configuration changes does not prove successful end-to-end scheduled publication.

### Verification and future collaboration
- Confirm local git clone, branch and dirty state on the user's machine separately. Remote GitHub inspection cannot verify these.
- Check category/search empty results, TOC anchors, back/top buttons, mobile widths 360/390/760px, source accuracy, external references, GitHub deployment and actual rendered page.
- Implemented on 2026-11-07 (entry 13): Markdown source files in `content/`, front-matter metadata, shared article/home templates, a build self-check (`tests/check.py`). Still future work: migrating the remaining legacy HTML articles one by one, browser-level regression tests in CI, a controlled Notion-to-GitHub dry run.
- Local and web agents should operate on separate branches/PRs where practical, refresh current state before writing to shared files, and record verified work plus uncertainties. Never rewrite user Q&A merely to polish layout.

Updated: 2026-11-07. Entry 13 records the Markdown pipeline decision; local build, self-check and headless-Chrome checks passed on the feature branch, but GitHub Actions deployment and the scheduled job were not tested.
