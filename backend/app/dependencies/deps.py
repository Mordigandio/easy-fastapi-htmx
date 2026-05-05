from collections.abc import AsyncGenerator
from typing import Annotated

from app.db.session import AsyncSessionLocal
from app.repository.book import BookRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    """ Асинхронная сессия базы-данных """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Аннотация типа, для routes/endpoints 
SessionDeps = Annotated[AsyncSession, Depends(async_get_db)]

async def get_book_repo(session: SessionDeps) -> BookRepository:
    """ Зависимость текущей сессии БД в репозиторий """
    return BookRepository(session)


BookRepoDeps = Annotated[BookRepository, Depends(get_book_repo)]
