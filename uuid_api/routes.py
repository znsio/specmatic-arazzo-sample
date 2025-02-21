from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import UUID4
from sqlmodel import and_, select

from schemas.uuid_schemas import Uuid, UuidBase, UuidPublic, UuidType
from uuid_api import SessionDep

uuids = APIRouter()


@uuids.get("/uuids", response_model=list[UuidPublic])
async def get_uuids(
    session: SessionDep,
    uuid_type: Annotated[UuidType, Query(alias="uuidType")],
    uuid_id: Annotated[UUID4 | None, Query(alias="uuid")] = None,
):
    query = select(Uuid).where(Uuid.uuid_type == uuid_type)
    if uuid_id:
        query = query.where(Uuid.uuid == uuid_id)
    return session.exec(query)


@uuids.post("/uuids", response_model=UuidPublic, status_code=201)
async def create_uuid(uuid_data: UuidBase, session: SessionDep):
    query = select(Uuid).where(Uuid.email == uuid_data.email)
    uuid_exists = session.exec(query).first()

    if uuid_exists:
        return uuid_exists

    db_uuid = Uuid.model_validate(uuid_data)
    session.add(db_uuid)
    session.commit()
    session.refresh(db_uuid)
    return db_uuid


@uuids.get("/uuids/{uuidType}/{uuid}", response_model=UuidPublic)
async def get_uuid(
    uuid_type: Annotated[UuidType, Path(alias="uuidType")],
    uuid_id: Annotated[UUID4, Path(alias="uuid")],
    session: SessionDep,
):
    query = select(Uuid).where(and_(Uuid.uuid_type == uuid_type, Uuid.uuid == uuid_id))
    uuid = session.exec(query).first()
    if not uuid:
        raise HTTPException(404, f"UUID not found for {uuid_type} {uuid_id}")
    return uuid


@uuids.patch("/uuids/{uuidType}/{uuid}", response_model=UuidPublic)
async def update_uuid(
    uuid_type: Annotated[UuidType, Path(alias="uuidType")],
    uuid_id: Annotated[UUID4, Path(alias="uuid")],
    uuid_data: UuidBase,
    session: SessionDep,
):
    query = select(Uuid).where(and_(Uuid.uuid_type == uuid_type, Uuid.uuid == uuid_id))
    db_uuid = session.exec(query).first()
    if not db_uuid:
        raise HTTPException(404, f"UUID not found for {uuid_type} {uuid_id}")

    uuid_dump = uuid_data.model_dump(exclude_unset=True)
    db_uuid.sqlmodel_update(uuid_dump)
    session.add(db_uuid)
    session.commit()
    session.refresh(db_uuid)
    return db_uuid
