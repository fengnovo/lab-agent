from sqlalchemy.orm import Session

from app.common.exceptions import BusinessException
from app.models.lab import Lab
from app.schemas.lab import (
    LabResponse,
    LabQueryRequest,
    LabCreateRequest,
    LabUpdateRequest,
)


def get_lab_page(query: LabQueryRequest, db: Session):
    """分页查询实验室列表"""
    db_query = db.query(Lab)
    # 关键词模糊搜索: 名称/位置/简介
    if query.keyword:
        keyword = f"%{query.keyword}%"
        db_query = db_query.filter(
            Lab.name.like(keyword)
            | Lab.location.like(keyword)
            | Lab.description.like(keyword)
        )
    total = db_query.count()
    labs = (
        db_query.order_by(Lab.id.desc())
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )
    return {
        "list": [LabResponse.model_validate(lab) for lab in labs],
        "total": total,
        "page": query.page,
        "page_size": query.page_size,
    }


def get_lab_detail(lab_id: int, db: Session):
    """获取实验室详情"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(msg="实验室不存在")
    return LabResponse.model_validate(lab)


def create_lab(data: LabCreateRequest, db: Session):
    """新增实验室"""
    # 校验名称是否重复
    lab = db.query(Lab).filter(Lab.name == data.name).first()
    if lab:
        raise BusinessException(msg="实验室名称已存在")
    lab_model = Lab(**data.model_dump())
    db.add(lab_model)
    db.commit()
    db.refresh(lab_model)
    return LabResponse.model_validate(lab_model)


def update_lab(lab_id: int, data: LabUpdateRequest, db: Session):
    """更新实验室信息"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(msg="实验室不存在")
    update_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    # 校验名称是否与其他实验室重复
    if "name" in update_dict and update_dict["name"] != lab.name:
        exists = db.query(Lab).filter(Lab.name == update_dict["name"]).first()
        if exists:
            raise BusinessException(msg="实验室名称已存在")
    for key, value in update_dict.items():
        setattr(lab, key, value)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)


def delete_lab(lab_id: int, db: Session):
    """删除实验室"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(msg="实验室不存在")
    db.delete(lab)
    db.commit()
