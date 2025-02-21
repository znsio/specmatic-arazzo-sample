import enum
import uuid as uuid_pkg

from pydantic import EmailStr, StrictStr
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel


class UuidType(str, enum.Enum):
    REGULAR = "Regular"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"


class Status(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class Customer(SQLModel):
    first_name: StrictStr
    last_name: StrictStr
    email: EmailStr = Field(index=True, unique=True)

    class Config:  # pyright: ignore[]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UuidBase(Customer):
    uuid_type: UuidType = Field(index=True, default=UuidType.REGULAR)
    status: Status = Field(alias="status", default=Status.ACTIVE, exclude=True)


class UuidPublic(UuidBase):
    uuid: uuid_pkg.UUID


class Uuid(UuidBase, table=True):
    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, nullable=False)
