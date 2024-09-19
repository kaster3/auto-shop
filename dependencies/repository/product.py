from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from core import db_helper
from api.api_v1.repository import ProductRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_product_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)]
) -> ProductRepository:
    return ProductRepository(session=session)
