from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class BookBase(BaseModel):
    """ Базовая схема с общими полями для всех операций """

    title: str
    author: str
    year: int | None = None


class BookCreate(BookBase):
    """ Схема для валидации данных при создании новой записи """
    
    @model_validator(mode='before')
    @classmethod
    def empty_str_to_none(cls, data: Any) -> Any:
        """ Костыль для пустых строк HTMX-форм """

        if isinstance(data, dict):
            return {k: (None if v == "" else v) for k, v in data.items()}
        return data


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

    