from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.config import settings


class DatabaseHelper:
    """Класс для взаимодействия с бд."""

    def __init__(self, url: str, echo: bool = False):
        """Инициализация."""
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """Получаем сессию."""
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self):
        """Реализация асинхронного подхода."""
        session = self.get_scoped_session()
        yield session
        await session.close()

    async def dispose(self):
        """Разрыв."""
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Контекстный менеджер для получения сессии"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_helper = DatabaseHelper(url=settings.db.url, echo=settings.db.echo)
