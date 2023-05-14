from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    """Базовая схема для работы с проектами."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[int]

    @validator('name')
    def name_cant_be_none(cls, value: str):
        if value is None:
            raise ValueError(
                'Имя/описание целевого проекта не может быть пустым!'
            )
        return value


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description', 'full_amount')
    def none_and_empty_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError('Требуется заполнить все поля!')
        return value


class CharityProjectUpdate(CharityProjectBase):
    """Схема для изменения проекта."""

    pass


class CharityProjectDB(CharityProjectBase):
    """Схема для работы с проектом в БД."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
