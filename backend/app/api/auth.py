from fastapi import APIRouter, Depends, HTTPException

from app.schemas.auth import LoginRequest, RegisterRequest
from app.database import SessionLocal, get_db
from app.common.response import Response
from app.schemas.auth import LoginResponse, RegisterResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login")
def login(data: LoginRequest, db: SessionLocal = Depends(get_db)):
    """登录"""
    # 调用登录服务
    result = auth_service.login(data, db)
    # 返回登录成功响应
    return Response.success(
        msg="登录成功",
        data=LoginResponse(**result),
    )


@router.post("/register")
def register(data: RegisterRequest, db: SessionLocal = Depends(get_db)):
    """注册"""
    # 调用注册服务
    result = auth_service.register(data, db)
    # 返回注册成功响应
    return Response.success(msg="注册成功")
