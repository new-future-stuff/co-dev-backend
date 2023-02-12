from passlib.context import CryptContext
from datetime import timedelta
from tortoise.exceptions import DoesNotExist
from jose import JWTError, jwt

from sources.models import User

import os
import datetime

ACCESS_TOKEN_EXPIRATION_TIME = timedelta(minutes=30)
JWT_ENCRYPTION_ALGORITHM = "HS256"

JWT_PRIVATE_KEY = os.environ["JWT_PRIVATE_KEY"]

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashes_password):
    return password_context.verify(plain_password, hashes_password)


def get_password_hash(password):
    return password_context.hash(password)


class UsernameOrPasswordAreIncorrect(Exception):
    pass


async def authenticate_user(textual_id: str, plain_password: str):
    try:
        user = await User.get(textual_id=textual_id)
    except DoesNotExist:
        raise UsernameOrPasswordAreIncorrect
    if verify_password(plain_password, user.hashed_password):
        return user
    else:
        raise UsernameOrPasswordAreIncorrect


def create_access_token(user_id: int):
    return jwt.encode(
        {
            "exp": int((datetime.datetime.now() + ACCESS_TOKEN_EXPIRATION_TIME).timestamp()),
            "user_id": user_id,
        },
        JWT_PRIVATE_KEY,
        algorithm=JWT_ENCRYPTION_ALGORITHM,
    )


class TokenIsInvalid(Exception):
    pass


def get_user_id_from_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_PRIVATE_KEY)
    except JWTError:
        raise TokenIsInvalid
    return payload["user_id"]
