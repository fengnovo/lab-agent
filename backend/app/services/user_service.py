from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest
from sqlalchemy.orm import Session


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
