from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from bff.services import OrdersService, ProductService, UUidService
from schemas.uuid_schemas import Customer

app = FastAPI()


async def get_product_service(request: Request) -> ProductService:
    body = await request.json()
    customer = Customer.model_validate(body.get("customer", {}))
    uuid = await UUidService().create_uuid(customer)
    return ProductService(uuid)


async def get_order_service(request: Request) -> OrdersService:
    body = await request.json()
    customer = Customer.model_validate(body.get("customer", {}))
    uuid = await UUidService().create_uuid(customer)
    return OrdersService(uuid)


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def handle_marshmallow_validation_error(_, e: "RequestValidationError|ValidationError"):
    return JSONResponse(
        status_code=400,
        content={
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "status": 400,
            "error": "Bad Request",
            "message": str(e),
        },
    )


@app.exception_handler(HTTPException)
async def http_error_handler(_, e: "HTTPException"):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "status": e.status_code,
            "error": e.__class__.__name__,
            "message": e.detail,
        },
    )


from .orders.routes import orders  # noqa: E402
from .products.routes import products  # noqa: E402

app.include_router(products)
app.include_router(orders)
