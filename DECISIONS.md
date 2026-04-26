# Decisions

> Append-only ADR log. Only record choices future-you would wonder about.
>
> Format: `## YYYY-MM-DD: <short title>` followed by a `**Why**:` paragraph (2–4 lines covering reasoning, alternatives, and any constraint this locks in). Newest entries at the bottom.

---

## 2026-04-27: Python + yt-dlp for both CLI and proxy

**Why**: `yt-dlp` is the actively-maintained fork of `youtube-dl` and is the de-facto tool for YouTube extraction — writing this from scratch would be reinventing a moving target. Using Python for both the CLI and the Fly.io proxy keeps a single stack and lets the proxy reuse the CLI's wrapper logic. Alternatives considered: Go + `yt-dlp` shelled out (more deploy hassle, no real win), Node + `youtube-dl-exec` (smaller ecosystem of fixes).

## 2026-04-27: GH Pages UI + Fly.io proxy that streams files

**Why**: GH Pages alone cannot download YouTube videos — the browser is blocked by CORS and YouTube's signed URLs require server-side decryption (which `yt-dlp` does). The chosen split: GH Pages serves a tiny static UI; a Fly.io proxy receives the URL, runs `yt-dlp`, and streams the file back with `Content-Disposition: attachment` so the browser handles the save. Returning a direct YouTube CDN URL was rejected as fragile (CORS + signature expiry). This locks in the constraint that v1 needs both GH Pages and Fly.io to be deployed for the UI to work; the CLI works standalone.

## 2026-04-27: v1 deferrals — playlists, quality picker, subtitles, auth

**Why**: All four are real features but each multiplies UI surface area or forces session/state. Single-video, default-quality, no-auth keeps v1 to roughly one screen of HTML and one FastAPI endpoint. Reconsider once the happy path is rock-solid.

## 2026-04-27: Hatchling build backend, package nested as `cli/ytdl/`

**Why**: Hatchling is the modern PEP 517 default and needs zero `MANIFEST.in` / `setup.cfg` ceremony. The package source lives at `cli/ytdl/` (not `ytdl/` at repo root) so the PLAN's `cli/` / `proxy/` / `web/` triad stays clean — `cli/` holds CLI source, with `ytdl` as the importable package name preserved via `[tool.hatch.build.targets.wheel] packages = ["cli/ytdl"]`. This locks in: console entry resolves to `ytdl.main:main`, and any future CLI Python modules go under `cli/ytdl/`, not at repo root.

## 2026-04-27: Single-file MP4 format (no ffmpeg merge)

**Why**: `format="best[ext=mp4]/best"` picks the best single-file MP4 (currently itag 18, 360p) so the CLI works with no ffmpeg dependency. Higher resolutions on YouTube are split into separate video+audio streams that require ffmpeg merging, and yt-dlp's JS challenge solver (needed for the highest streams) wants a deno/node runtime — both extra deps we said we'd avoid in v1. Trade: lower default quality. Smoke test confirmed both `watch?v=...` and `/shorts/...` URLs download correctly with this setting. Revisit if quality complaints surface.

## 2026-04-27: GH Actions workflow over `/docs` rename for Pages

**Why**: GH Pages "Deploy from a branch" only supports root or `/docs`, never `/web`. Two ways to honor PLAN's `web/` directory: rename `web/` → `docs/` (loses semantic name, conflicts with future doc folder), or use a GH Actions workflow that uploads `web/`. Picked the workflow — keeps the directory layout clean and lets the UI evolve (build steps later) without another rename. Cost: requires the repo owner to flip Pages source to "GitHub Actions" once in Settings.

---

*New entries go below, newest at the bottom.*
