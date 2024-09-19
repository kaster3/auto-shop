from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from dependencies.repository.product import get_product_repository
from dependencies.caches.product import get_product_cache_repository
from api.api_v1.services.service_products import ProductService


if TYPE_CHECKING:
    from api.api_v1.repository import ProductRepository
    from api.api_v1 import ProductCache


def get_product_service(
    product_repository: Annotated["ProductRepository", Depends(get_product_repository)],
    cache_repository: Annotated["ProductCache", Depends(get_product_cache_repository)],
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        cache_repository=cache_repository,
    )
