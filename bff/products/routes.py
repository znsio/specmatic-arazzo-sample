from typing import Annotated

from fastapi import APIRouter, Depends

from bff import get_product_service
from bff.schemas import ProductRequest
from bff.services import ProductService
from schemas.product import ProductBase, ProductPublic

products = APIRouter()


@products.post("/products", status_code=201, response_model=ProductPublic)
async def add_product(
    data: ProductRequest,
    product_service: Annotated[ProductService, Depends(get_product_service)],
):
    product_data = ProductBase.model_validate(data)
    return await product_service.create_product(product_data)
