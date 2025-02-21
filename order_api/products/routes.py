from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from sqlmodel import select

from order_api import SessionDep
from schemas.product import Product, ProductBase, ProductPublic, ProductType

products = APIRouter()


@products.get("/products", response_model=list[Product])
async def get_products(session: SessionDep, product_type: Annotated[ProductType | None, Query(alias="type")] = None):
    query = select(Product)
    if product_type:
        query = query.where(Product.type == product_type)
    return session.exec(query)


@products.post("/products", response_model=ProductPublic, status_code=201)
async def add_product(product: ProductBase, session: SessionDep):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@products.get("/products/{id}", response_model=ProductPublic)
async def get_product(product_id: Annotated[int, Path(alias="id")], session: SessionDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(404, f"Product with ID {product_id} was not found")
    return db_product


@products.patch("/products/{id}", response_model=ProductPublic)
async def update_product(
    product_id: Annotated[int, Path(alias="id")],
    product: ProductBase,
    session: SessionDep,
):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(404, f"Product with ID {product_id} was not found")
    product_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@products.delete("/products/{id}", status_code=204)
async def delete_product(product_id: Annotated[int, Path(alias="id")], session: SessionDep):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(404, f"Product with ID {product_id} was not found")
    session.delete(db_product)
    session.commit()
