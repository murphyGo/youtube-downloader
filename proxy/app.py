import os
import shutil
import tempfile
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

app = FastAPI(title="youtube-downloader proxy")

ALLOWED_ORIGINS = [
    "https://murphygo.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
}


def _validate_youtube_url(url: str) -> None:
    try:
        parsed = urlparse(url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="invalid URL") from e
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="URL must be http(s)")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="only YouTube hosts are allowed")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/download")
def download(url: str = Query(..., description="YouTube video URL")) -> FileResponse:
    _validate_youtube_url(url)
    tmpdir = tempfile.mkdtemp(prefix="ytdl-")
    opts = {
        "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
    except DownloadError as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise HTTPException(status_code=502, detail=f"download failed: {e}") from e

    filename = os.path.basename(filepath)
    return FileResponse(
        filepath,
        media_type="application/octet-stream",
        filename=filename,
        background=BackgroundTask(shutil.rmtree, tmpdir, ignore_errors=True),
    )
