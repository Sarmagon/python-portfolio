"""
Модуль пользовательского интерфейса (логирование и вывод).
"""

import sys
import time
import threading
from loguru import logger


def setup_logger(log_file):
    """
    Настраивает логгер loguru для записи в файл и вывода в консоль.
    """
    # Удаляем ВСЕ существующие хендлеры (включая стандартный)
    logger.remove()
    
    # Формат для файла (подробный с временем)
    file_format = "synchroniser {time:YYYY-MM-DD HH:mm:ss,SSS} {level} {message}"
    logger.add(log_file, format=file_format, encoding="utf-8")
    
    # Формат для консоли (только сообщение, без технических деталей)
    console_format = "{message}"
    logger.add(
        sys.stdout,
        format=console_format,
        colorize=False,
        level="INFO"
    )


def print_header():
    """Выводит заголовок программы."""
    logger.info("=" * 70)
    logger.info("🔄  СЕРВИС СИНХРОНИЗАЦИИ ФАЙЛОВ С ЯНДЕКС ДИСКОМ")
    logger.info("=" * 70)


def print_config_info(local_folder, yandex_folder, sync_period):
    """Выводит информацию о настройках."""
    logger.info("")
    logger.info("⚙️  НАСТРОЙКИ:")
    logger.info(f"   📁 Локальная папка: {local_folder}")
    logger.info(f"   ☁️  Облачная папка:  {yandex_folder}")
    logger.info(f"   ⏱️  Интервал:        {sync_period} сек.")
    logger.info("-" * 70)


def print_sync_start():
    """Выводит сообщение о начале синхронизации."""
    logger.info("")
    logger.info("🔍 Начинаю синхронизацию...")


def print_sync_summary(stats, duration):
    """Выводит сводку по результатам синхронизации."""
    logger.info("")
    logger.info("✅ Синхронизация завершена")
    logger.info(f"    Создано папок: {stats['folders_created']}")
    logger.info(f"    Загружено файлов: {stats['files_uploaded']}")
    logger.info(f"   🔄 Обновлено файлов: {stats['files_updated']}")
    logger.info(f"   🗑️ Удалено файлов: {stats['files_deleted']}")
    logger.info(f"   🗑️ Удалено папок: {stats['folders_deleted']}")
    logger.info(f"   ❌ Ошибок: {stats['errors']}")
    logger.info(f"   ️ Общее время: {duration:.2f} сек.")


def print_waiting(sync_period):
    """Выводит сообщение об ожидании следующей синхронизации."""
    logger.info(f" Ожидание {sync_period} секунд до следующей синхронизации...")
    logger.info("")


def format_file_size(size_bytes):
    """Форматирует размер файла в читаемый вид."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


class ProgressTracker:
    """Класс для отслеживания прогресса последовательных операций."""
    
    def __init__(self, operation_name, total_items, emoji="📄"):
        self.operation_name = operation_name
        self.total_items = total_items
        self.emoji = emoji
        self.current = 0
        self.start_time = time.time()
        self.item_start_time = None
    
    def start_item(self, item_name, item_size=None):
        """Начинает отслеживание элемента."""
        self.current += 1
        self.item_start_time = time.time()
        
        size_str = f" ({format_file_size(item_size)})" if item_size else ""
        logger.info(
            f"{self.emoji} [{self.current}/{self.total_items}] "
            f"{self.operation_name} {item_name}{size_str} ... "
        )
    
    def finish_item(self, success=True, error_msg=None):
        """Завершает отслеживание элемента."""
        item_duration = time.time() - self.item_start_time
        
        if success:
            logger.info(f"   ✅ Завершено за {item_duration:.1f} сек.")
        else:
            logger.info(f"   ❌ Ошибка: {error_msg} ({item_duration:.1f} сек.)")
        
        return item_duration
    
    def get_elapsed_time(self):
        """Возвращает общее время операции."""
        return time.time() - self.start_time
    
    def get_eta(self):
        """Возвращает примерное оставшееся время."""
        if self.current == 0:
            return None
        
        elapsed = time.time() - self.start_time
        avg_time_per_item = elapsed / self.current
        remaining_items = self.total_items - self.current
        return avg_time_per_item * remaining_items
    
    def print_eta(self):
        """Выводит информацию о прогрессе и ETA."""
        elapsed = self.get_elapsed_time()
        eta = self.get_eta()
        
        eta_str = f" | Осталось: ~{eta:.0f} сек." if eta is not None else ""
        logger.info(
            f"   ⏱️ Прошло: {elapsed:.1f} сек.{eta_str} "
            f"({self.current}/{self.total_items})"
        )


class LoadingAnimation:
    """
    Анимация загрузки с таймером в реальном времени.
    Показывает бегущий спиннер и время выполнения в фоне.
    """
    
    SPINNERS = ['', '⠙', '⠹', '⠸', '⠼', '', '⠦', '', '⠇', '⠏']
    
    def __init__(self, message):
        """
        Args:
            message (str): Сообщение для отображения (например, "Загрузка файлов").
        """
        self.message = message
        self.start_time = time.time()
        self.stop_event = threading.Event()
        self.thread = None
    
    def _animate(self):
        """Фоновый поток анимации."""
        i = 0
        while not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            
            # Форматируем время
            if elapsed < 60:
                time_str = f"{elapsed:.0f} сек."
            else:
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                time_str = f"{minutes} мин. {seconds} сек."
            
            spinner = self.SPINNERS[i % len(self.SPINNERS)]
            
            # Выводим в консоль (перезаписывая текущую строку)
            sys.stdout.write(f"\r   {spinner} {self.message} ({time_str})   ")
            sys.stdout.flush()
            
            i += 1
            self.stop_event.wait(0.3)  # Обновление каждые 0.3 сек
        
        # Очищаем строку после остановки
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
    
    def start(self):
        """Запускает анимацию."""
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Останавливает анимацию."""
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1)