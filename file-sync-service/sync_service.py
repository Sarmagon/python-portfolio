"""
Модуль основной логики синхронизации.
"""

import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger

from file_manager import get_all_local_files, get_all_local_folders
from exceptions import (
    FileOperationError,
    FolderOperationError,
    NetworkError,
    SyncBaseException
)
from ui import (
    print_sync_start,
    print_sync_summary,
    ProgressTracker,
    format_file_size,
    LoadingAnimation
)


def _delete_file(yandex_client, rel_path):
    """Удаляет файл из облака."""
    start = time.time()
    try:
        yandex_client.delete(rel_path)
        duration = time.time() - start
        return True, None, duration
    except Exception as e:
        duration = time.time() - start
        return False, str(e), duration


def _upload_file(yandex_client, local_folder, rel_path):
    """Загружает файл в облако."""
    start = time.time()
    try:
        full_path = os.path.join(local_folder, rel_path)
        yandex_client.load(full_path, rel_path)
        duration = time.time() - start
        return True, None, duration
    except Exception as e:
        duration = time.time() - start
        return False, str(e), duration


def _update_file(yandex_client, local_folder, rel_path):
    """Обновляет файл в облаке."""
    start = time.time()
    try:
        full_path = os.path.join(local_folder, rel_path)
        yandex_client.reload(full_path, rel_path)
        duration = time.time() - start
        return True, None, duration
    except Exception as e:
        duration = time.time() - start
        return False, str(e), duration


