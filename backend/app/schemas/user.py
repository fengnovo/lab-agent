from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# 类型自动校验
class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    phone: str
    avatar: str | None
    status: int
    email: str | None
    created_at: datetime = Field(validation_alias="create_time")
    updated_at: datetime = Field(validation_alias="update_time")

    model_config = ConfigDict(
        from_attributes=True,
    )
