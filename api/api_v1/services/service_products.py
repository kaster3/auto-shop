from typing import TYPE_CHECKING

from core import ProductRead


if TYPE_CHECKING:
    from api.api_v1.repository.products import ProductRepository
    from api.api_v1 import ProductCache


class ProductService:
    def __init__(
        self,
        product_repository: "ProductRepository",
        cache_repository: "ProductCache",
    ) -> None:
        self.repo = product_repository
        self.cache = cache_repository

    async def get_products(self):
        if products := self.cache.get_products():
            print("from cache")
            return products
        print("not from cache")
        products = await self.repo.get_all_products()
        product_schema = [ProductRead.model_validate(product) for product in products]
        self.cache.set_products(product_schema)
        return product_schema
