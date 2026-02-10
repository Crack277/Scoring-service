from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from . import Client


class Loan(Base):
    """Таблица кредита клиента."""

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    loan_data: Mapped[str] = mapped_column(Date, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False,
    )
    client: Mapped["Client"] = relationship(back_populates="loan")
