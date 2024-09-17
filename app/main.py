from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Note, Tag
from app.schema import NoteCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/notes")
async def get_notes(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Note))
        notes = result.scalars().all()
    return notes


@app.get("/notes/{note_id}")
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@app.post("/notes")
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    new_note = Note(
        title=note.title,
        content=note.content,
    )
    db.add(new_note)

    await db.commit()
    await db.refresh(new_note)

    tag_ids = []
    for tag_name in note.tags:
        result = await db.execute(select(Tag).filter(Tag.name == tag_name))
        existing_tag = result.scalars().first()

        if existing_tag:
            tag_ids.append(existing_tag.id)
        else:
            new_tag = Tag(name=tag_name)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            tag_ids.append(new_tag.id)

    for tag_id in tag_ids:
        insert_query = text("INSERT INTO note_tag (note_id, tag_id) VALUES (:note_id, :tag_id)")
        await db.execute(insert_query, {"note_id": new_note.id, "tag_id": tag_id})

    await db.commit()

    return {"message": "Note created successfully", "note": new_note}


from fastapi import HTTPException


@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: NoteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note).where(Note.id == note_id))
    existing_note = result.scalars().first()

    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    existing_note.title = note.title
    existing_note.content = note.content

    tag_ids = []
    for tag_name in note.tags:
        result = await db.execute(select(Tag).filter(Tag.name == tag_name))
        existing_tag = result.scalars().first()

        if existing_tag:
            tag_ids.append(existing_tag.id)
        else:
            new_tag = Tag(name=tag_name)
            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            tag_ids.append(new_tag.id)

    await db.execute(text("DELETE FROM note_tag WHERE note_id = :note_id"), {"note_id": existing_note.id})

    for tag_id in tag_ids:
        insert_query = text("INSERT INTO note_tag (note_id, tag_id) VALUES (:note_id, :tag_id)")
        await db.execute(insert_query, {"note_id": existing_note.id, "tag_id": tag_id})

    await db.commit()
    await db.refresh(existing_note)

    return {"message": "Note updated successfully", "note": existing_note}

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    await db.delete(note)
    await db.commit()

    return {"message": "Note deleted successfully"}
