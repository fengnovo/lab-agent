from pydantic import BaseModel
from typing import Any

class Response(BaseModel):
    """统一响应模型"""

    code: int
    msg: str
    data: Any = None

    @classmethod
    def success(cls, data: Any = None, msg: str = "成功") -> "Response":
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def error(cls, msg: str, code: int = 500) -> "Response":
        return cls(code=code, msg=msg, data=None)
