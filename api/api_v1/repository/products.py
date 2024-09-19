from typing import Sequence, Type

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core import Product, ProductCreate
from utils.exceptions import not_found_by_id
from utils.item_name import item_naming


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_products(self) -> Sequence[Product]:
        query = select(Product).order_by(Product.id)
        result = await self.session.scalars(query)
        return result.all()

    async def get_product(self, product_id: int) -> Type[Product]:
        # query = select(Product).where(Product.id == product_id)
        # product = await session.scalar(query)
        product = await self.session.get(Product, product_id)
        if product is not None:
            return product

        not_found_by_id(item_id=product_id, item=item_naming())

    async def create_product(
        self,
        product_create: ProductCreate,
    ) -> Product:
        product = Product(**product_create.model_dump())
        self.session.add(product)
        await self.session.commit()
        # на стороне бд данные могут быть не актуальны так как могут быть какие-то правки объекта при сохранение
        # и в таком случае важно обновить данные, чтобы были актуальные, это только в асинхронной алхимии тк параметры
        # autoflash и тд при async = False
        await self.session.refresh(product)
        return product

    async def delete_product(self, product_id: int) -> None:
        query = select(Product).where(Product.id == product_id)
        product = await self.session.scalar(query)
        if product is not None:
            delete_query = delete(Product).where(Product.id == product_id)
            await self.session.execute(delete_query)
            await self.session.commit()
        else:
            not_found_by_id(item_id=product_id, item=item_naming())
