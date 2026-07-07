"""
⚙️ Конфигурация проекта и переменные окружения
"""

import os
from dotenv import load_dotenv

load_dotenv()

# 🤖 Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔑 API ключи (RapidAPI / TheMealDB)
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST", "thecocktaildb.p.rapidapi.com")

# 📋 Команды бота для меню в Telegram
DEFAULT_COMMANDS = [
    ("start", "🚀 Запустить бота"),
    ("help", "📖 Помощь"),
    ("hello_world", "👋 Приветствие"),
    ("history", "📜 История запросов"),
]