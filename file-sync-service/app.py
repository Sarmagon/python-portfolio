"""
Модуль запуска приложения.
Содержит основную логику инициализации и запуска сервиса.
"""

import os
import time
from loguru import logger

from config import load_config
from ui import setup_logger, print_header, print_config_info
from yandex_disk import YandexDisk
from sync_service import sync_files
from exceptions import ConfigError, SyncBaseException


def run_service():
    """
    Основная функция запуска сервиса.
    """
    # 1. Загружаем конфигурацию (пока используем обычный print для критических ошибок)
    try:
        config = load_config()
    except ConfigError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        print("Проверьте файл .env")
        return
    except Exception as e:
        print(f"❌ Неожиданная ошибка при загрузке конфигурации: {e}")
        return

    local_folder = config.get("LOCAL_FOLDER")
    yandex_folder = config.get("YANDEX_FOLDER")
    token = config.get("YANDEX_TOKEN")
    sync_period = int(config.get("SYNC_PERIOD", 10))
    log_file = config.get("LOG_FILE", "sync.log")

    # 2. СРАЗУ настраиваем логгер, чтобы все дальнейшие выводы были чистыми!
    setup_logger(log_file)

    # 3. Выводим заголовок и настройки
    print_header()
    print_config_info(local_folder, yandex_folder, sync_period)

    # Проверка локальной папки
    if not os.path.exists(local_folder):
        logger.error(f"❌ Ошибка: Папка '{local_folder}' не существует.")
        logger.error("Проверьте параметр LOCAL_FOLDER в файле .env")
        return

    logger.info("Программа синхронизации файлов начинает работу.")
    logger.info(f"Локальная директория: {local_folder}")
    logger.info(f"Облачная директория: {yandex_folder}")

    # Инициализация клиента Яндекс Диска
    try:
        yandex_client = YandexDisk(token, yandex_folder)
        logger.info("Клиент Яндекс Диска успешно инициализирован")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации клиента Яндекс Диска: {e}")
        return

    logger.info("")
    logger.info("✅ Сервис запущен и готов к работе!")
    logger.info("")

    # Основной цикл синхронизации
    try:
        while True:
            try:
                sync_files(yandex_client, local_folder)
            except SyncBaseException as e:
                logger.error(f"❌ Ошибка синхронизации: {e}")
            except Exception as e:
                logger.error(f"❌ Неожиданная ошибка при синхронизации: {e}")
            
            logger.info(f"⏳ Ожидание {sync_period} секунд до следующей синхронизации...")
            logger.info("")
            time.sleep(sync_period)
            
    except KeyboardInterrupt:
        logger.info("🛑 Сервис остановлен пользователем (Ctrl+C)")
        logger.info("До свидания! 👋")