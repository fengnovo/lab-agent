from pydantic import BaseModel


class FileRequest(BaseModel):
    original_name: str
    size: int
    url: str
    disk_name: str
