from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
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


db_helper = DatabaseHelper(url=settings.db.url, echo=settings.db.echo)
