from fastapi import APIRouter

from .chat import router as chat_router
from .personas import router as personas_router

router = APIRouter()

router.include_router(chat_router)
router.include_router(personas_router)
