from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from . import Loan


class Client(Base):
    """Таблица клиента с полями."""

    name: Mapped[str] = mapped_column(String(40), nullable=False)
    surname: Mapped[str | None] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    income_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    loan: Mapped[list["Loan"]] = relationship(back_populates="client")
