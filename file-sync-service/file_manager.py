"""
Модуль для работы с локальной файловой системой.
"""

import os
from loguru import logger
from exceptions import LocalFolderError


def get_all_local_files(local_folder):
    """
    Рекурсивно получает все файлы из локальной папки.
    Игнорирует системные, скрытые и временные файлы.
    
    Returns:
        dict: Словарь {относительный_путь: {'mtime': float, 'size': int}}.
    """
    if not os.path.exists(local_folder):
        raise LocalFolderError(f"Папка '{local_folder}' не существует.")
    
    if not os.path.isdir(local_folder):
        raise LocalFolderError(f"'{local_folder}' не является папкой.")
    
    files = {}
    # Системные файлы и префиксы временных файлов
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}

    try:
        for root, dirs, filenames in os.walk(local_folder):
            # Игнорируем скрытые папки, папки с ~$ и системные папки
            dirs[:] = [
                d for d in dirs 
                if not d.startswith('.') and not d.startswith('~$') and d not in system_files
            ]

            for filename in filenames:
                # Игнорируем скрытые файлы, временные файлы (~$) и системные файлы
                if filename.startswith('.') or filename.startswith('~$') or filename in system_files:
                    continue

                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, local_folder).replace(os.sep, '/')
                
                try:
                    # Пытаемся получить метаданные файла
                    files[rel_path] = {
                        'mtime': os.path.getmtime(full_path),
                        'size': os.path.getsize(full_path)
                    }
                except PermissionError:
                    # Если файл заблокирован другой программой (например, Excel), просто пропускаем его
                    logger.warning(f"⚠️ Пропущен заблокированный файл: {rel_path}")
                    continue
                except OSError as e:
                    logger.warning(f"⚠️ Пропущен файл {rel_path} (ошибка доступа): {e}")
                    continue

        return files
        
    except PermissionError as e:
        raise LocalFolderError(f"Нет прав доступа к папке '{local_folder}': {e}")
    except OSError as e:
        raise LocalFolderError(f"Ошибка чтения папки '{local_folder}': {e}")


def get_all_local_folders(local_folder):
    """
    Рекурсивно получает все папки из локальной файловой системы.
    
    Returns:
        set: Множество относительных путей к папкам.
    """
    if not os.path.exists(local_folder):
        raise LocalFolderError(f"Папка '{local_folder}' не существует.")
    
    if not os.path.isdir(local_folder):
        raise LocalFolderError(f"'{local_folder}' не является папкой.")
    
    folders = set()
    system_files = {'desktop.ini', 'Thumbs.db', '.DS_Store'}

    try:
        for root, dirs, _ in os.walk(local_folder):
            # Игнорируем скрытые папки, папки с ~$ и системные папки
            dirs[:] = [
                d for d in dirs 
                if not d.startswith('.') and not d.startswith('~$') and d not in system_files
            ]

            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                rel_path = os.path.relpath(full_path, local_folder).replace(os.sep, '/')
                folders.add(rel_path)

        return folders
        
    except PermissionError as e:
        raise LocalFolderError(f"Нет прав доступа к папке '{local_folder}': {e}")
    except OSError as e:
        raise LocalFolderError(f"Ошибка чтения папки '{local_folder}': {e}")