from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.common.response import Response


class BusinessException(Exception):
    """业务异常"""

    def __init__(self, msg: str, code: int = 500):
        self.msg = msg
        self.code = code
        super().__init__(msg)


async def business_exception_handler(request: Request, exc: BusinessException):
    """处理业务异常"""
    return JSONResponse(
        content=Response.error(msg=exc.msg, code=exc.code).dict(), status_code=200
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    return JSONResponse(
        content=Response.error(msg=exc.detail, code=exc.status_code).dict(),
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """参数校验异常"""
    return JSONResponse(
        content=Response.error(msg="请求参数校验失败", code=422).dict(), status_code=422
    )


async def default_exception_handler(request: Request, exc: Exception):
    """默认异常处理"""
    return JSONResponse(
        content=Response.error(msg="服务器内部错误", code=500).dict(), status_code=500
    )
