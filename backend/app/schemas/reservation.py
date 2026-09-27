from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    username: str | None = None  # 预约人姓名, 由 service 填充
    lab_id: int
    lab_name: str | None = None
    equipment_id: int | None = None
    equipment_name: str | None = None
    date: str
    start_time: str
    end_time: str
    remark: str | None
    status: int
    created_at: datetime = Field(validation_alias="create_time")

    model_config = ConfigDict(from_attributes=True)


class ReservationQueryRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    status: int | None = None
    keyword: str | None = None  # 实验室名/预约人名
    date: str | None = None


class ReservationCreateRequest(BaseModel):
    lab_id: int
    equipment_id: int | None = None  # 空表示只预约实验室
    date: str  # 预约日期, 格式 YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    remark: str | None = None


class ReservationAuditRequest(BaseModel):
    """管理员审核: 1 通过, 2 拒绝"""
    status: int
    remark: str | None = None
