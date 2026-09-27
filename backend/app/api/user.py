from fastapi import APIRouter, Depends

import app.services.user_service as user_service
from app.schemas.user import UserUpdateRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.common.response import Response
from app.schemas.user import PasswordResetRequest

router = APIRouter(prefix="/user", tags=["用户信息"])


@router.get("/info")
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return Response.success(
        msg="获取成功", data=user_service.get_user_info(current_user)
    )


@router.put("/update")
def update_user_info(
    user_update_request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新用户信息"""
    return Response.success(
        msg="更新成功",
        data=user_service.update_user_info(current_user, user_update_request, db),
    )


@router.post("/reset-password")
def reset_password(
    data: PasswordResetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """重置密码"""
    # 调用重置密码服务
    user_service.reset_password(data, current_user, db)
    # 返回重置密码成功响应
    return Response.success(msg="重置密码成功")
