from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# 类型自动校验
class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str
    phone: str | None
    avatar: str | None
    email: str | None
    status: int
    created_at: datetime = Field(validation_alias="create_time")
    updated_at: datetime = Field(validation_alias="update_time")

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserUpdateRequest(BaseModel):
    username: str | None = None  # 一定要默认赋值None，否则会报错
    password: str | None = None
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    avatar: str | None = None


class PasswordResetRequest(BaseModel):
    new_password: str
    old_password: str
