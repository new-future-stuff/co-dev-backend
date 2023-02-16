from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from secrets import token_bytes
import datetime
from tortoise.exceptions import IntegrityError

from sources.models import TelegramUserData, User, WebsiteUserData
from sources.secrets import encrypt_password


router = APIRouter(prefix="/api")


@router.get("/users")
async def list_users():
    return [
        {
            "id": user.id,
            "name": user.name,
            "join_date": user.join_date,
        }
        for user in await User.all().order_by("-join_date")
    ]


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get(pk=user_id).prefetch_related("skills")
    return {
        "name": user.name,
        "skills": [{"name": skill.name} for skill in user.skills],
        "join_date": user.join_date,
    }


class UserData(BaseModel):
    name: str
    password: str
    email: str


async def create_telegram_user(name: str, telegram_id: int):
    user = await User.create(
        name=name,
        skills=[],
        join_date=datetime.datetime.now(),
    )
    try:
        await TelegramUserData(telegram_id=telegram_id, user=user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": "telegram id already taken"}
        )


@router.post("/users")
async def create_website_user(user: UserData):
    salt = token_bytes(16)
    user_record = await User.create(
        name=user.name,
        skills=[],
        join_date=datetime.datetime.now(),
    )
    try:
        await WebsiteUserData(
            hashed_password=encrypt_password(user.password, salt),
            password_hash_salt=salt,
            email=user.email,
            user=user_record,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": "email already taken"},
        )
