import os
import time
from datetime import datetime
from dotenv import dotenv_values
from loguru import logger
from yandex_disk import YandexDisk


def load_config():
    """Читает файл .env и возвращает словарь с настройками."""
    return dotenv_values(".env")


def setup_logger(log_file):
    """Настраивает логгер loguru для записи в файл и вывода в консоль."""
    logger.remove()
    log_format = "synchroniser {time:YYYY-MM-DD HH:mm:ss,SSS} {level} {message}"
    logger.add(log_file, format=log_format, encoding="utf-8")
    logger.add(lambda msg: print(msg, end=""), format=log_format)


def print_header():
    """Выводит красивый заголовок при запуске программы."""
    print("\n" + "="*70)
    print("🔄  СЕРВИС СИНХРОНИЗАЦИИ ФАЙЛОВ С ЯНДЕКС ДИСКОМ")
    print("="*70 + "\n")


def print_config_info(local_folder, yandex_folder, sync_period):
    """Выводит информацию о конфигурации."""
    print("⚙️  НАСТРОЙКИ:")
    print(f"   📁 Локальная папка: {local_folder}")
    print(f"   ☁️  Облачная папка:  {yandex_folder}")
    print(f"   ⏱️  Интервал:        {sync_period} сек.")
    print("-"*70 + "\n")


def print_sync_start():
    """Выводит сообщение о начале синхронизации."""
    print("\n🔍 Начинаю синхронизацию...")


def print_sync_end():
    """Выводит сообщение о завершении синхронизации."""
    print("✅ Синхронизация завершена\n")


def print_waiting(seconds):
    """Выводит сообщение об ожидании."""
    print(f"⏳ Ожидание {seconds} секунд до следующей синхронизации...\n")


def get_local_items(local_folder):
    """
    Возвращает словарь {имя: {'type': 'file'/'dir', 'modified': timestamp}}
    для элементов в корневой папке.
    """
    items = {}
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}
    
    for name in os.listdir(local_folder):
        if name.startswith('.') or name in system_files:
            continue
            
        full_path = os.path.join(local_folder, name)
        if os.path.isfile(full_path):
            items[name] = {
                'type': 'file',
                'modified': os.path.getmtime(full_path)
            }
        elif os.path.isdir(full_path):
            items[name] = {
                'type': 'dir',
                'modified': os.path.getmtime(full_path)
            }
            
    return items


def get_all_local_files(local_folder):
    """
    Рекурсивно получает все файлы из локальной папки.
    Возвращает словарь {относительный_путь: время_изменения}.
    Пути используют прямой слэш для совместимости с облаком.
    """
    files = {}
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}
    
    for root, dirs, filenames in os.walk(local_folder):
        # Удаляем скрытые и системные папки из обхода
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in system_files]
        
        for filename in filenames:
            if filename.startswith('.') or filename in system_files:
                continue
                
            full_path = os.path.join(root, filename)
            # Относительный путь с прямыми слэшами
            rel_path = os.path.relpath(full_path, local_folder).replace(os.sep, '/')
            files[rel_path] = os.path.getmtime(full_path)
            
    return files


def get_all_local_folders(local_folder):
    """
    Рекурсивно получает все папки из локальной файловой системы.
    Возвращает множество относительных путей к папкам.
    """
    folders = set()
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}
    
    for root, dirs, _ in os.walk(local_folder):
        # Удаляем скрытые и системные папки из обхода
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in system_files]
        
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(full_path, local_folder).replace(os.sep, '/')
            folders.add(rel_path)
            
    return folders


def get_local_folders(local_folder):
    """Возвращает множество имён папок в корневой папке."""
    folders = set()
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}
    
    for name in os.listdir(local_folder):
        if name.startswith('.') or name in system_files:
            continue
        full_path = os.path.join(local_folder, name)
        if os.path.isdir(full_path):
            folders.add(name)
            
    return folders


