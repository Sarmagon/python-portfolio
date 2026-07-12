"""
Модуль для загрузки и валидации конфигурации.
"""

import os
from dotenv import dotenv_values
from exceptions import ConfigError


def load_config():
    """
    Читает файл .env и возвращает словарь с настройками.
    
    Returns:
        dict: Словарь с конфигурацией.
        
    Raises:
        ConfigError: Если файл .env не найден или параметры некорректны.
    """
    if not os.path.exists(".env"):
        raise ConfigError("Файл .env не найден в корневой директории проекта.")
    
    config = dotenv_values(".env")
    
    # Валидация обязательных параметров
    required_params = ["LOCAL_FOLDER", "YANDEX_FOLDER", "YANDEX_TOKEN"]
    missing_params = [param for param in required_params if not config.get(param)]
    
    if missing_params:
        raise ConfigError(
            f"Отсутствуют обязательные параметры в .env: {', '.join(missing_params)}"
        )
    
    # Валидация числовых параметров
    try:
        sync_period = int(config.get("SYNC_PERIOD", 10))
        if sync_period < 1:
            raise ConfigError("SYNC_PERIOD должен быть больше 0.")
    except ValueError:
        raise ConfigError("SYNC_PERIOD должен быть целым числом.")
    
    return config