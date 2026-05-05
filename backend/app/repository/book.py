from app.models import Book
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: BookCreate) -> Book:
        book = Book(**data.model_dump())
        self.session.add(book)
        await self.session.flush()
        await self.session.refresh(book)
        return book
    
    async def get(self, book_id: int) -> Book | None:
        return await self.session.get(Book, book_id)
    
    async def list(self, skip: int = 0, limit: int = 100) -> list[Book]:
        stmt = select(Book).offset(skip).limit(limit).order_by(Book.created_at.desc())
        result = await self.session.scalars(stmt)
        return list(result.all())
    
    async def update(self, book_id: int, data: BookUpdate) -> Book | None:
        book = await self.session.get(Book, book_id)
        
        if not book:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        
        await self.session.flush()
        await self.session.refresh(book)
        return book
    
    async def delete(self, book_id: int) -> bool:
        book = await self.session.get(Book, book_id)

        if not book:
            return False
        await self.session.delete(book)
        return True
