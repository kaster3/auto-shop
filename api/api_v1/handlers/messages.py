from typing import Annotated

from fastapi import Depends, APIRouter

from dependencies.authentication.fastap_users import (
    current_active_user,
    current_active_superuser,
)
from core import settings, User
from core.database.schemas.user import UserRead

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)


@router.get(path="")
def get_user_messages(
    user: Annotated[User, Depends(current_active_user)],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }


@router.get(path="/secrets")
def get_superuser_messages(
    user: Annotated[User, Depends(current_active_superuser)],
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }
