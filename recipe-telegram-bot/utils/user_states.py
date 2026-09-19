"""
🤖 Машина состояний для пользователей (FSM)
Используем встроенную FSM от pyTelegramBotAPI
"""

from telebot.handler_backends import State, StatesGroup
from loader import bot


class UserStates(StatesGroup):
    """📋 Состояния пользователя для FSM"""
    
    waiting_for_dish_name = State()
    waiting_for_ingredient = State()


def set_state(user_id: int, state):
    """Установить состояние пользователя"""
    bot.set_state(user_id, state)


def get_state(user_id: int):
    """Получить состояние пользователя"""
    # ← bot.get_state() уже возвращает строку! Не надо .state!
    return bot.get_state(user_id)


def delete_state(user_id: int):
    """Удалить состояние пользователя"""
    bot.delete_state(user_id)