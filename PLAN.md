# Plan

> Flat checklist. Checking items off IS the project state. Edit freely.

## Commands

- **Install CLI (dev)**: `pip install -e .`
- **Run CLI**: `ytdl <url>`
- **Install proxy deps**: `pip install -r proxy/requirements.txt`
- **Run proxy locally**: `cd proxy && uvicorn app:app --reload --port 8080`
- **Run UI locally**: `cd web && python -m http.server 8000`
- **Deploy proxy**: `cd proxy && fly deploy`
- **Deploy UI**: push to `main`; GH Pages serves `web/` (configure in repo Settings → Pages)

## Tasks

### Setup

- [x] Initialize Python project (`pyproject.toml`) with `yt-dlp` dependency and console_scripts entry for `ytdl`
- [x] Create `web/`, `proxy/`, and `cli/` directory layout with placeholders
- [x] Add `.gitignore` entries for downloads, `__pycache__/`, `.venv/`, fly secrets

### CLI

- [x] Implement `ytdl <url>` that wraps `yt-dlp` and saves to cwd with the video title as filename
- [x] Verify it handles both `watch?v=...` and `/shorts/...` URLs (use the two URLs in BRIEF as smoke tests)
- [x] Print clear progress + final filepath; non-zero exit on failure (so agents can detect errors)

### Proxy

- [x] Bare FastAPI app with `GET /download?url=<encoded>` endpoint
- [x] Endpoint streams the resolved video back with `Content-Disposition: attachment; filename=...` (no client-side YouTube fetch — sidesteps CORS + signature decryption)
- [x] URL validation — only accept YouTube hosts; reject everything else with 400
- [x] CORS headers allowing the GH Pages origin
- [x] `Dockerfile` + `fly.toml` for Fly.io (Docker build + run verified locally)
- [ ] Deploy proxy to Fly.io + curl smoke test against deployed URL (needs user-chosen app name + region; `fly launch --copy-config --no-deploy` to claim a name, then `fly deploy`)

### Web UI

- [x] Single `index.html` with URL input, download button, status text
- [ ] Client-side YouTube URL validation; enable button only when valid
- [ ] Button links to `<PROXY_HOST>/download?url=<encoded>` (browser handles the file save via `Content-Disposition`)
- [ ] Configure GH Pages to serve `web/`

### Polish

- [ ] Friendly error states in UI (invalid URL, proxy 5xx, video unavailable)
- [ ] CLI error messages for the obvious failure modes (network, age-gated, removed video)
- [ ] Update root `README.md` with deploy + usage steps for all three pieces
- [ ] End-to-end manual smoke test using the two example URLs from BRIEF

---

**Conventions**:
- One task ≈ one commit (<200 LOC diff). Split if it grows.
- If a task is blocked, leave it unchecked and skip ahead.
- Add new tasks freely. Reorder freely. Don't nest deeper than one level.
