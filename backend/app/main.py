from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.api import router as api_router
from app.common.exceptions import (
    BusinessException,
    business_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    default_exception_handler,
)
from app.config import UPLOAD_DIR


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

# 注册自定义异常处理函数
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# 兜底的要放最后
app.add_exception_handler(Exception, default_exception_handler)
# 静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": "Hello World"}
