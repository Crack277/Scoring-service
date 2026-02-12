from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.client.schemas import ClientCreate, ClientUpdate
from api.utils.task import send_email_newsletter
from src.models import Client


async def get_clients(session: AsyncSession) -> list[Client]:
    """Получаем всех клиентов по id."""
    stmt = select(Client).order_by(Client.id)
    result: Result = await session.execute(stmt)
    clients = result.scalars().all()
    return list(clients)


async def get_client(client_id: int, session: AsyncSession) -> Client | None:
    """Получаем конкретного клиента по id."""
    return await session.get(Client, client_id)


async def create_client(
    client_create: ClientCreate,
    session: AsyncSession,
) -> Client:
    """Создаём клиента."""
    stmt = select(Client).where(Client.email == client_create.email)
    result = await session.scalar(stmt)
    if result is None:
        send_email_newsletter(client_name=client_create.name)
        client = Client(**client_create.model_dump())
        session.add(client)
        await session.commit()
        return client

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="This email is already occupied",
    )


async def update_client(
    client_update: ClientUpdate,
    client: Client,
    session: AsyncSession,
    partial: bool = False,
) -> Client:
    """Обновляем данных о клиенте(не частично)."""
    for name, value in client_update.model_dump(exclude_unset=partial).items():
        setattr(client, name, value)
    await session.commit()
    return client


async def delete_client(client: Client, session: AsyncSession) -> None:
    """Удаляем клиента."""
    await session.delete(client)
    await session.commit()
