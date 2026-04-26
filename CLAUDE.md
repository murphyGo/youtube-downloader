# youtube-downloader

A YouTube video downloader with a GH Pages web UI and a CLI for agent automation, sharing a Fly.io proxy that does the actual extraction.

## Quick reference

| File | Role |
|------|------|
| `BRIEF.md` | Problem, MVP scope, tech, out-of-scope, success |
| `PLAN.md` | Flat checklist — checking items off IS the state |
| `DECISIONS.md` | ADR log for non-obvious choices |

## Skills

- `/lite-dev` — picks the next unchecked `PLAN.md` item, implements it, checks it off
- `/code-review` — review pending changes (defaults to `git diff`); reads `BRIEF.md` for project alignment
- `/lite-init` — re-run to refine `BRIEF.md` if direction changes

## Tech

- **Language**: Python (CLI + Fly.io proxy)
- **Core lib**: `yt-dlp`
- **Proxy framework**: FastAPI + Uvicorn
- **UI**: Static HTML + vanilla JS on GitHub Pages
- **Data**: none (stateless)

## Build / test commands

- Install CLI (dev): `pip install -e .`
- Run CLI: `ytdl <url>`
- Install proxy deps: `pip install -r proxy/requirements.txt`
- Run proxy locally: `cd proxy && uvicorn app:app --reload --port 8080`
- Run UI locally: `cd web && python -m http.server 8000`
- Deploy proxy: `cd proxy && fly deploy`
- Deploy UI: push to `main` (GH Pages serves `web/`)

## Conventions

- Commit is the approval gate. No other gates.
- One PLAN.md task per commit when possible.
- If a non-obvious choice is made during dev, append to `DECISIONS.md`.
- The CLI must work standalone (no proxy dependency) — agents call it directly.
- The proxy is the only piece allowed to fetch YouTube; the static UI never talks to YouTube directly.

## When to graduate

If this project grows past ~3k LOC, multiple developers, or real compliance/audit needs, copy `BRIEF.md` into an [aidlc-starter](https://github.com/murphyGo/aidlc-starter) `IDEA.md` and run `/init-project` there. aidlc-lite is intentionally one-way — no migration tool.
