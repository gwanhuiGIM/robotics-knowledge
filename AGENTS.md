# Robotics Knowledge Lab — Agent Instructions

> Applies to Codex, Claude Code, ChatGPT Work, and other AI/software agents working in this repository. Read [docs/OPERATIONS.md](docs/OPERATIONS.md) and [docs/HANDOFF.md](docs/HANDOFF.md) before modifying published content.

## Mission and priority

This is a Korean-language robotics learning archive. **Highest priority: preserve the user's exact question(s), existing ChatGPT answer(s), code, formulas, tables, references, and the distinction between source material and newly generated content.** UI polish and categorization must not override this priority.

Repository: https://github.com/gwanhuiGIM/robotics-knowledge
Site: https://gwanhuigim.github.io/robotics-knowledge/

## Non-negotiable rules

1. **Explicit publishing intent only.** A question or an idea alone is not authorization to make it public. Publish when the user explicitly requests site publication (in ChatGPT project conversation or in Notion). For Notion, recognize `사이트 게시 | <질문 또는 주제>` in a new entry.
2. **Two content modes.** (a) Existing Q&A: use the complete *actually retrieved* text, preserving sequence and wording; do not paraphrase it as an original. (b) Topic/question-only: write a fresh, technically grounded answer and label it **새로 생성한 답변**. Never claim access to past chat text that was not retrieved.
3. Do not silently remove/add claims, invent citations, manipulate original measurements, reconstruct missing sentences as source text, or conflate a recreated visualization with a source image.
4. Keep original source material separately when feasible. Rendering fixes (semantic headings, tables, LaTeX, code highlighting) may change markup **without changing informational meaning**. If exact restoration is impossible, disclose it.
5. Treat all GitHub Pages content as **public**. Check for personal information, secrets, proprietary material, credentials, private attachments, and third-party reuse rights before committing.
6. Preserve the working dark design and features: **category sidebar, keyword search, article links, sticky TOC, back/list/top controls, reading progress, mobile responsive layout**.
7. Check duplicates before adding an article (title, Notion page URL/ID, topic and source). Do not create multiple cards for the same article; update only if requested or materially necessary.
8. Do not overwrite unrelated user files, delete existing articles, or reword prior Q&A as a side effect of layout improvements.
9. Distinguish **commit success**, **GitHub Actions deployment success**, and **real rendered/browser behavior**. Do not report unperformed tests as passed.
10. Prefer smallest reviewable changes, clear commit messages, and a short record of what changed, verification, and remaining uncertainty. For large architectural migration, propose and stage a safe migration rather than destructively rewriting the site.

## Existing implementation (verify before relying on it)

- **New articles are Markdown**: write `content/<slug>.md` (front matter + Markdown) following [docs/AUTHORING.md](docs/AUTHORING.md). Allowed values live only in `tools/site.yml`. Do **not** create `articles/*.html` or edit the homepage by hand for new articles.
- `tools/build.py`: builds `_site/` on deploy — renders `content/*.md` to `articles/<slug>.html`, generates the homepage from `tools/templates/index.html`, copies legacy files, excludes `docs/`, `AGENTS.md`, `*.txt`, `content/`, `tools/`. `tools/layout_tags.py` renders ChatGPT layout tags (`<box>`, `<row>`, `<grid>`, `{#each}`) kept verbatim in `content/*.md`.
- `tools/legacy_cards.yml`: verbatim homepage cards of the legacy HTML articles.
- `articles/*.html`: legacy static articles (individual markup/styles); keep unless migrating one to `content/` in the same change.
- `assets/reader.css`, `assets/reader.js`: shared article reading UI. `assets/article.css`, `assets/article.js`: Markdown article styles and KaTeX/Mermaid/lucide-icon rendering (pinned CDN versions with SRI in `tools/build.py`).
- `tests/check.py`: renderer and site self-check (`python tests/check.py --site _site`).
- `.github/workflows/static.yml`: on `main` push, builds `_site`, runs the self-check (warning only), deploys `_site` to GitHub Pages.
- No independent database server is currently a documented requirement; GitHub files are the source of truth.

## Publish checklist

- [ ] Explicit request and source provenance identified
- [ ] Exact prompt preserved; answer mode accurately labeled
- [ ] Original Q&A content complete (or limitations clearly stated)
- [ ] Tables/code/math/links/visuals handled without unmarked alteration
- [ ] Existing article checked; safe filename and category/keywords chosen
- [ ] New article written as `content/<slug>.md` per docs/AUTHORING.md (front matter valid, `content_mode` accurate); homepage lists it once
- [ ] Search and categories actually hide nonmatching cards
- [ ] Heading IDs/TOC anchors valid; long tables scroll within mobile viewport
- [ ] Accessibility, keyboard interaction and narrow screen checked where tooling permits
- [ ] Commit SHA obtained; deployment/browser status verified separately
- [ ] Notion result updated when the request originated in Notion

## Handoff

Read [docs/HANDOFF.md](docs/HANDOFF.md) for recent user intentions and decisions, and [docs/OPERATIONS.md](docs/OPERATIONS.md) for the background, two user entry routes, scheduled automation, audit findings, acceptance tests, and future architecture. If those instructions conflict with a current explicit user instruction, obey the user, note the conflict, and preserve source data.
