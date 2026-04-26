import os
import sys

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def _progress_hook(d: dict) -> None:
    if d.get("status") == "downloading":
        pct = (d.get("_percent_str") or "").strip()
        speed = (d.get("_speed_str") or "").strip()
        sys.stderr.write(f"\r  {pct} at {speed}   ")
        sys.stderr.flush()
    elif d.get("status") == "finished":
        sys.stderr.write("\n")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ytdl <url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    print(f"ytdl: downloading {url}", file=sys.stderr)
    opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": False,
        "noprogress": True,
        "progress_hooks": [_progress_hook],
    }
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
    except DownloadError as e:
        print(f"ytdl: download failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(os.path.abspath(filepath))
