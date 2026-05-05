from app.db.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import TimeStampMixin


class Book(Base, TimeStampMixin):
    """ Информация для BD, или просто таблица нашей базы данных """
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Отображение для debug
    def __repr__(self) -> str:
        return f"<book(id={self.id}, title={self.title}, author={self.author})>"
    
