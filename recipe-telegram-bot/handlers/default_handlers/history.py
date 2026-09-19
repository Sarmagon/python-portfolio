from keyboards.inline.recipe_keyboard import get_history_keyboard
from telebot.types import Message
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard
from database.models import SearchHistory, User


@bot.message_handler(commands=['history'])
def history_command(message: Message):
    """📜 Команда /history — показывает историю запросов"""
    
    
    try:
        user = User.get_or_none(User.user_id == message.from_user.id)
        
        
        if not user:
            bot.send_message(
                chat_id=message.chat.id,
                text="📜 **История поиска**\n\n"
                     "Пока история пуста — сделайте первый поиск! 🔍",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            return
        
        history = SearchHistory.select().where(
            SearchHistory.user == user
        ).order_by(SearchHistory.created_at.desc()).limit(10)
        
        
        if history.count() == 0:
            bot.send_message(
                chat_id=message.chat.id,
                text="📜 **История поиска**\n\n"
                     "Пока история пуста — сделайте первый поиск! 🔍",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
            return
        
        history_text = "📜 **История поиска**\n\n"
        for i, record in enumerate(history, 1):
            history_text += f"{i}. 🔍 {record.query} → {record.result_summary}\n"
        
        history_text += f"\nВсего запросов: {history.count()}"
        
        # Добавляем кнопку "Очистить историю"
        bot.send_message(
            chat_id=message.chat.id,
            text=history_text,
            parse_mode="Markdown",
            reply_markup=get_history_keyboard()
        )
        
    except Exception as e:
        print(f"❌ Ошибка истории: {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="📜 **История поиска**\n\n"
                 "Пока история пуста — сделайте первый поиск! 🔍",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )