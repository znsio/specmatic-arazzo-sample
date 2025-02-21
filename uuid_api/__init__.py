from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine

from uuid_api.config import Config

config = Config()  # pyright: ignore[reportCallIssue]
connect_args = {"check_same_thread": False}
engine = create_engine(config.UUID_DATABASE_URI, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
def handle_marshmallow_validation_error(_, e: "RequestValidationError|ValidationError"):
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
def http_error_handler(_, e: "HTTPException"):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "status": e.status_code,
            "error": e.__class__.__name__,
            "message": e.detail,
        },
    )


from .routes import uuids  # noqa: E402

app.include_router(uuids)
