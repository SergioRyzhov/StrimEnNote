import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TOKEN
from bot.handlers import router  # Import your router with handlers

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher with in-memory storage
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # MemoryStorage is optional if you don't need state storage

# Include the router with all your handlers
dp.include_router(router)

# Set bot commands (optional but useful)
async def set_bot_commands():
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description="Get help"),
    ]
    await bot.set_my_commands(commands)

# Startup function
async def on_startup():
    logging.info("Starting bot...")
    await set_bot_commands()

# Shutdown function
async def on_shutdown():
    logging.info("Shutting down bot...")

# Main function to start the bot
async def main():
    await on_startup()  # Run startup logic
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()  # Run shutdown logic

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

