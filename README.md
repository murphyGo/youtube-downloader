# youtube-downloader

A YouTube video downloader with three faces, all sharing the same `yt-dlp` backbone:

1. **CLI** (`ytdl <url>`) — agent-callable, prints the saved file path on stdout.
2. **Proxy** (FastAPI on Fly.io) — `GET /download?url=...` streams the file back with `Content-Disposition: attachment`.
3. **Web UI** (GH Pages) — paste a URL, click Download, the proxy serves the file.

Single-video, default-quality, no auth. See `BRIEF.md` for scope and `DECISIONS.md` for the design choices.

## Repo layout

```
cli/ytdl/        Python package — the ytdl CLI
proxy/           FastAPI app + Dockerfile + fly.toml for Fly.io
web/             Static index.html for GH Pages
.github/         GH Actions workflow that publishes web/ to Pages
```

## CLI

Install in editable mode (creates the `ytdl` console script):

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/ytdl "https://www.youtube.com/watch?v=tgBuvq_ccjY"
```

Stdout is the absolute path of the downloaded file; progress and warnings go to stderr. Exit codes: `0` success, `1` download failure, `2` usage error, `130` interrupted.

## Proxy (Fly.io)

The proxy wraps `yt-dlp` as `GET /download?url=<encoded-youtube-url>` and streams the resolved video file. URL validation rejects non-YouTube hosts with HTTP 400; `yt-dlp` errors surface as HTTP 502.

Run locally:

```sh
.venv/bin/pip install -r proxy/requirements.txt
cd proxy && .venv/bin/uvicorn app:app --reload --port 8080
curl -OJ 'http://127.0.0.1:8080/download?url=https%3A%2F%2Fwww.youtube.com%2Fshorts%2Fx9vvabHTrm4'
```

Deploy to Fly.io (one-time setup, then push to redeploy):

```sh
cd proxy
fly launch --copy-config --no-deploy   # claim a globally-unique app name + region
fly deploy
```

After deploying, copy the `https://<app>.fly.dev` URL into `web/index.html`'s `PROXY_HOST` constant.

## Web UI (GH Pages)

Static, no build step. Run locally against the proxy:

```sh
cd web && python3 -m http.server 8000
# open http://127.0.0.1:8000
```

To publish to GH Pages:

1. In repo Settings → Pages, set Source to **"GitHub Actions"** (one-time).
2. Push to `main`. The `.github/workflows/pages.yml` workflow uploads `web/` and deploys.
3. Edit `PROXY_HOST` in `web/index.html` to point at your deployed Fly URL.

## Status

See `PLAN.md` for the full task list. The remaining items are the cloud-side toggles only owners can flip:

- Fly.io app name + first deploy
- GH Pages source = "GitHub Actions" in repo Settings
- End-to-end smoke test once both are live

## Layout decisions

Briefly: `yt-dlp` does the heavy lifting (single Python lib for all three pieces), the proxy buffers each video to a per-request tmpdir (simpler than pipe-through streaming and fits Fly's ephemeral disk), and the UI uses `fetch` + `Blob` so HTTP errors land in the page rather than the address bar. Full rationale in `DECISIONS.md`.
