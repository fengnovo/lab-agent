from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.equipment import Equipment
from app.models.lab import Lab
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import (
    ReservationAuditRequest,
    ReservationCreateRequest,
    ReservationQueryRequest,
    ReservationResponse,
)

# 有效状态
STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED, STATUS_CANCELED = 0, 1, 2, 3


def _to_response(r: Reservation) -> ReservationResponse:
    resp = ReservationResponse.model_validate(r)
    resp.username = r.user.username if r.user else None
    resp.lab_name = r.lab.name if r.lab else None
    resp.equipment_name = r.equipment.name if r.equipment else None
    return resp


def _validate_hhmm(value: str, label: str):
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise BusinessException(msg=f"{label}格式应为 HH:MM")


def create_reservation(db: Session, current_user: User, data: ReservationCreateRequest):
    """创建预约记录"""
    # 1. 时间格式与先后顺序
    _validate_hhmm(data.start_time, "开始时间")
    _validate_hhmm(data.end_time, "结束时间")
    if data.end_time <= data.start_time:
        raise BusinessException(msg="结束时间必须晚于开始时间")
    try:
        reserve_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    except ValueError:
        raise BusinessException(msg="预约日期格式应为 YYYY-MM-DD")

    # 2. 不能预约已经过去的时间
    start_dt = datetime.strptime(f"{data.date} {data.start_time}", "%Y-%m-%d %H:%M")
    if start_dt <= datetime.now():
        raise BusinessException(msg="不能预约已经过去的时间")

    # 3. 实验室存在且开放
    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise BusinessException(msg="实验室不存在")
    if lab.status != 1:
        raise BusinessException(msg="实验室已关闭, 暂不可预约")

    # 4. 预约时段必须在实验室开放时间内
    if lab.open_time and data.start_time < lab.open_time:
        raise BusinessException(
            msg=f"预约开始时间不能早于实验室开放时间 {lab.open_time}"
        )
    if lab.close_time and data.end_time > lab.close_time:
        raise BusinessException(
            msg=f"预约结束时间不能晚于实验室关闭时间 {lab.close_time}"
        )

    # 5. equipment_id 不为空表示预约的是实验室设备
    if data.equipment_id:
        equipment = (
            db.query(Equipment).filter(Equipment.id == data.equipment_id).first()
        )
        if not equipment:
            raise BusinessException(msg="实验室设备不存在")
        if equipment.lab_id != data.lab_id:
            raise BusinessException(msg="该设备不属于所选实验室")
        if equipment.status != 1:
            raise BusinessException(msg="实验室设备正在维修, 暂不可预约")

    # 6. 时段冲突校验: 同一天、同一实验室, 待审核/已通过的预约时间不重叠
    #    整实验室预约与任何预约互斥; 设备预约与同设备预约或整实验室预约互斥;
    #    不同设备同一时段可以同时预约
    query = db.query(Reservation).filter(
        Reservation.lab_id == data.lab_id,
        Reservation.date == data.date,
        Reservation.status.in_([STATUS_PENDING, STATUS_APPROVED]),
        Reservation.start_time < data.end_time,
        Reservation.end_time > data.start_time,
    )
    if data.equipment_id:
        # 预约设备: 冲突对象为 整实验室预约 或 同一设备的预约
        query = query.filter(
            or_(
                Reservation.equipment_id.is_(None),
                Reservation.equipment_id == data.equipment_id,
            )
        )
    # equipment_id 为空(预约整间实验室): 不加设备过滤, 与该实验室任何预约冲突
    if query.first():
        raise BusinessException(msg="该时段已被预约, 请选择其他时间")

    reservation = Reservation(
        user_id=current_user.id,
        lab_id=data.lab_id,
        equipment_id=data.equipment_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        remark=data.remark,
        status=STATUS_PENDING,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return _to_response(reservation)


def get_my_reservation_page(
    db: Session, current_user: User, query: ReservationQueryRequest
):
    """查询当前用户的预约"""
    return _get_page(
        db,
        query,
        base_filter=Reservation.user_id == current_user.id,
    )


def get_reservation_page(db: Session, query: ReservationQueryRequest):
    """管理员查询全部预约"""
    extra = None
    if query.keyword:
        keyword = f"%{query.keyword}%"
        extra = or_(Lab.name.like(keyword), User.username.like(keyword))
    return _get_page(db, query, base_filter=None, extra_filter=extra)


def _get_page(
    db: Session, query: ReservationQueryRequest, base_filter, extra_filter=None
):
    db_query = (
        db.query(Reservation)
        .join(Lab, Reservation.lab_id == Lab.id)
        .join(User, Reservation.user_id == User.id)
    )
    if base_filter is not None:
        db_query = db_query.filter(base_filter)
    if extra_filter is not None:
        db_query = db_query.filter(extra_filter)
    if query.status is not None:
        db_query = db_query.filter(Reservation.status == query.status)
    if query.date:
        db_query = db_query.filter(Reservation.date == query.date)
    total = db_query.count()
    rows = (
        db_query.order_by(Reservation.id.desc())
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )
    return {
        "list": [_to_response(r) for r in rows],
        "total": total,
        "page": query.page,
        "page_size": query.page_size,
    }


def cancel_reservation(db: Session, current_user: User, reservation_id: int):
    """用户取消自己的预约(待审核/已通过可取消)"""
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise BusinessException(msg="预约记录不存在")
    if r.user_id != current_user.id:
        raise BusinessException(msg="只能取消自己的预约")
    if r.status in (STATUS_REJECTED, STATUS_CANCELED):
        raise BusinessException(msg="该预约已结束, 无法取消")
    r.status = STATUS_CANCELED
    db.commit()


def audit_reservation(db: Session, reservation_id: int, data: ReservationAuditRequest):
    """管理员审核预约(1 通过 / 2 拒绝)"""
    if data.status not in (STATUS_APPROVED, STATUS_REJECTED):
        raise BusinessException(msg="审核状态只能是通过或拒绝")
    r = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not r:
        raise BusinessException(msg="预约记录不存在")
    if r.status != STATUS_PENDING:
        raise BusinessException(msg="该预约已审核, 请勿重复操作")

    # 通过时再次校验时段冲突, 防止多个待审核预约通过后撞车
    if data.status == STATUS_APPROVED:
        conflict_query = db.query(Reservation).filter(
            Reservation.id != r.id,
            Reservation.lab_id == r.lab_id,
            Reservation.date == r.date,
            Reservation.status == STATUS_APPROVED,
            Reservation.start_time < r.end_time,
            Reservation.end_time > r.start_time,
        )
        if r.equipment_id:
            conflict_query = conflict_query.filter(
                or_(
                    Reservation.equipment_id.is_(None),
                    Reservation.equipment_id == r.equipment_id,
                )
            )
        if conflict_query.first():
            raise BusinessException(msg="该时段存在冲突的已通过预约, 无法通过")

    r.status = data.status
    if data.remark:
        r.remark = data.remark
    db.commit()
