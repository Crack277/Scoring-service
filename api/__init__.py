from fastapi import APIRouter

from api.views import router as client_router

router = APIRouter(prefix="/v1")
router.include_router(client_router)
