from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientBase(BaseModel):
    """Базовая схема."""

    name: str = Field(max_length=40, description="Имя")
    surname: str | None = Field(max_length=40, description="Фамилия")
    email: EmailStr = Field(max_length=100, description="Почта")
    age: int = Field(ge=18, le=150, description="Возраст")
    income_amount: int = Field(ge=0, description="Заработная плата")


class ClientCreate(ClientBase):
    """Схема для создания."""

    pass


class ClientUpdate(ClientBase):
    """Схема для обновления."""

    pass


class Client(ClientBase):
    """Схема с конкретным id клиента."""

    model_config = ConfigDict(from_attributes=True)

    id: int
