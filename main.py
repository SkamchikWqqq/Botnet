from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
import asyncio
from routers.handlers import router

# Хранилище для FSM
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # Подключаем маршруты
    dp.include_router(router)

    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
    
