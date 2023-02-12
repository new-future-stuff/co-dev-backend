from fastapi import APIRouter, Request

from sources.models import User


api_router = APIRouter(prefix="/api")


@api_router.get("/users")
async def list_users():
    return [

    ]


@api_router.get("/users/{user_id}")
async def get_user(user_id: int):
    return User.get(pk=user_id)
