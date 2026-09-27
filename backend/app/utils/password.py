import bcrypt
from fastapi import HTTPException


# 在注册时对密码进行哈希加密
def hash_password(password: str) -> str:
    """对密码哈希加密"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# 在登录时验证密码
def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