def sync_files(yandex_client, local_folder, logger):
    """Основная логика синхронизации файлов и папок."""
    print_sync_start()
    
    try:
        cloud_files = yandex_client.get_all_cloud_files()
        local_files = get_all_local_files(local_folder)
        local_folders = get_all_local_folders(local_folder)
        cloud_folders = yandex_client.get_all_cloud_folders()
        
        # 1. Создаём все папки в облаке (включая вложенные), которых нет
        for folder_path in sorted(local_folders):
            if folder_path not in cloud_folders:
                try:
                    yandex_client.create_folder_recursive(folder_path)
                    logger.info(f"Папка {folder_path} создана на облаке.")
                    print(f"   📂 ➕ Создана папка: {folder_path}")
                except Exception as e:
                    logger.error(f"Папка {folder_path} не создана. {e}")
                    print(f"   ❌ Ошибка создания папки {folder_path}: {e}")
        
        # 2. Удаляем из облака файлы, которых нет локально
        for rel_path in cloud_files:
            if rel_path not in local_files:
                try:
                    yandex_client.delete(rel_path)
                    logger.info(f"Файл {rel_path} удален из облака.")
                    print(f"   📄 ➖ Удалён файл: {rel_path}")
                except Exception as e:
                    logger.error(f"Файл {rel_path} не удален. {e}")
                    print(f"   ❌ Ошибка удаления файла {rel_path}: {e}")
        
        # 3. Удаляем из облака папки, которых нет локально
        # Сортируем по длине пути в обратном порядке (от вложенных к корневым)
        for folder_path in sorted(cloud_folders, key=len, reverse=True):
            if folder_path not in local_folders:
                try:
                    yandex_client.delete(folder_path)
                    logger.info(f"Папка {folder_path} удалена из облака.")
                    print(f"   📂 ➖ Удалена папка: {folder_path}")
                except Exception as e:
                    # Игнорируем ошибку 404 (папка уже удалена как часть родительской)
                    if "404" in str(e):
                        logger.info(f"Папка {folder_path} уже удалена (входит в удалённую родительскую папку).")
                    else:
                        logger.error(f"Папка {folder_path} не удалена. {e}")
                        print(f"   ❌ Ошибка удаления папки {folder_path}: {e}")
        
        # 4. Загружаем или обновляем файлы
        for rel_path, local_mtime in local_files.items():
            if rel_path not in cloud_files:
                # Файла нет в облаке - загружаем
                try:
                    full_path = os.path.join(local_folder, rel_path.replace('/', os.sep))
                    yandex_client.load(full_path, rel_path)
                    logger.info(f"Файл {rel_path} успешно загружен.")
                    print(f"   📄 ⬆️  Загружен: {rel_path}")
                except Exception as e:
                    logger.error(f"Файл {rel_path} не загружен. {e}")
                    print(f"   ❌ Ошибка загрузки файла {rel_path}: {e}")
            else:
                # Файл есть - сравниваем время изменения
                cloud_time_str = cloud_files[rel_path]
                if cloud_time_str:
                    cloud_mtime = datetime.fromisoformat(cloud_time_str.replace('Z', '+00:00')).timestamp()
                    
                    if local_mtime > cloud_mtime:
                        try:
                            full_path = os.path.join(local_folder, rel_path.replace('/', os.sep))
                            yandex_client.reload(full_path, rel_path)
                            logger.info(f"Файл {rel_path} успешно перезаписан.")
                            print(f"   📄 🔄 Обновлён: {rel_path}")
                        except Exception as e:
                            logger.error(f"Файл {rel_path} не перезаписан. {e}")
                            print(f"   ❌ Ошибка обновления файла {rel_path}: {e}")
                        
    except Exception as e:
        logger.error(f"Ошибка соединения или чтения: {e}")
        print(f"   ❌ Критическая ошибка: {e}")
    
    print_sync_end()


def main():
    """Точка входа в программу."""
    print_header()
    
    config = load_config()
    
    local_folder = config.get("LOCAL_FOLDER")
    yandex_folder = config.get("YANDEX_FOLDER")
    token = config.get("YANDEX_TOKEN")
    sync_period = int(config.get("SYNC_PERIOD", 10))
    log_file = config.get("LOG_FILE", "sync.log")

    # Проверка существования локальной папки
    if not os.path.exists(local_folder):
        print(f"❌ Ошибка: Папка '{local_folder}' не существует.")
        print(f"   Проверьте параметр LOCAL_FOLDER в файле .env")
        return

    print_config_info(local_folder, yandex_folder, sync_period)
    
    setup_logger(log_file)
    logger.info(f"Программа синхронизации файлов начинает работу с директорией {local_folder}.")

    yandex_client = YandexDisk(token, yandex_folder)

    print("🚀 Сервис запущен и готов к работе!\n")

    # Бесконечный цикл синхронизации
    try:
        while True:
            sync_files(yandex_client, local_folder, logger)
            print_waiting(sync_period)
            time.sleep(sync_period)
    except KeyboardInterrupt:
        print("\n\n🛑 Сервис остановлен пользователем (Ctrl+C)")
        print("До свидания! 👋\n")


if __name__ == "__main__":
    main()