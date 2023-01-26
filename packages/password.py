from passlib.context import CryptContext

from config.settings.base import settings

pwd_context = CryptContext(schemes=[settings.HASH_ALGORITHM], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


