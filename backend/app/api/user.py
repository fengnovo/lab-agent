from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.common.response import Response

router = APIRouter(prefix="/user", tags=["用户信息"])


@router.get("/info")
def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return Response.success(
        msg="获取成功", data=UserResponse.model_validate(current_user)
    )
