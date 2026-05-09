from app.domain.entity import BookEntity
from app.domain.exception import BookAlreadyExistsError
from app.models import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create(self, data: BookCreate) -> BookEntity:
        book = Book(**data.model_dump())
        self.session.add(book)
        try:
            await self.session.flush()
        except IntegrityError:
            raise BookAlreadyExistsError(data.title, data.author)
        
        await self.session.refresh(book)
        return self._to_entity(book)
    

    async def get(self, book_id: int) -> BookEntity | None:
        book = await self.session.get(Book, book_id)
        return self._to_entity(book) if book else None
    

    async def list(self, skip: int = 0, limit: int = 100, search: str | None = None) -> list[BookEntity]:
        stmt = select(Book).offset(skip).limit(limit).order_by(Book.created_at.desc())
        
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))

        result = await self.session.scalars(stmt)
        return [self._to_entity(b) for b in result.all()]
    

    async def update(self, book_id: int, data: BookUpdate) -> BookEntity | None:
        book = await self.session.get(Book, book_id)
        
        if not book:
            return None


        for key, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(book, key, value)
        
        await self.session.flush()
        await self.session.refresh(book)
        return self._to_entity(book)
    
    async def delete(self, book_id: int) -> bool:
        book = await self.session.get(Book, book_id)

        if not book:
            return False
        await self.session.delete(book)
        return True


    def _to_entity(self, book: Book) -> BookEntity:
        """Вспомогательный метод для маппинга"""
        return BookEntity(
            id=book.id,
            title=book.title,
            author=book.author,
            year=book.year,
            created_at=book.created_at,
            updated_at=book.updated_at
        )