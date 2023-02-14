from passlib.hash import bcrypt_sha256


def encrypt_password(password: str, salt: bytes):
    return bcrypt_sha256.encrypt(password.encode(password) + salt)
