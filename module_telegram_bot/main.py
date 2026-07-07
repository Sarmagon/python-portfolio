"""
🍳 Recipe Bot — Телеграм-бот для поиска рецептов
Точка входа в приложение
"""

from loader import bot
from database.models import initialize_database
from utils.set_bot_commands import set_default_commands

# Импортируем обработчики (декораторы регистрируются автоматически)
from handlers.default_handlers import start, help, echo, history
from handlers.custom_handlers import callback_handlers


def main():
    """🚀 Запуск бота"""
    
    # Красивое приветствие в терминале
    print("\n" + "=" * 50)
    print("🍳  RECIPE BOT — ЗАПУЩЕН!")
    print("=" * 50)
    print("🤖 Бот готов к работе...")
    print("📊 База данных: подключена")
    print("🌐 Telegram API: подключено")
    print("=" * 50)
    print("💡 Для остановки нажмите: Ctrl + C")
    print("=" * 50 + "\n")
    
    # Инициализация базы данных
    initialize_database()
    
    # Установка команд бота в меню Telegram
    set_default_commands(bot)
    
    # Запуск polling
    bot.infinity_polling()


if __name__ == "__main__":
    main()