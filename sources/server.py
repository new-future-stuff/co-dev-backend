from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
import api


STATIC = Path("../static")

templates = Jinja2Templates("../templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.include_router(api.router, prefix="/api")


@app.get("/")
async def main_page(request: Request):
    user = api.get_user(request, required=False)
    return templates.TemplateResponse("main.jinja2", context={"user": user, "request": request})


@app.get("/registration")
async def registration():
    return FileResponse(STATIC / "registration.html")


@app.get("/authentication")
async def authentication():
    return FileResponse(STATIC / "authentication.html")


@app.get("/skills")
async def skills(request: Request):
    user = api.get_user(request, required=False)
    return templates.TemplateResponse("skills.jinja2", context={"user": user, "request": request})


@app.get("/projects")
async def projects(request: Request):
    user = api.get_user(request, required=True)
    return templates.TemplateResponse("projects.jinja2", context={"user": user, "request": request})
