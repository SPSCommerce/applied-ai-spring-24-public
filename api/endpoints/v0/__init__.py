from fastapi import APIRouter

from .chat import router as chat

router = APIRouter()

router.include_router(chat)
