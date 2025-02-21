import enum

from pydantic import StrictInt, StrictStr
from sqlmodel import Field, SQLModel
from sqlmodel import Field as SQLField


class ProductType(str, enum.Enum):
    GADGET = "gadget"
    FOOD = "food"
    BOOK = "book"
    OTHER = "other"


class ProductBase(SQLModel):
    name: StrictStr
    type: ProductType
    inventory: StrictInt = Field(ge=1, le=101)
    description: StrictStr | None = Field(default=None, exclude=True)


class ProductPublic(ProductBase):
    id: StrictInt


class Product(ProductBase, table=True):
    id: StrictInt | None = SQLField(default=None, primary_key=True)
