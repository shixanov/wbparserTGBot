import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN

from handlers.start import start_handler, menu_handler 
from handlers.help import help_handler
from handlers.support import support_handler
from handlers.search import search_start, search_process, show_history, close_history
from handlers.support_beta import router as support_router

from states.search_state import SearchState

from config import BOT_TOKEN
async def main():
    if not BOT_TOKEN:
        exit("Ошибка: Токен не найден! Проверь файл .env")
    
    logging.basicConfig(level=logging.INFO)

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(support_router)

    dp.message.register(start_handler, F.text == "/start")
    dp.message.register(menu_handler, F.text == "📱 МЕНЮ")

    dp.callback_query.register(search_start, F.data == "search")
    dp.message.register(search_process, SearchState.query)
    dp.callback_query.register(show_history, F.data == "view_history") 
    dp.callback_query.register(close_history, F.data == "close_history")
    dp.callback_query.register(help_handler, F.data == "help")
    dp.callback_query.register(support_handler, F.data == "support")

    print("Бот запущен и готов к работе! 🚀")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен! ‼')