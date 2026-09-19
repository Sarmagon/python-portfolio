from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard


@bot.message_handler(commands=['help'])
def help_command(message: Message):
    """📖 Команда /help"""
    help_text = """
Доступные команды:
/start — 🚀 Запустить бота
/help — 📖 Помощь
/hello_world — 👋 Приветствие
/history — 📜 История запросов

Кнопки меню:
🔎 Поиск по названию
🥕 Поиск по ингредиентам
📜 История поиска
ℹ️ Помощь
"""
    bot.reply_to(
        message,
        help_text,
        reply_markup=get_main_menu_keyboard()
    )