from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BookEntity:
    id: int | None
    title: str
    author: str
    year: int | None
    created_at: datetime | None
    updated_at: datetime | None