"""
⌨️ Reply-клавиатуры (кнопки под полем ввода)
"""

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """🏠 Главная клавиатура с кнопками меню"""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    keyboard.row(
        KeyboardButton("🔎 Поиск по названию"),
        KeyboardButton("🥕 Поиск по ингредиентам")
    )
    keyboard.row(
        KeyboardButton("📜 История поиска"),
        KeyboardButton("ℹ️ Помощь")
    )
    
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """❌ Клавиатура с кнопкой отмены"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("❌ Отмена"))
    return keyboard