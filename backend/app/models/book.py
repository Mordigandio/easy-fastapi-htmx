from app.db.base import Base
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import TimeStampMixin


class Book(Base, TimeStampMixin):
    """ Информация для BD / таблица нашей базы данных """

    # Название нашей таблицы    
    __tablename__ = "books"

    # Таблицы в базе
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Ограничение на дубликаты
    __table_args__ = (
        UniqueConstraint("title", "author", name="uq_book_title_author"),
    )

    # Отображение для debug
    def __repr__(self) -> str:
        return f"<book(id={self.id}, title={self.title}, author={self.author})>"
    
