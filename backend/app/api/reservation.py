from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.reservation_service as reservation_service
from app.common.response import Response
from app.database import get_db
from app.dependencies.auth import get_current_admin_user, get_current_user
from app.models.user import User
from app.schemas.reservation import (
    ReservationAuditRequest,
    ReservationCreateRequest,
    ReservationQueryRequest,
)

router = APIRouter(prefix="/reservation", tags=["预约管理"])


@router.post("/add")
def create_reservation(
    data: ReservationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交预约(登录用户)"""
    return Response.success(
        msg="预约提交成功, 请等待审核",
        data=reservation_service.create_reservation(db, current_user, data),
    )


@router.get("/my")
def get_my_reservations(
    page: int = 1,
    page_size: int = 10,
    status: int | None = None,
    date: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查询我的预约"""
    query = ReservationQueryRequest(
        page=page, page_size=page_size, status=status, date=date
    )
    return Response.success(
        msg="查询成功",
        data=reservation_service.get_my_reservation_page(db, current_user, query),
    )


@router.put("/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """取消我的预约"""
    reservation_service.cancel_reservation(db, current_user, reservation_id)
    return Response.success(msg="取消成功")


@router.get("/page")
def get_reservation_page(
    page: int = 1,
    page_size: int = 10,
    status: int | None = None,
    keyword: str | None = None,
    date: str | None = None,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """管理员分页查询全部预约"""
    query = ReservationQueryRequest(
        page=page, page_size=page_size, status=status, keyword=keyword, date=date
    )
    return Response.success(
        msg="查询成功", data=reservation_service.get_reservation_page(db, query)
    )


@router.put("/{reservation_id}/audit")
def audit_reservation(
    reservation_id: int,
    data: ReservationAuditRequest,
    _: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """管理员审核预约(1 通过 / 2 拒绝)"""
    reservation_service.audit_reservation(db, reservation_id, data)
    return Response.success(msg="审核成功")
