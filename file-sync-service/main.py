import os
import time
import sys
import itertools
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    print(f"   ️  Интервал:        {sync_period} сек.")
    print("-"*70 + "\n")


def print_sync_start():
    """Выводит сообщение о начале синхронизации."""
    print("\n🔍 Начинаю синхронизацию...")


def print_sync_end(duration):
    """Выводит сообщение о завершении синхронизации с временем выполнения."""
    print(f"✅ Синхронизация завершена за {duration:.1f} сек.\n")


def print_waiting(seconds):
    """Выводит сообщение об ожидании с обратным отсчетом."""
    print(f"⏳ Ожидание {seconds} секунд до следующей синхронизации...")
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Ожидание: {i} сек. до следующей синхронизации...")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")


def print_sync_summary(stats):
    """Выводит сводку по синхронизации."""
    print(f"\n📊 Статистика синхронизации:")
    print(f"   ➕ Создано: {stats['created']}")
    print(f"   🔄 Обновлено: {stats['updated']}")
    print(f"   ➖ Удалено: {stats['deleted']}")
    print(f"   ❌ Ошибок: {stats['errors']}\n")


class Spinner:
    """Простой спиннер для отображения загрузки."""
    def __init__(self, message="Загрузка..."):
        self.message = message
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '', '⠦', '⠧', '⠇', '⠏'])
        self.running = False

    def __enter__(self):
        self.running = True
        self.thread = None
        return self

    def __exit__(self, *args):
        self.running = False
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

    def update(self):
        """Обновляет спиннер (вызывать в цикле)."""
        if self.running:
            sys.stdout.write(f'\r{next(self.spinner)} {self.message}')
            sys.stdout.flush()


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
    """
    files = {}
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}
    
    for root, dirs, filenames in os.walk(local_folder):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in system_files]
        
        for filename in filenames:
            if filename.startswith('.') or filename in system_files:
                continue
                
            full_path = os.path.join(root, filename)
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


def delete_file(yandex_client, rel_path, logger):
    """Вспомогательная функция для удаления файла."""
    try:
        yandex_client.delete(rel_path)
        logger.info(f"📄 ➖ Удалён файл: {rel_path}")
        print(f"    ➖ Удалён файл: {rel_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка удаления файла {rel_path}: {e}")
        return False


def upload_file(yandex_client, local_folder, rel_path, logger):
    """Вспомогательная функция для загрузки файла."""
    try:
        full_path = os.path.join(local_folder, rel_path.replace('/', os.sep))
        yandex_client.load(full_path, rel_path)
        logger.info(f"📄 ⬆️  Загружен: {rel_path}")
        print(f"   📄 ️  Загружен: {rel_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки файла {rel_path}: {e}")
        return False


def update_file(yandex_client, local_folder, rel_path, logger):
    """Вспомогательная функция для обновления файла."""
    try:
        full_path = os.path.join(local_folder, rel_path.replace('/', os.sep))
        yandex_client.reload(full_path, rel_path)
        logger.info(f"📄 🔄 Обновлён: {rel_path}")
        print(f"   📄 🔄 Обновлён: {rel_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка обновления файла {rel_path}: {e}")
        return False


def sync_files(yandex_client, local_folder, logger):
    """Основная логика синхронизации файлов и папок."""
    start_time = time.time()
    print_sync_start()
    
    stats = {'created': 0, 'updated': 0, 'deleted': 0, 'errors': 0}
    
    try:
        # Показываем прогресс получения данных
        print("   📡 Получаю данные из облака...")
        cloud_files = yandex_client.get_all_cloud_files()
        cloud_folders = yandex_client.get_all_cloud_folders()
        print(f"   ✅ Получено: {len(cloud_files)} файлов, {len(cloud_folders)} папок")
        
        print("   📂 Сканирую локальную папку...")
        local_files = get_all_local_files(local_folder)
        local_folders = get_all_local_folders(local_folder)
        print(f"   ✅ Найдено: {len(local_files)} файлов, {len(local_folders)} папок")
        
        # 1. Создаём папки (последовательно)
        folders_to_create = [f for f in sorted(local_folders) if f not in cloud_folders]
        if folders_to_create:
            print(f"\n   📂 Создаю {len(folders_to_create)} папок в облаке...")
            for folder_path in folders_to_create:
                try:
                    yandex_client.create_folder_recursive(folder_path)
                    logger.info(f"📂  Создана папка: {folder_path}")
                    print(f"   📂 ➕ Создана папка: {folder_path}")
                    stats['created'] += 1
                except Exception as e:
                    logger.error(f"❌ Ошибка создания папки {folder_path}: {e}")
                    print(f"   ❌ Ошибка создания папки {folder_path}: {e}")
                    stats['errors'] += 1
        
        # 2. Удаляем файлы из облака (параллельно)
        files_to_delete = [rel_path for rel_path in cloud_files if rel_path not in local_files]
        if files_to_delete:
            print(f"\n   🗑️  Удаляю {len(files_to_delete)} файлов из облака...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(delete_file, yandex_client, rel_path, logger): rel_path 
                    for rel_path in files_to_delete
                }
                for future in as_completed(futures):
                    try:
                        if future.result():
                            stats['deleted'] += 1
                        else:
                            stats['errors'] += 1
                    except Exception as e:
                        rel_path = futures[future]
                        logger.error(f"❌ Ошибка удаления файла {rel_path}: {e}")
                        stats['errors'] += 1
        
        # 3. Удаляем папки из облака (последовательно, от вложенных к корневым)
        folders_to_delete = [f for f in sorted(cloud_folders, key=len, reverse=True) if f not in local_folders]
        if folders_to_delete:
            print(f"\n   🗑️  Удаляю {len(folders_to_delete)} папок из облака...")
            for folder_path in folders_to_delete:
                try:
                    yandex_client.delete(folder_path)
                    logger.info(f"📂 ➖ Удалена папка: {folder_path}")
                    print(f"   📂 ➖ Удалена папка: {folder_path}")
                    stats['deleted'] += 1
                except Exception as e:
                    if "404" in str(e):
                        logger.info(f"📂 ℹ️  Папка {folder_path} уже удалена")
                    else:
                        logger.error(f"❌ Ошибка удаления папки {folder_path}: {e}")
                        print(f"   ❌ Ошибка удаления папки {folder_path}: {e}")
                        stats['errors'] += 1
        
        # 4. Подготавливаем списки файлов для загрузки и обновления
        files_to_upload = []
        files_to_update = []
        
        for rel_path, local_mtime in local_files.items():
            if rel_path not in cloud_files:
                files_to_upload.append((rel_path, local_mtime))
            else:
                cloud_time_str = cloud_files[rel_path]
                if cloud_time_str:
                    cloud_mtime = datetime.fromisoformat(cloud_time_str.replace('Z', '+00:00')).timestamp()
                    if local_mtime > cloud_mtime:
                        files_to_update.append((rel_path, local_mtime))
        
        # 5. Загружаем новые файлы (параллельно)
        if files_to_upload:
            print(f"\n   ⬆️  Загружаю {len(files_to_upload)} файлов в облако...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(upload_file, yandex_client, local_folder, rel_path, logger): rel_path 
                    for rel_path, _ in files_to_upload
                }
                for future in as_completed(futures):
                    try:
                        if future.result():
                            stats['created'] += 1
                        else:
                            stats['errors'] += 1
                    except Exception as e:
                        rel_path = futures[future]
                        logger.error(f" Ошибка загрузки файла {rel_path}: {e}")
                        stats['errors'] += 1
        
        # 6. Обновляем изменённые файлы (параллельно)
        if files_to_update:
            print(f"\n   🔄 Обновляю {len(files_to_update)} файлов в облаке...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(update_file, yandex_client, local_folder, rel_path, logger): rel_path 
                    for rel_path, _ in files_to_update
                }
                for future in as_completed(futures):
                    try:
                        if future.result():
                            stats['updated'] += 1
                        else:
                            stats['errors'] += 1
                    except Exception as e:
                        rel_path = futures[future]
                        logger.error(f"❌ Ошибка обновления файла {rel_path}: {e}")
                        stats['errors'] += 1
        
        # Если ничего не делали
        if not any([folders_to_create, files_to_delete, folders_to_delete, files_to_upload, files_to_update]):
            print("\n    Все файлы синхронизированы, изменений нет")
        
        print_sync_summary(stats)
                        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        print(f"   ❌ Критическая ошибка: {e}")
    
    duration = time.time() - start_time
    print_sync_end(duration)


def main():
    """Точка входа в программу."""
    print_header()
    
    config = load_config()
    
    local_folder = config.get("LOCAL_FOLDER")
    yandex_folder = config.get("YANDEX_FOLDER")
    token = config.get("YANDEX_TOKEN")
    sync_period = int(config.get("SYNC_PERIOD", 10))
    log_file = config.get("LOG_FILE", "sync.log")

    if not os.path.exists(local_folder):
        print(f"❌ Ошибка: Папка '{local_folder}' не существует.")
        print(f"   Проверьте параметр LOCAL_FOLDER в файле .env")
        return

    print_config_info(local_folder, yandex_folder, sync_period)
    
    setup_logger(log_file)
    logger.info(f"Программа синхронизации файлов начинает работу с директорией {local_folder}.")

    yandex_client = YandexDisk(token, yandex_folder)

    print(" Сервис запущен и готов к работе!\n")

    try:
        while True:
            sync_files(yandex_client, local_folder, logger)
            print_waiting(sync_period)
    except KeyboardInterrupt:
        print("\n\n🛑 Сервис остановлен пользователем (Ctrl+C)")
        print("До свидания! 👋\n")


if __name__ == "__main__":
    main()