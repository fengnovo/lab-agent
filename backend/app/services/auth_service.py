from app.schemas.auth import LoginRequest, RegisterRequest
from app.models.user import User
from app.database import SessionLocal
from app.utils.password import verify_password, hash_password
from app.utils.jwt import create_access_token
from app.common.exceptions import BusinessException
from app.schemas.user import UserResponse


def login(data: LoginRequest, db: SessionLocal):
    """登录"""
    print(data)
    # 根据用户名查询用户
    user = db.query(User).filter(User.username == data.username).first()
    # 校验用户是否存在
    if not user:
        raise BusinessException(msg="用户不存在")
    # 校验密码是否正确
    if not verify_password(data.password, user.password):
        raise BusinessException(msg="密码错误")
    # 校验用户账号是否被禁用
    if user.status != 1:
        raise BusinessException(msg="用户账号已被禁用")
    # 创建JWT Token
    token = create_access_token(user.id)
    # 返回登录成功响应
    return {"token": token, "user": UserResponse.model_validate(user)}


def register(data: RegisterRequest, db: SessionLocal):
    """注册"""
    # 校验密码是否为空
    if not data.password:
        raise BusinessException(msg="密码不能为空")
    # 校验用户名是否存在
    user = db.query(User).filter(User.username == data.username).first()
    if user:
        raise BusinessException(msg="用户名已存在")

    user_model = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name or data.username,
        status=1,
        role="student",
    )

    # 保存用户到数据库
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
