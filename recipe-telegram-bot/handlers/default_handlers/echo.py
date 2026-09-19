from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard
from utils.user_states import UserStates, get_state, set_state, delete_state
from handlers.custom_handlers.search_by_name import process_dish_name
from handlers.custom_handlers.search_by_ingredient import process_ingredient


MENU_BUTTONS = [
    "🔎 Поиск по названию",
    "🥕 Поиск по ингредиентам",
    "📜 История поиска",
    "ℹ️ Помощь"
]


@bot.message_handler(func=lambda message: not message.text.startswith('/') if message.text else False)
def bot_echo(message: Message):
    """💬 Обработчик всех сообщений (КРОМЕ команд!)"""
    
    text = message.text
    if not text:
        return
    
    # 🔎 ПРОВЕРЯЕМ КНОПКИ МЕНЮ ПЕРЕД состоянием!
    if text in MENU_BUTTONS:
        delete_state(message.from_user.id)
    
    # 🔍 Проверяем состояние
    current_state = get_state(message.from_user.id)
    
    # ← ИСПРАВЛЕНО: Преобразуем в строку!
    if str(current_state) == "UserStates:waiting_for_dish_name":
        process_dish_name(message)
        return
    
    if str(current_state) == "UserStates:waiting_for_ingredient":
        process_ingredient(message)
        return
    
    # 🔎 Кнопка: Поиск по названию
    if text == "🔎 Поиск по названию":
        set_state(message.from_user.id, UserStates.waiting_for_dish_name)
        bot.send_message(
            chat_id=message.chat.id,
            text="🔎 **Поиск по названию**\n\n"
                 "Введите название блюда:\n\n"
                 f"🍳 **Примеры:** Pizza, Spaghetti, Chicken, Soup, Burger\n"
                 f"🇷 **По-русски:** пицца, спагетти, курица, суп, бургер\n\n"
                 "❌ Напишите 'Отмена' чтобы вернуться в меню",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # 🥕 Кнопка: Поиск по ингредиентам
    if text == "🥕 Поиск по ингредиентам":
        set_state(message.from_user.id, UserStates.waiting_for_ingredient)
        bot.send_message(
            chat_id=message.chat.id,
            text="🥕 **Поиск по ингредиентам**\n\n"
                 "Введите ингредиент:\n\n"
                 f"🥕 **Примеры:** Cheese, Tomato, Chicken, Garlic, Rice\n"
                 f"🇷 **По-русски:** сыр, томат, курица, чеснок, рис\n\n"
                 "❌ Напишите 'Отмена' чтобы вернуться в меню",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # 📜 Кнопка: История поиска
    if text == "📜 История поиска":
        bot.send_message(
            chat_id=message.chat.id,
            text="📜 **История поиска**\n\n"
                 "Напишите /history для просмотра вашей истории запросов.",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # ℹ️ Кнопка: Помощь
    if text == "ℹ️ Помощь":
        bot.send_message(
            chat_id=message.chat.id,
            text="ℹ️ **Помощь**\n\n"
                 "Напишите /help для полной справки.",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # 💬 Эхо
    bot.send_message(
        chat_id=message.chat.id,
        text=f"🤔 Я пока не понял запрос: **{text}**\n\n"
             "Напишите /help для справки.",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )