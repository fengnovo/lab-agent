from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "用户信息表"}
    username: Mapped[str] = mapped_column(String(50), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")
    name: Mapped[str] = mapped_column(String(50), comment="姓名")
    role: Mapped[str] = mapped_column(
        String(50), comment="角色: student, admin", nullable=False
    )
    email: Mapped[str | None] = mapped_column(String(50), comment="邮箱")
    phone: Mapped[str | None] = mapped_column(String(50), comment="手机号")
    avatar: Mapped[str | None] = mapped_column(String(50), comment="头像")
    status: Mapped[int] = mapped_column(default=1, comment="状态: 0-禁用, 1-正常")
