from collections.abc import AsyncGenerator
from typing import Annotated

from app.db.session import AsyncSessionLocal
from app.repository.book import BookRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    """ Асинхронная сессия базы-данных """

    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session

#  Псевдонимы типов 
SessionDeps = Annotated[AsyncSession, Depends(async_get_db)]

async def get_book_repo(session: SessionDeps) -> BookRepository:
    return BookRepository(session)

BookRepoDeps = Annotated[BookRepository, Depends(get_book_repo)]