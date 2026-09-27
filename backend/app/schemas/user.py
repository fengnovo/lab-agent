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


class UserQueryRequest(BaseModel):
    page: int = 1
    page_size: int = 10
    keyword: str | None = None  # 模糊搜索: 用户名/姓名/手机号/邮箱


class UserCreateRequest(BaseModel):
    username: str
    password: str
    name: str
    role: str = "student"
    phone: str | None = None
    email: str | None = None


class UserAdminUpdateRequest(BaseModel):
    name: str | None = None
    role: str | None = None
    phone: str | None = None
    email: str | None = None
    status: int | None = None
    password: str | None = None  # 管理员重置密码, 为空则不修改
