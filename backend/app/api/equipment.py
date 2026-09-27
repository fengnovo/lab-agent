from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.equipment_service as equipment_service
from app.schemas.equipment import (
    EquipmentQueryRequest,
    EquipmentCreateRequest,
    EquipmentUpdateRequest,
)
from app.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user, get_current_admin_user
from app.common.response import Response

router = APIRouter(prefix="/equipment", tags=["实验室设备管理"])


@router.get("/page")
def get_equipment_page(
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    lab_id: int | None = None,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """分页查询设备列表(登录即可查看)"""
    query = EquipmentQueryRequest(
        page=page, page_size=page_size, keyword=keyword, lab_id=lab_id
    )
    return Response.success(
        msg="查询成功", data=equipment_service.get_equipment_page(query, db)
    )


@router.post("/add")
def create_equipment(
    data: EquipmentCreateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """新增设备(管理员)"""
    return Response.success(
        msg="新增成功", data=equipment_service.create_equipment(data, db)
    )


@router.put("/{equipment_id}")
def update_equipment(
    equipment_id: int,
    data: EquipmentUpdateRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """更新设备信息(管理员)"""
    return Response.success(
        msg="更新成功", data=equipment_service.update_equipment(equipment_id, data, db)
    )


@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: int,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """删除设备(管理员)"""
    equipment_service.delete_equipment(equipment_id, db)
    return Response.success(msg="删除成功")
