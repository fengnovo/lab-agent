from fastapi import APIRouter
from .user import router as user_router
from .auth import router as auth_router
from .files import router as files_router

router = APIRouter(
    prefix="/api",
    tags=["API"],
)
router.include_router(files_router)
router.include_router(user_router)
router.include_router(auth_router)
