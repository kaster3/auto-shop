__all__ = (
    "ProductCache",
    "router",
    "http_bearer",
    "api_router",
    "ProductService",
)

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core import settings
from api.api_v1.handlers.products import router as products_router
from api.api_v1.handlers.auth import router as auth_router
from api.api_v1.handlers.users import router as users_router
from api.api_v1.handlers.messages import router as messages_router
from .cache import ProductCache
from .services import ProductService


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

for api_router in auth_router, products_router, users_router, messages_router:
    router.include_router(api_router)
