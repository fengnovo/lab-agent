from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest, PasswordResetRequest
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
