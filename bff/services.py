from typing import ClassVar

import httpx
from fastapi import HTTPException

from bff.config import Config
from schemas.order import OrderBase, OrderPublic
from schemas.product import ProductBase, ProductPublic, ProductType
from schemas.uuid_schemas import Customer, UuidBase, UuidPublic


class BaseService:
    def __init__(self, user_uuid: UuidPublic):
        self.config = Config()  # pyright: ignore[reportCallIssue]
        self.headers = {"Authenticate": self.config.AUTH_TOKEN, "UUID": str(user_uuid.uuid)}


class ProductService(BaseService):
    _API_LIST: ClassVar[dict[str, str]] = {
        "SEARCH": "/products",
        "CREATE": "/products",
    }

    async def find_products(self, product_type: ProductType | None) -> list[ProductPublic]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.config.API_URL}{ProductService._API_LIST['SEARCH']}",
                params={"type": product_type.value} if product_type else None,
                headers=self.headers,
                timeout=self.config.REQ_TIMEOUT,
            )

        if resp.status_code != 200:
            raise HTTPException(resp.status_code, "An error occurred while retrieving the products.")

        return [ProductPublic(**product) for product in resp.json()]

    async def create_product(self, product: ProductBase) -> ProductPublic:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.config.API_URL}{ProductService._API_LIST['CREATE']}",
                json=product.model_dump(exclude={"description"}, by_alias=True),
                headers=self.headers,
                timeout=self.config.REQ_TIMEOUT,
            )

        if resp.status_code != 201:
            raise HTTPException(resp.status_code, "An error occurred while creating the product.")

        return ProductPublic(**resp.json())


class OrdersService(BaseService):
    _API_LIST: ClassVar[dict[str, str]] = {
        "CREATE": "/orders",
    }

    async def create_order(self, order: OrderBase) -> OrderPublic:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.config.API_URL}{OrdersService._API_LIST['CREATE']}",
                json=order.model_dump(by_alias=True),
                headers=self.headers,
                timeout=self.config.REQ_TIMEOUT,
            )

        if resp.status_code != 201:
            raise HTTPException(resp.status_code, "An error occurred while creating the order.")

        return OrderPublic(**resp.json())


class UUidService:
    config = Config()  # pyright: ignore[reportCallIssue]
    _API_LIST: ClassVar[dict[str, str]] = {
        "CREATE": "/uuids",
    }

    async def create_uuid(self, customer: Customer) -> UuidPublic:
        request = UuidBase.model_validate(customer)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.config.UUID_URL}{UUidService._API_LIST['CREATE']}",
                json=request.model_dump(by_alias=True),
                timeout=self.config.REQ_TIMEOUT,
            )

        if resp.status_code not in (200, 201):
            raise HTTPException(resp.status_code, "An error occurred while fetching the UUID")

        return UuidPublic(**resp.json())
