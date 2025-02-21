from schemas.order import OrderBase
from schemas.product import ProductBase
from schemas.uuid_schemas import Customer


class ProductRequest(ProductBase):
    customer: Customer


class OrderRequest(OrderBase):
    customer: Customer
