from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api.client import crud as client_crud
from api.client.dependencies import (
    get_client_by_id,
    scoring_message,
    show_clients_with_loans,
)
from api.client.schemas import ClientCreate, ClientUpdate
from api.loan.dependencies import create_loan
from api.utils.key_builder import users_key_builder
from src.models import Client, Loan, db_helper

router = APIRouter(
    prefix="/clients",
    tags=["CLIENTS / LOANS"],
)


@router.get("/all")
@cache(expire=30, key_builder=users_key_builder)
async def get_clients(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await client_crud.get_clients(session=session)


@router.get("/{client_id}/")
async def get_client(client: Client = Depends(get_client_by_id)):
    return client


@router.get("/{client_id}/loans/")
async def scoring_message(client: Client = Depends(scoring_message)):
    return client


@router.get("/all/loans")
async def show_clients_with_loans(
    clients: list[Client] = Depends(show_clients_with_loans),
):
    return clients


@router.post("/{client_id}/")
async def create_client(
    background_tasks: BackgroundTasks,
    client_create: ClientCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await client_crud.create_client(
        background_tasks=background_tasks,
        client_create=client_create,
        session=session,
    )


@router.post("/{client_id}/loans/{loan_id}")
async def create_loan(loan: Loan = Depends(create_loan)):
    return loan


@router.put("/{client_id}/")
async def update_client(
    client_update: ClientUpdate,
    client: Client = Depends(get_client_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await client_crud.update_client(
        client_update=client_update, client=client, session=session
    )


@router.delete("/{client_id}/")
async def delete_client(
    client: Client = Depends(get_client_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await client_crud.delete_client(client=client, session=session)
