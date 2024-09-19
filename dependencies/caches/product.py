from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from api.api_v1.cache.accessor import get_redis_connection
from api.api_v1.cache.cache_products import ProductCache


if TYPE_CHECKING:
    from redis import Redis


def get_product_cache_repository(
    redis: Annotated["Redis", Depends(get_redis_connection)]
) -> ProductCache:
    return ProductCache(redis=redis)
