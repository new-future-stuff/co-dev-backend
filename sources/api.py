from fastapi import APIRouter, HTTPException, Request, status, Response, Form
from secrets import token_urlsafe

from fastapi.responses import RedirectResponse


router = APIRouter()


def _add_user(password, token, email):
    users[email] = {"password": password, "token": token, "projects": [], "skills": []}


users = {}
_add_user("pass", "tok", "mail")

last_project_id = 0


def get_user(request: Request, *, required: bool):
    try:
        token = request.cookies["token"]
    except KeyError:
        pass
    else:
        for _email, user in users.items():
            if user["token"] == token:
                return user
    if required:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/authenticate")
async def authenticate(email: str = Form(), password: str = Form()):
    try:
        user = users[email]
    except KeyError:
        pass
    else:
        if user["password"] == password:
            token = user["token"]
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie("token", token)
            return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/register")
async def register(response: Response, email: str = Form(), password: str = Form()):
    if email in users:
        return HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        token = token_urlsafe(128)
        _add_user(password, token, email)
        response.set_cookie("token", token)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/set_skills")
async def set_skills(request: Request, skills: str = Form()):
    user = get_user(request, required=True)
    skills: list = skills.split()
    user["skills"] = skills
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/create_project")
async def create_project(request: Request, title: str):
    user = get_user(request, required=True)
    user["projects"].append({"id": last_project_id, "title": title})
    last_project_id += 1
    return RedirectResponse(url="/projects", status_code=status.HTTP_303_SEE_OTHER)
