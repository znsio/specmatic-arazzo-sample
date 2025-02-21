import enum

from pydantic import StrictInt
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel


class OrderStatus(str, enum.Enum):
    FULFILLED = "fulfilled"
    PENDING = "pending"
    CANCELLED = "cancelled"


class OrderBase(SQLModel):
    product_id: StrictInt = Field(ge=1)
    count: StrictInt = Field(ge=1)
    status: OrderStatus = OrderStatus.PENDING

    class Config: # pyright: ignore[]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class OrderPublic(OrderBase):
    id: StrictInt


class Order(OrderBase, table=True):
    id: StrictInt | None = Field(default=None, primary_key=True)
