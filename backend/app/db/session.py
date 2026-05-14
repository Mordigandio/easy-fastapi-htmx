from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

#  асинхронный движок
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO_SQL
)

#  фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,      
)

