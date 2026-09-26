from fastapi import APIRouter, Depends, HTTPException

from app.schemas.auth import LoginRequest
from app.schemas.user import UserResponse
from app.models.user import User
from app.database import SessionLocal, get_db
from app.utils.password import verify_password
from app.utils.jwt import create_access_token
from app.common.response import Response
from app.common.exceptions import BusinessException
from app.schemas.auth import LoginResponse


router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login")
def login(data: LoginRequest, db: SessionLocal = Depends(get_db)):
    """登录"""
    print(data)
    # 根据用户名查询用户
    user = db.query(User).filter(User.username == data.username).first()
    # 校验用户是否存在
    if not user:
        raise BusinessException(msg="用户不存在")
    # 校验密码是否正确
    if not verify_password(data.password, user.password):
        raise BusinessException(msg="密码错误")
    # 校验用户账号是否被禁用
    if user.status != 1:
        raise BusinessException(msg="用户账号已被禁用")
    # 创建JWT Token
    token = create_access_token(user.id)
    # 返回登录成功响应
    return Response.success(msg="登录成功", data = LoginResponse(token=token, user=UserResponse.model_validate(user)))