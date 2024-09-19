from sqlalchemy.orm import Mapped

from .base import Base
from .mixins import IntIdPkMixin


class Product(IntIdPkMixin, Base):
    name: Mapped[str]
    price:  Mapped[int]
    description:  Mapped[str]
