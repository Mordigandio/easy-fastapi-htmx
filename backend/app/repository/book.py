from typing import Protocol

from app.domain.entity import BookEntity
from app.domain.exception import BookAlreadyExistsError, BookNotFoundError
from app.models import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class IBookRepository(Protocol):
    # Интерфейс 

    async def create(self, data: BookCreate) -> BookEntity: ...
    async def get(self, book_id: int) -> BookEntity | None: ...
    async def list(self, skip: int, limit: int, search: str | None) -> list[BookEntity]: ...
    async def update(self, book_id: int, data: BookUpdate) -> BookEntity: ...
    async def delete(self, book_id: int) -> None: ...

class BookRepository(IBookRepository):
    """ Репозиторий отвечающий за взаимодействие с базой данных """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get(self, book_id: int) -> BookEntity | None:
        """ Получение книги by ID """

        book = await self.session.get(Book, book_id)
        return BookEntity.model_validate(book) if book else None
    
    async def list(
            self, 
            skip: int = 0, 
            limit: int = 100, 
            search: str | None = None) -> list[BookEntity]:
        """ Список книг / плагинация и поиск """

        stmt = select(Book)

        if search:
            stmt = stmt.where(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                )
            )

        stmt = stmt.order_by(Book.created_at.desc()).offset(skip).limit(limit)
        
        result = await self.session.scalars(stmt)
        return [BookEntity.model_validate(b) for b in result.all()]

    async def create(self, data: BookCreate) -> BookEntity:
        """ Создание новой книги """
        book = Book(**data.model_dump())
        self.session.add(book)

        try:
            await self.session.flush()
            return BookEntity.model_validate(book)
        except IntegrityError as e:
            raise BookAlreadyExistsError(title=data.title, author=data.author) from e
 
    async def update(self, book_id: int, data: BookUpdate) -> BookEntity:
        """ Частичное обновление книги """

        book = await self.session.get(Book, book_id)
        if not book:
            raise BookNotFoundError(book_id) 
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None and value != "":
                setattr(book, key, value)

        await self.session.flush()
        await self.session.refresh(book)
        return BookEntity.model_validate(book)
  
    async def delete(self, book_id: int) -> None:
        """ Удалание книги by id """

        book = await self.session.get(Book, book_id)
        if book:
            await self.session.delete(book)
            await self.session.flush()