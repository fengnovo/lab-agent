from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.lab_service as lab_service
from app.schemas.lab import LabQueryRequest, LabCreateRequest, LabUpdateRequest
from app.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user, get_current_admin_user
from app.common.response import Response

router = APIRouter(prefix="/lab", tags=["实验室管理"])


@router.get("/page")
def get_lab_page(
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """分页查询实验室列表(登录即可查看)"""
    query = LabQueryRequest(page=page, page_size=page_size, keyword=keyword)
    return Response.success(msg="查询成功", data=lab_service.get_lab_page(query, db))


@router.get("/{lab_id}")
def get_lab_detail(
    lab_id: int,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """实验室详情"""
    return Response.success(msg="查询成功", data=lab_service.get_lab_detail(lab_id, db))


@router.post("/add")
def create_lab(
    data: LabCreateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """新增实验室(管理员)"""
    return Response.success(msg="新增成功", data=lab_service.create_lab(data, db))


@router.put("/{lab_id}")
def update_lab(
    lab_id: int,
    data: LabUpdateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """更新实验室信息(管理员)"""
    return Response.success(
        msg="更新成功", data=lab_service.update_lab(lab_id, data, db)
    )


@router.delete("/{lab_id}")
def delete_lab(
    lab_id: int,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """删除实验室(管理员)"""
    lab_service.delete_lab(lab_id, db)
    return Response.success(msg="删除成功")
