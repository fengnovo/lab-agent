from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EquipmentResponse(BaseModel):
    id: int
    lab_id: int
    lab_name: str | None = None  # 所属实验室名称, 由 service 填充
    name: str
    description: str | None
    img: str | None
    spec: str | None
    quantity: int
    status: int
    created_at: datetime = Field(validation_alias="create_time")
    updated_at: datetime = Field(validation_alias="update_time")

    model_config = ConfigDict(
        from_attributes=True,
    )


class EquipmentQueryRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    keyword: str | None = None  # 模糊搜索: 名称/型号规格/说明
    lab_id: int | None = None  # 按所属实验室筛选


class EquipmentCreateRequest(BaseModel):
    lab_id: int
    name: str
    description: str | None = None
    img: str | None = None
    spec: str | None = None
    quantity: int = 1
    status: int = 1


class EquipmentUpdateRequest(BaseModel):
    lab_id: int | None = None
    name: str | None = None
    description: str | None = None
    img: str | None = None
    spec: str | None = None
    quantity: int | None = None
    status: int | None = None
