from fastapi import HTTPException, Depends
from fastapi import FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Note, Tag
from app.schema import NoteCreate
from app.models import User
from auth import endpoints as auth_endpoints
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_endpoints.router, prefix="/auth")

@app.get("/notes")
async def get_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note))
    notes = result.scalars().all()
    return notes

@app.get("/notes/{note_id}")
async def get_note(note_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Note).where(Note.id == note_id, Note.owner_id == current_user.id))
    note = result.scalars().first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@app.post("/notes")
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
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

@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: NoteCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Note).where(Note.id == note_id, Note.owner_id == current_user.id))
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
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Note).filter(Note.id == note_id, Note.owner_id == current_user.id))
    note = result.scalars().first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    await db.delete(note)
    await db.commit()

    return {"message": "Note deleted successfully"}
