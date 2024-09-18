from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from .services import get_notes, create_note

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Welcome! Use /create_note to create a new note, /get_notes to retrieve notes.")

@router.message(Command("get_notes"))
async def get_notes_command(message: Message):
    notes = await get_notes()
    if notes:
        response = "\n".join([f"Title: {note['title']}\nContent: {note['content']}" for note in notes])
    else:
        response = "No notes found."
    await message.answer(response)

@router.message(Command("create_note"))
async def create_note_command(message: Message):
    # For simplicity, we assume the format is "/create_note title; content; tag1,tag2"
    try:
        _, text = message.text.split(" ", 1)
        title, content, tags_str = text.split(";")
        tags = [tag.strip() for tag in tags_str.split(",")]
        response = await create_note(title.strip(), content.strip(), tags)
        await message.answer(f"Note created: {response}")
    except Exception as e:
        await message.answer(f"Failed to create note: {e}")
