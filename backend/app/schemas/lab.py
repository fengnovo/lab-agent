from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LabResponse(BaseModel):
    id: int
    name: str
    description: str | None
    img: str | None
    location: str | None
    capacity: int
    open_time: str | None
    close_time: str | None
    status: int
    created_at: datetime = Field(validation_alias="create_time")
    updated_at: datetime = Field(validation_alias="update_time")

    model_config = ConfigDict(
        from_attributes=True,
    )


class LabQueryRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    keyword: str | None = None  # 模糊搜索: 名称/位置/简介


class LabCreateRequest(BaseModel):
    name: str
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int = 0
    open_time: str | None = None
    close_time: str | None = None
    status: int = 1


class LabUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    img: str | None = None
    location: str | None = None
    capacity: int | None = None
    open_time: str | None = None
    close_time: str | None = None
    status: int | None = None
