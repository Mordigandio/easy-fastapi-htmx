from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookEntity(BaseModel):
    """ Доменная модель книги """
    
    model_config = ConfigDict(from_attributes=True, frozen=True)
    id: int
    title: str
    author: str
    year: int | None = None
    created_at: datetime | None
    updated_at: datetime | None