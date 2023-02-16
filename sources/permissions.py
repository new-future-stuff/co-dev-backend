from fastapi import HTTPException, status, Request
from functools import wraps
import datetime

from tortoise.exceptions import DoesNotExist

from sources.models import Token


def only_for_authorized_users(f):
    @wraps(f)
    async def checker(request: Request, *args, **kwargs):
        token = request.cookies["Token"]
        try:
            token = await Token.get(
                contents=token,
                expiration_time__lte=datetime.datetime.now()
            ).prefetch_related("owner")
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return await f(request, *args, user=token.owner, **kwargs)
    return checker
