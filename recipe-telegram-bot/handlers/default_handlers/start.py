from telebot.types import Message
from loader import bot
from database.models import User
from keyboards.reply.main_menu import get_main_menu_keyboard


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """🚀 Команда /start"""
    User.get_or_create(
        user_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name or "",
            "last_name": message.from_user.last_name,
        },
    )
    bot.reply_to(
        message,
        f"Привет, {message.from_user.first_name}! 🍳\n"
        "Я бот для поиска рецептов.\n"
        "Напиши /help, чтобы узнать, что я умею.",
        reply_markup=get_main_menu_keyboard()
    )


@bot.message_handler(commands=['hello_world'])
def handle_hello_world(message: Message):
    """👋 Команда /hello_world"""
    bot.reply_to(
        message,
        "👋 Привет! Я бот для поиска рецептов. 🍳\n"
        "📖 Напиши /help для справки.",
        reply_markup=get_main_menu_keyboard()
    )


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def handle_hello_text(message: Message):
    """💬 Обработчик текста 'Привет'"""
    bot.reply_to(
        message,
        "👋 И тебе привет! Давай готовить что-нибудь вкусное? 🥗",
        reply_markup=get_main_menu_keyboard()
    )