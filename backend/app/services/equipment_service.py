from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.equipment import Equipment
from app.models.lab import Lab
from app.schemas.equipment import (
    EquipmentResponse,
    EquipmentQueryRequest,
    EquipmentCreateRequest,
    EquipmentUpdateRequest,
)


def _equipment_response(eq: Equipment) -> EquipmentResponse:
    """转换响应模型, 并填充所属实验室名称"""
    resp = EquipmentResponse.model_validate(eq)
    resp.lab_name = eq.lab.name if eq.lab else None
    return resp


def _check_lab_exists(lab_id: int, db: Session):
    """校验所属实验室是否存在"""
    if not db.query(Lab).filter(Lab.id == lab_id).first():
        raise BusinessException(msg="所属实验室不存在")


def get_equipment_page(query: EquipmentQueryRequest, db: Session):
    """分页查询设备列表"""
    db_query = db.query(Equipment)
    # 关键词模糊搜索: 名称/型号规格/说明
    if query.keyword:
        keyword = f"%{query.keyword}%"
        db_query = db_query.filter(
            Equipment.name.like(keyword)
            | Equipment.spec.like(keyword)
            | Equipment.description.like(keyword)
        )
    # 按所属实验室筛选
    if query.lab_id:
        db_query = db_query.filter(Equipment.lab_id == query.lab_id)
    total = db_query.count()
    equipments = (
        db_query.order_by(Equipment.id.desc())
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )
    return {
        "list": [_equipment_response(eq) for eq in equipments],
        "total": total,
        "page": query.page,
        "page_size": query.page_size,
    }


def create_equipment(data: EquipmentCreateRequest, db: Session):
    """新增设备"""
    _check_lab_exists(data.lab_id, db)
    eq = Equipment(**data.model_dump())
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return _equipment_response(eq)


def update_equipment(equipment_id: int, data: EquipmentUpdateRequest, db: Session):
    """更新设备信息"""
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise BusinessException(msg="设备不存在")
    update_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    if "lab_id" in update_dict:
        _check_lab_exists(update_dict["lab_id"], db)
    for key, value in update_dict.items():
        setattr(eq, key, value)
    db.commit()
    db.refresh(eq)
    return _equipment_response(eq)


def delete_equipment(equipment_id: int, db: Session):
    """删除设备"""
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise BusinessException(msg="设备不存在")
    db.delete(eq)
    db.commit()
