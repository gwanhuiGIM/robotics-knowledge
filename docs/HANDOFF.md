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

This is a curated paraphrased history, not a full original transcript. Never present it as a replacement for source Q&A.