def sync_files(yandex_client, local_folder):
    """Основная логика синхронизации файлов и папок."""
    start_time = time.time()
    print_sync_start()

    stats = {
        'folders_created': 0,
        'files_uploaded': 0,
        'files_updated': 0,
        'files_deleted': 0,
        'folders_deleted': 0,
        'errors': 0
    }

    try:
        # Получение данных из облака
        logger.info("📡 Получаю данные из облака...")
        cloud_animation = LoadingAnimation("Получение данных из облака")
        cloud_animation.start()
        
        cloud_start = time.time()
        try:
            cloud_files = yandex_client.get_all_cloud_files()
            cloud_folders = yandex_client.get_all_cloud_folders()
            cloud_duration = time.time() - cloud_start
            cloud_animation.stop()
            
            logger.info(
                f"✅ Получено: {len(cloud_files)} файлов, "
                f"{len(cloud_folders)} папок (за {cloud_duration:.1f} сек.)"
            )
        except Exception as e:
            cloud_animation.stop()
            raise NetworkError(f"Ошибка получения данных из облака: {e}")

        # Сканирование локальной папки
        logger.info("📂 Сканирую локальную папку...")
        scan_start = time.time()
        try:
            local_files = get_all_local_files(local_folder)
            local_folders = get_all_local_folders(local_folder)
            scan_duration = time.time() - scan_start
            logger.info(
                f"✅ Найдено: {len(local_files)} файлов, "
                f"{len(local_folders)} папок (за {scan_duration:.2f} сек.)"
            )
        except Exception as e:
            raise SyncBaseException(f"Ошибка сканирования локальной папки: {e}")

        # 1. Создание папок (последовательно)
        folders_to_create = [f for f in sorted(local_folders) if f not in cloud_folders]
        if folders_to_create:
            logger.info(f"📂 Создаю {len(folders_to_create)} папок в облаке...")
            folder_progress = ProgressTracker("Создаю папку", len(folders_to_create), "")
            
            for folder_path in folders_to_create:
                folder_progress.start_item(folder_path)
                try:
                    yandex_client.create_folder_recursive(folder_path)
                    stats['folders_created'] += 1
                    folder_progress.finish_item(success=True)
                except Exception as e:
                    logger.error(f"   ❌ Ошибка создания папки {folder_path}: {e}")
                    stats['errors'] += 1
                    folder_progress.finish_item(success=False, error_msg=str(e))
                
                folder_progress.print_eta()

        # 2. Удаление файлов из облака (параллельно)
        files_to_delete = [rel_path for rel_path in cloud_files if rel_path not in local_files]
        if files_to_delete:
            logger.info(f"🗑️ Удаляю {len(files_to_delete)} файлов из облака...")
            delete_animation = LoadingAnimation(f"Удаление {len(files_to_delete)} файлов")
            delete_animation.start()
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(_delete_file, yandex_client, rel_path): rel_path
                    for rel_path in files_to_delete
                }
                
                for future in as_completed(futures):
                    rel_path = futures[future]
                    try:
                        success, error_msg, duration = future.result()
                        if success:
                            logger.info(f"   ✅ Удалён: {rel_path} (за {duration:.1f} сек.)")
                            stats['files_deleted'] += 1
                        else:
                            delete_animation.stop()
                            logger.error(f"   ❌ Ошибка удаления {rel_path}: {error_msg}")
                            stats['errors'] += 1
                    except Exception as e:
                        delete_animation.stop()
                        logger.error(f"   ❌ Ошибка удаления {rel_path}: {e}")
                        stats['errors'] += 1
            
            delete_animation.stop()

        # 3. Удаление папок из облака (последовательно)
        folders_to_delete = [
            f for f in sorted(cloud_folders, key=len, reverse=True) 
            if f not in local_folders
        ]
        if folders_to_delete:
            logger.info(f"🗑️ Удаляю {len(folders_to_delete)} папок из облака...")
            folder_delete_progress = ProgressTracker("Удаляю папку", len(folders_to_delete), "🗑️")
            
            for folder_path in folders_to_delete:
                folder_delete_progress.start_item(folder_path)
                try:
                    yandex_client.delete(folder_path)
                    stats['folders_deleted'] += 1
                    folder_delete_progress.finish_item(success=True)
                except Exception as e:
                    if "404" in str(e):
                        logger.info(f"   ℹ️ Папка {folder_path} уже удалена")
                        folder_delete_progress.finish_item(success=True)
                    else:
                        logger.error(f"   ❌ Ошибка удаления папки {folder_path}: {e}")
                        stats['errors'] += 1
                        folder_delete_progress.finish_item(success=False, error_msg=str(e))
                
                folder_delete_progress.print_eta()

        # 4. Подготовка списков файлов для загрузки и обновления
        files_to_upload = []
        files_to_update = []

        for rel_path, file_info in local_files.items():
            if rel_path not in cloud_files:
                files_to_upload.append((rel_path, file_info))
            else:
                cloud_time_str = cloud_files[rel_path]
                if cloud_time_str:
                    cloud_mtime = datetime.fromisoformat(
                        cloud_time_str.replace('Z', '+00:00')
                    ).timestamp()
                    if file_info['mtime'] > cloud_mtime:
                        files_to_update.append((rel_path, file_info))

        # 5. Загрузка новых файлов (параллельно)
        if files_to_upload:
            logger.info(f"⬆️ Загружаю {len(files_to_upload)} файлов в облако...")
            
            # Показываем список файлов
            for rel_path, file_info in files_to_upload:
                file_size = file_info.get('size', 0)
                size_str = f" ({format_file_size(file_size)})" if file_size else ""
                logger.info(f"   📄 {rel_path}{size_str}")
            
            # Запускаем анимацию
            upload_animation = LoadingAnimation(f"Загрузка {len(files_to_upload)} файлов")
            upload_animation.start()
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(
                        _upload_file, yandex_client, local_folder, rel_path
                    ): (rel_path, file_info)
                    for rel_path, file_info in files_to_upload
                }
                
                for future in as_completed(futures):
                    rel_path, file_info = futures[future]
                    try:
                        success, error_msg, duration = future.result()
                        if success:
                            logger.info(f"   ✅ Загружен: {rel_path} (за {duration:.1f} сек.)")
                            stats['files_uploaded'] += 1
                        else:
                            upload_animation.stop()
                            logger.error(f"   ❌ Ошибка загрузки {rel_path}: {error_msg}")
                            stats['errors'] += 1
                    except Exception as e:
                        upload_animation.stop()
                        logger.error(f"   ❌ Ошибка загрузки {rel_path}: {e}")
                        stats['errors'] += 1
            
            upload_animation.stop()

        # 6. Обновление изменённых файлов (параллельно)
        if files_to_update:
            logger.info(f"🔄 Обновляю {len(files_to_update)} файлов в облаке...")
            
            # Показываем список файлов
            for rel_path, file_info in files_to_update:
                file_size = file_info.get('size', 0)
                size_str = f" ({format_file_size(file_size)})" if file_size else ""
                logger.info(f"    {rel_path}{size_str}")
            
            # Запускаем анимацию
            update_animation = LoadingAnimation(f"Обновление {len(files_to_update)} файлов")
            update_animation.start()
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(
                        _update_file, yandex_client, local_folder, rel_path
                    ): (rel_path, file_info)
                    for rel_path, file_info in files_to_update
                }
                
                for future in as_completed(futures):
                    rel_path, file_info = futures[future]
                    try:
                        success, error_msg, duration = future.result()
                        if success:
                            logger.info(f"   ✅ Обновлён: {rel_path} (за {duration:.1f} сек.)")
                            stats['files_updated'] += 1
                        else:
                            update_animation.stop()
                            logger.error(f"   ❌ Ошибка обновления {rel_path}: {error_msg}")
                            stats['errors'] += 1
                    except Exception as e:
                        update_animation.stop()
                        logger.error(f"   ❌ Ошибка обновления {rel_path}: {e}")
                        stats['errors'] += 1
            
            update_animation.stop()

        # Если ничего не делали
        if not any([
            folders_to_create, files_to_delete, folders_to_delete,
            files_to_upload, files_to_update
        ]):
            logger.info("✅ Все файлы синхронизированы, изменений нет")

    except SyncBaseException as e:
        logger.error(f"❌ Критическая ошибка синхронизации: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Непредвиденная ошибка: {e}")
        raise SyncBaseException(f"Непредвиденная ошибка: {e}")

    duration = time.time() - start_time
    print_sync_summary(stats, duration)