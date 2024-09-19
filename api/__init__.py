__all__ = (
    "ProductCache",
    "router",
)


from fastapi import APIRouter


from core import settings
from .api_v1 import router as router_api_v1, ProductCache


router = APIRouter(prefix=settings.api.prefix)

router.include_router(router=router_api_v1)
