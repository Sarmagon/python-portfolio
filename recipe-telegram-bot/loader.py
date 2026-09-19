"""
🤖 Инициализация бота
"""

from telebot import TeleBot
from telebot.storage import StateMemoryStorage  # ← ПРАВИЛЬНОЕ НАЗВАНИЕ!
from config_data import config


# Создаём бота с storage для FSM!
bot = TeleBot(token=config.BOT_TOKEN, state_storage=StateMemoryStorage())