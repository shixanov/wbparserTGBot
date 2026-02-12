from aiogram.types import CallbackQuery
from config import SUPPORT_USERNAME

async def support_handler(call: CallbackQuery):
    await call.message.answer(
        f"📩 Связь с поддержкой:\n{SUPPORT_USERNAME}"
    )
    await call.answer()
