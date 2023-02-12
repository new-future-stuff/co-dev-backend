from fastapi import HTTPException, status, Request
from functools import wraps


def only_for_authorized_users(f):
    @wraps(f)
    async def checker(request: Request):
        token = request.cookies["Token"]
        if token
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return checker
