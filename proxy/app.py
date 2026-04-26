from fastapi import FastAPI, Query

app = FastAPI(title="youtube-downloader proxy")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/download")
def download(url: str = Query(..., description="YouTube video URL")) -> dict[str, str]:
    return {"url": url, "status": "stub"}
