from pydantic import BaseModel
from app.schemas.user import UserResponse


# 类型自动校验
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse
