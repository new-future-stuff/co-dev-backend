from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


@router.post("/authenticate")
async def authenticate(email: str, password: str):
    return await 
