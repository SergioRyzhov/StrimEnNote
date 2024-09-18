import aiohttp

API_URL = "http://localhost:8000"  # Adjust according to your FastAPI setup

async def get_notes():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/notes") as response:
            return await response.json()

async def create_note(title: str, content: str, tags: list):
    async with aiohttp.ClientSession() as session:
        data = {
            "title": title,
            "content": content,
            "tags": tags
        }
        async with session.post(f"{API_URL}/notes", json=data) as response:
            return await response.json()
