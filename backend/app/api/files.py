import os
from pathlib import Path
from fastapi import APIRouter, File, UploadFile
import time
import uuid
import shutil
from app.common.exceptions import BusinessException
from app.common.response import Response
from app.schemas.file import FileRequest
from app.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR

router = APIRouter(prefix="/files", tags=["文件管理"])


@router.post("/upload")
def upload_files(file: UploadFile = File(...)):
    """上传文件"""
    if not file.filename:
        raise BusinessException(msg="文件名不能为空")

    # 原始文件名
    original_filename = os.path.basename(file.filename)
    # 文件扩展名校验
    ext = Path(original_filename).suffix.lower()
    if not ext:
        raise BusinessException(msg="文件扩展名不能为空")
    if not ext in ALLOWED_EXTENSIONS:
        raise BusinessException(msg=f"文件格式错误，不支持{ext}")

    # 文件大小校验
    if file.size > MAX_FILE_SIZE:
        raise BusinessException(msg=f"文件大小不能超过 {MAX_FILE_SIZE/1024/1024}MB")

    # 生成文件名
    new_filename = f"{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}{ext}"  # 时间戳_随机数_扩展名 ，随机数取前8位

    save_path = UPLOAD_DIR / new_filename

    # 保存文件到服务器, 流式写入
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return Response.success(
        data=FileRequest(
            original_name=original_filename,
            size=file.size,
            url=f"/uploads/{new_filename}",
            disk_name=new_filename,
        )
    )
