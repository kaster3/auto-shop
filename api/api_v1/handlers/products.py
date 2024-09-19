from typing import Annotated, Type, TYPE_CHECKING

from fastapi import APIRouter, Depends, status

from dependencies.repository.product import get_product_repository
from core import settings, Product, ProductCreate, ProductRead
from dependencies.services.product import get_product_service


if TYPE_CHECKING:
    from api.api_v1.repository import ProductRepository
    from api.api_v1 import ProductService

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


@router.get(path="/{product_id}", response_model=ProductRead)
async def get_product(
    repo: Annotated["ProductRepository", Depends(get_product_repository)],
    product_id: int,
) -> Type[Product]:
    product = await repo.get_product(product_id=product_id)
    return product


@router.get(path="", response_model=list[ProductRead])
async def get_products(
    service: Annotated["ProductService", Depends(get_product_service)]
) -> list[ProductRead]:
    products = await service.get_products()
    return products


@router.post(path="", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    repo: Annotated["ProductRepository", Depends(get_product_repository)],
) -> Product:
    product = await repo.create_product(product_create=product_create)
    return product


@router.delete(path="", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    repo: Annotated["ProductRepository", Depends(get_product_repository)],
) -> None:
    await repo.delete_product(product_id=product_id)
