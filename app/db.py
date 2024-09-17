from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/notes_db")

async_engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))

async def get_db():
    async with SessionLocal() as session:
        yield session
