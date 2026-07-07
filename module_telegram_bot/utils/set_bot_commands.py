from telebot import TeleBot
from telebot.types import BotCommand

from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """Устанавливает список команд, отображаемый в меню Telegram-клиента."""
    bot.set_my_commands(
        [BotCommand(name, description) for name, description in DEFAULT_COMMANDS]
    )
