from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Client, db_helper

from .crud import get_client


async def get_client_by_id(
    client_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Client:
    """Получаем клиента по id, иначе генерируем исключение."""
    client = await get_client(client_id=client_id, session=session)
    if client is not None:
        return client
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client is not found!",
    )


async def show_clients_with_loans(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[Client]:
    stmt = select(Client).options(selectinload(Client.loan)).order_by(Client.id)
    clients = await session.scalars(stmt)
    return list(clients)


async def scoring_message(
    client_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    stmt = (
        select(Client).where(Client.id == client_id).options(selectinload(Client.loan))
    )
    client = await session.scalar(stmt)
    if client is not None:
        count_loans = len(client.loan)
        message = {
            "result": 0,
        }
        if count_loans >= 1:
            message["result"] = 30000
            return message
        if count_loans == 0 and client.income_amount > 50000:
            message["result"] = 20000
            return message
        if count_loans == 0 and client.income_amount > 30000:
            message["result"] = 10000
            return message
        return message

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client is not found!",
    )
