from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    """ Базовая схема с общими полями для всех операций """
    title: str
    author: str
    year: int | None = None


class BookCreate(BookBase):
    """ Схема для валидации данных при создании новой записи """
    pass


class BookUpdate(BaseModel):
    """ Схема для обновления данных, конструкция "| None" для опциональности """
    title: str | None = None
    author: str | None = None
    year: int | None = None


class BookResponse(BookBase):
    """ Схема для формирования ответа API  """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    