"""Тесты для dbhelper.py"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


# @pytest.mark.unit
class TestDatabaseHelper:
    """Тесты для DatabaseHelper"""

    @patch("src.models.dbhelper.create_async_engine")
    @patch("src.models.dbhelper.async_sessionmaker")
    def test_db_helper_init(self, mock_sessionmaker, mock_create_async_engine):
        """Проверка инициализации."""
        from src.models.dbhelper import DatabaseHelper

        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_async_engine.return_value = mock_engine
        db_helper = DatabaseHelper(url="postgresql+asyncpg://test", echo=True)

        # Проверяем: создан ли engine с верными параметрами
        mock_create_async_engine.assert_called_once()
        response = mock_create_async_engine.call_args[1]
        assert response["url"] == "postgresql+asyncpg://test"
        assert response["echo"] is True

        # Проверяем: правильно ли сохранён engine в атрибуте объекта
        mock_sessionmaker.assert_called_once()
        assert db_helper.engine == mock_engine

    @patch("src.models.dbhelper.create_async_engine")
    @patch("src.models.dbhelper.async_sessionmaker")
    @pytest.mark.asyncio
    async def test_dispose(self, mock_sessionmaker, mock_create_async_engine):
        """Проверка закрытия соединения."""
        from src.models.dbhelper import DatabaseHelper

        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_async_engine.return_value = mock_engine
        db_helper = DatabaseHelper(url="postgresql+asyncpg://test")

        await db_helper.dispose()

        mock_engine.dispose.assert_called_once()

    @patch("src.models.dbhelper.create_async_engine")
    @patch("src.models.dbhelper.async_sessionmaker")
    @pytest.mark.asyncio
    async def test_db_session(self, mock_sessionmaker, mock_create_async_engine):
        """Проверка работы сессии."""
        from src.models.dbhelper import DatabaseHelper

        mock_engine = MagicMock(spec=AsyncEngine)
        mock_create_async_engine.return_value = mock_engine

        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock()
        mock_session.close = AsyncMock()
        mock_session.rollback = AsyncMock()

        mock_factory = MagicMock()
        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_factory.return_value.__aexit__ = AsyncMock()
        mock_sessionmaker.return_value = mock_factory

        db_helper = DatabaseHelper(url="postgresql+asyncpg://test")

        async with db_helper.session() as session:
            assert session == mock_session

        # Проверяем, что commit вызван один раз
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        mock_session.rollback.assert_not_called()


# @pytest.mark.unit
class TestDatabaseHelperObject:
    """Тесты для объекта db_helper."""

    def test_db_helper_not_null(self):
        from src.models import db_helper

        assert db_helper is not None

    def test_db_has_engine(self):
        from src.models import db_helper

        assert hasattr(db_helper, "engine")

    def test_db_has_session_factory(self):
        from src.models import db_helper

        assert hasattr(db_helper, "session_factory")
        assert callable(db_helper.session_factory)

    def test_db_has_scoped_session(self):
        from src.models import db_helper

        assert hasattr(db_helper, "get_scoped_session")
        assert callable(db_helper.get_scoped_session())

    def test_db_has_session_dependency(self):
        from src.models import db_helper

        assert hasattr(db_helper, "session_dependency")
        assert callable(db_helper.session_dependency)

    def test_db_has_dispose(self):
        from src.models import db_helper

        assert hasattr(db_helper, "dispose")
        assert callable(db_helper.dispose)

    def test_db_has_session(self):
        from src.models import db_helper

        assert hasattr(db_helper, "session")
        assert callable(db_helper.session())
