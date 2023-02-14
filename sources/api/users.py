from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from secrets import token_bytes
import datetime
from tortoise.exceptions import IntegrityError

from sources.models import User
from sources.secrets import encrypt_password


router = APIRouter(prefix="/api")


@router.get("/users")
async def list_users():
    return [
        {
            "id": user.id,
            "textual_id": user.textual_id,
            "name": user.name,
            "join_date": user.join_date,
        }
        for user in await User.all().order_by("-join_date")
    ]


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get(pk=user_id).prefetch_related("skills")
    return {
        "textual_id": user.textual_id,
        "name": user.name,
        "skills": [{"name": skill.name} for skill in user.skills],
        "join_date": user.join_date,
    }


class UserData(BaseModel):
    name: str
    password: str
    textual_id: str
    skill_ids: List[int]


@router.post("/users")
async def create_user(user: UserData):
    salt = token_bytes(16)
    try:
        await User.create(
            hashed_password=encrypt_password(user.password, salt),
            password_hash_salt=salt,
            textual_id=user.textual_id,
            name=user.name,
            skills=user.skill_ids,
            join_date=datetime.datetime.now(),
        )
    except IntegrityError:

