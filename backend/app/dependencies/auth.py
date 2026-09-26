from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.database import SessionLocal, get_db
from app.utils.jwt import decode_access_token

# 定义OAuth2密码认证方案
# 用于在路由中依赖于当前用户的操作
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)  # 如果解析错误，会"msg": "Not authenticated",


def get_current_user(
    token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)
) -> User:
    """使用JWT Token鉴权当前用户"""
    try:
        payload = decode_access_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的Token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return user
