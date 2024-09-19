from fastapi import APIRouter

from core import settings
from dependencies.authentication.fastap_users import fastapi_users
from core.database.schemas.user import UserUpdate, UserRead


router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me, /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
