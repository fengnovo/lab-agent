from app.models.user import User
from app.schemas.user import (
    UserResponse,
    UserUpdateRequest,
    PasswordResetRequest,
    UserQueryRequest,
    UserCreateRequest,
    UserAdminUpdateRequest,
)
from sqlalchemy.orm import Session
from app.utils.password import hash_password, verify_password
from app.common.exceptions import BusinessException


def get_user_info(user: User):
    """获取用户信息"""
    return UserResponse.model_validate(user)


def update_user_info(
    current_user: User, user_update_request: UserUpdateRequest, db: Session
):
    """更新用户信息"""
    print("更新用户信息", user_update_request)
    user_dict = user_update_request.model_dump(
        exclude_unset=True
    )  # 转换成字典，并排除未设置的字段, 只更新有值的字段
    for key, value in user_dict.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return UserResponse.model_validate(current_user)


def reset_password(data: PasswordResetRequest, current_user: User, db: Session):
    """重置密码"""
    print("重置密码", data)
    # 校验旧密码是否正确
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user or not verify_password(data.old_password, user.password):
        raise BusinessException(msg="旧密码错误")
    # 新密码不能和旧密码相同
    if data.new_password == data.old_password:
        raise BusinessException(msg="新密码不能和旧密码相同")
    # 更新密码
    user.password = hash_password(data.new_password)
    db.commit()


def get_user_page(query: UserQueryRequest, db: Session):
    """分页查询用户列表"""
    db_query = db.query(User)
    # 关键词模糊搜索: 用户名/姓名/手机号/邮箱
    if query.keyword:
        keyword = f"%{query.keyword}%"
        db_query = db_query.filter(
            User.username.like(keyword)
            | User.name.like(keyword)
            | User.phone.like(keyword)
            | User.email.like(keyword)
        )
    total = db_query.count()
    users = (
        db_query.order_by(User.id.desc())
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )
    return {
        "list": [UserResponse.model_validate(u) for u in users],
        "total": total,
        "page": query.page,
        "page_size": query.page_size,
    }


def create_user(data: UserCreateRequest, db: Session):
    """管理员新增用户"""
    # 校验用户名是否存在
    user = db.query(User).filter(User.username == data.username).first()
    if user:
        raise BusinessException(msg="用户名已存在")
    user_model = User(
        username=data.username,
        password=hash_password(data.password),
        name=data.name,
        role=data.role,
        phone=data.phone,
        email=data.email,
        status=1,
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return UserResponse.model_validate(user_model)


def admin_update_user(user_id: int, data: UserAdminUpdateRequest, db: Session):
    """管理员更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(msg="用户不存在")
    user_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    # 密码单独处理: 需要加密, 为空则不修改
    password = user_dict.pop("password", None)
    if password:
        user_dict["password"] = hash_password(password)
    for key, value in user_dict.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def delete_user(user_id: int, current_user: User, db: Session):
    """管理员删除用户"""
    # 不能删除自己
    if user_id == current_user.id:
        raise BusinessException(msg="不能删除当前登录账号")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(msg="用户不存在")
    db.delete(user)
    db.commit()
