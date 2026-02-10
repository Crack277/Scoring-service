from fastapi import BackgroundTasks
from fastapi_cache import FastAPICache
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.client.schemas import ClientCreate, ClientUpdate
from src.config import settings
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
    # background_tasks: BackgroundTasks,
    client_create: ClientCreate,
    session: AsyncSession,
) -> Client:
    """Создаём клиента."""
    # if background_tasks:
    #     background_tasks.add_task(
    #         FastAPICache.clear,
    #         namespace=settings.cache.namespace.users,
    #     )
    # else:
    #     await FastAPICache.clear(
    #         namespace=settings.cache.namespace.users,
    #     )

    client = Client(**client_create.model_dump())
    session.add(client)
    await session.commit()
    return client


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
