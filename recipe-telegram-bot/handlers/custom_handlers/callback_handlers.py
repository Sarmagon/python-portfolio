from telebot.types import CallbackQuery
from loader import bot
from keyboards.reply.main_menu import get_main_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "clear_history")
def callback_clear_history(call: CallbackQuery):
    """🗑️ Кнопка 'Очистить историю'"""
    from database.models import SearchHistory, User
    
    try:
        user = User.get_or_none(User.user_id == call.from_user.id)
        if user:
            SearchHistory.delete().where(SearchHistory.user == user).execute()
            bot.answer_callback_query(call.id, "История очищена!")
            bot.send_message(
                chat_id=call.message.chat.id,
                text="✅ **История очищена!**\n\nСделайте новый поиск! 🔍",
                parse_mode="Markdown",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            bot.answer_callback_query(call.id, "История пуста!")
    except Exception as e:
        print(f"❌ Ошибка очистки истории: {e}")
        bot.answer_callback_query(call.id, "Ошибка!")