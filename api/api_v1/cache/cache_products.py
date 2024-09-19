import json

from redis import Redis

from core import ProductRead


class ProductCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_products(self) -> list[ProductRead]:
        with self.redis as redis:
            products_json = redis.lrange("all_product", 0, -1)
            return [
                ProductRead.model_validate(json.loads(product_json))
                for product_json in products_json
            ]

    def set_products(self, products: list[ProductRead]):
        products_json = [product.json() for product in products]
        with self.redis as redis:
            redis.lpush("all_product", *products_json)
            redis.expire("all_product", 10)
