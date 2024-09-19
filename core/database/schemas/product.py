from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: int


class ProductCreate(ProductBase):
    description: str


class ProductRead(ProductCreate):
    id: int

    class Config:
        from_attributes = True
