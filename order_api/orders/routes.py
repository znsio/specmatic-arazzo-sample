from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select

from order_api import SessionDep
from schemas.order import Order, OrderBase, OrderPublic, OrderStatus

orders = APIRouter()


@orders.get("/orders", response_model=list[OrderPublic])
async def get_orders(
    session: SessionDep,
    product_id: Annotated[int | None, Query(alias="productId", ge=1)] = None,
    status: Annotated[OrderStatus | None, Query(alias="status")] = None,
):
    query = select(Order)
    if product_id:
        query = query.where(Order.product_id == product_id)
    if status:
        query = query.where(Order.status == status)
    return session.exec(query)


@orders.post("/orders", response_model=OrderPublic, status_code=201)
async def create_order(order: OrderBase, session: SessionDep):
    db_order = Order.model_validate_json(order.model_dump_json())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@orders.get("/orders/{id}", response_model=OrderPublic)
async def get_order(order_id: Annotated[int, Path(alias="id")], session: SessionDep):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(404, f"Order with ID {order_id} was not found")
    return db_order


@orders.patch("/orders/{id}", response_model=OrderPublic)
async def update_order(order_id: Annotated[int, Path(alias="id")], order: OrderBase, session: SessionDep):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(404, f"Order with ID {order_id} was not found")
    order_data = order.model_dump(exclude_unset=True)
    db_order.sqlmodel_update(order_data)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@orders.delete("/orders/{id}", status_code=204)
async def delete_order(order_id: Annotated[int, Path(alias="id")], session: SessionDep):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(404, f"Order with ID {order_id} was not found")
    session.delete(db_order)
    session.commit()
