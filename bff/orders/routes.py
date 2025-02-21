from typing import Annotated

from fastapi import APIRouter, Depends

from bff import get_order_service
from bff.schemas import OrderRequest
from bff.services import OrdersService
from schemas.order import OrderBase, OrderPublic

orders = APIRouter()


@orders.post("/orders", status_code=201, response_model=OrderPublic)
async def create_order(
    order_request: OrderRequest,
    order_service: Annotated[OrdersService, Depends(get_order_service)],
):
    order_data = OrderBase.model_validate(order_request)
    return await order_service.create_order(order_data)
