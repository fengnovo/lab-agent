from fastapi import APIRouter, Depends

import app.services.user_service as user_service
from app.schemas.user import (
    UserUpdateRequest,
    UserQueryRequest,
    UserCreateRequest,
    UserAdminUpdateRequest,
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user, get_current_admin_user
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


# ==================== 管理员用户管理接口 ====================


@router.get("/page")
def get_user_page(
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """分页查询用户列表(管理员)"""
    query = UserQueryRequest(page=page, page_size=page_size, keyword=keyword)
    return Response.success(msg="查询成功", data=user_service.get_user_page(query, db))


@router.post("/add")
def create_user(
    data: UserCreateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """新增用户(管理员)"""
    return Response.success(msg="新增成功", data=user_service.create_user(data, db))


@router.put("/{user_id}")
def admin_update_user(
    user_id: int,
    data: UserAdminUpdateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """管理员更新用户信息(角色/状态/重置密码等)"""
    return Response.success(
        msg="更新成功", data=user_service.admin_update_user(user_id, data, db)
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """删除用户(管理员)"""
    user_service.delete_user(user_id, current_user, db)
    return Response.success(msg="删除成功")
