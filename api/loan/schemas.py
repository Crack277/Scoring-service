from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LoanBase(BaseModel):
    """Базовая схема кредита клиента."""

    client_id: int = Field(gt=0, description="ID клиента")
    amount: int = Field(ge=0, le=100_000_000, description="Сумма кредита")
    loan_data: datetime = Field(description="Дата выдачи кредита")
    is_closed: bool = Field(default=False, description="Статус закрытия")


class LoanCreate(LoanBase):
    """Схема для создания кредита клиента."""

    pass


class Loan(LoanBase):
    """Схема с конкретным id кредита клиента."""

    model_config = ConfigDict(from_attributes=True)

    id: int
