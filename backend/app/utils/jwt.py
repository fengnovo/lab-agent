import jwt
from app.config import settings
from datetime import datetime, timedelta
from fastapi import HTTPException


def create_access_token(user_id: int) -> str:
    """创建JWT Token"""
    expire = datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id, "exp": expire} # exp是固定的，不能改变
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """解码JWT Token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token无效")
    return payload