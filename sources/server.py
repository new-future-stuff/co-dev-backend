from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path


STATIC = Path("../static")


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
async def main_page():
    return FileResponse(STATIC / "main.html")
