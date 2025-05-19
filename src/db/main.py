from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from src.config import Config
from src.db.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session