from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для реализации таблиц."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        """Получаем название таблицы в нижнем регистре + 's'."""
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
