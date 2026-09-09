from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
static = Path(__file__).parent / "dist"


@app.get("/api/health")
def health():
    return {"status": "ok"}


# API errors never fall through to the SPA's HTML response.
@app.api_route("/api/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
@app.api_route("/api", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
def unknown_api(rest: str = ""):
    raise HTTPException(status_code=404, detail="API route not found")


if (static / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=static / "assets"), name="assets")


@app.get("/{route:path}")
def frontend(route: str):
    candidate = (static / route).resolve()
    if not candidate.is_relative_to(static.resolve()):
        raise HTTPException(status_code=404)
    if candidate.is_file():
        return FileResponse(candidate)
    if Path(route).suffix or not (static / "index.html").is_file():
        raise HTTPException(status_code=404)
    return FileResponse(static / "index.html")
