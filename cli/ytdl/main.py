import sys

from yt_dlp import YoutubeDL


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: ytdl <url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "format": "best[ext=mp4]/best",
    }
    with YoutubeDL(opts) as ydl:
        ydl.download([url])
