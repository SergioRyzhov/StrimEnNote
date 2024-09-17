from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Note


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "working!"}


@app.get("/notes")
async def get_notes(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Note))
        notes = result.scalars().all()
    return notes