from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 МЕНЮ")]
        ],
        resize_keyboard=True
    )

def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Поиск товара", callback_data="search")],
            [InlineKeyboardButton(text="📜 История запросов", callback_data="view_history")],
            [InlineKeyboardButton(text="🔗 Помощь", callback_data="help")],
            [InlineKeyboardButton(text="💬 Поддержка", callback_data="support")],
            [InlineKeyboardButton(text="📝 Написать в поддержку", callback_data="support_beta")]
        ]
    )