# StrimEnNote
___

## Project Overview

This project is a FastAPI-based web application that allows users to 
manage their personal notes. Users can register and authenticate via JWT tokens 
and perform CRUD (Create, Read, Update, Delete) operations on their notes. 
Each note supports multiple tags for easier categorization and searching. 
The project also includes a Telegram bot integration for managing notes directly 
through Telegram.

### Key Features:
User Registration and Authentication: Secure JWT-based authentication for users.
CRUD Operations for Notes: Users can create, update, delete, and fetch notes.
Tagging System: Each note can have multiple tags, allowing easy searching and filtering.
Asynchronous API: Built with FastAPI and SQLAlchemy for efficient asynchronous operations.
Telegram Bot: A bot built with Aiogram allows users to manage their notes via Telegram.
___

## Local Setup Instructions
To set up and run the project locally, follow the steps below:

**1. Clone the Repository**
```bash
git clone https://github.com/SergioRyzhov/StrimEnNote.git
cd <repository-directory>
```
**2. Create a Virtual Environment**

Make sure you have Python 3.12 or higher installed. 
Then, create and activate a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**

Install the required dependencies listed in the 
requirements.txt file:
```bash
pip install -r requirements.txt
```
**4. Set Up Environment Variables**

Create a .env file in the root of the project and define the required environment 
variables:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/db_name
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
**5. Run Database Migrations**
Ensure that the database is set up and migrations are applied:
```bash
alembic upgrade head
```
**6. Run the FastAPI Server**
Start the FastAPI server:
```bash
docker-compose up -d
```
**or**
`uvicorn app.main:app`
### This will start the server at http://127.0.0.1:8000.

**7. Run the Telegram Bot**
In a separate terminal, run the Telegram bot:
```bash
python -m bot.main
```
**Or it runs automatically**


---
## API Endpoints
### Here is a description of the available endpoints for the FastAPI server:

**User Registration**
- URL: /auth/register
- Method: POST
- Description: Registers a new user.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```
**response**
```json
{
  "message": "User created successfully",
  "user": "username"
}

```

**User Login**
- URL: /auth/login
- Method: POST
- Description: Logs in a user and returns a JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```
**Response:**
```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

**Get All Notes**
- URL: /notes
- Method: GET
- Description: Returns a list of all notes.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Note Title",
    "content": "Note Content",
    "tags": ["tag1", "tag2"]
  }
]
```

**Get a Specific Note**
- URL: /notes/{note_id}
- Method: GET
- Description: Retrieves a specific note by its ID.

**Response:**
```json
{
  "id": 1,
  "title": "Note Title",
  "content": "Note Content",
  "tags": ["tag1", "tag2"]
}
```

**Create a New Note**

- URL: /notes
- Method: POST
- Description: Creates a new note. Requires authorization.

**Request Body:**
```json
{
  "title": "New Note",
  "content": "Note Content",
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "message": "Note created successfully",
  "note": {
    "id": 1,
    "title": "New Note",
    "content": "Note Content",
    "tags": ["tag1", "tag2"]
  }
}
```

**Update a Note**
- URL: /notes/{note_id}
- Method: PUT
- Description: Updates an existing note by its ID.

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated Content",
  "tags": ["updated_tag1", "updated_tag2"]
}
```

**Response:**
```json
{
  "message": "Note updated successfully",
  "note": {
    "id": 1,
    "title": "Updated Title",
    "content": "Updated Content",
    "tags": ["updated_tag1", "updated_tag2"]
  }
}
```

**Delete a Note**
- URL: /notes/{note_id}
- Method: DELETE
- Description: Deletes a specific note by its ID.

**Response:**
```json
{
  "message": "Note deleted successfully"
}
```

---

## Telegram Bot Features

### The Telegram bot allows users to interact with their notes. The available bot commands are:

`/start` Starts the bot and authorizes the user.
`/notes` Retrieves a list of the user's notes.
`/add_note` Creates a new note.
`/search_notes` Searches for notes by tags.

___

