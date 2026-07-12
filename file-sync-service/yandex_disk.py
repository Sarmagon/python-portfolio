"""
Модуль для работы с API Яндекс Диска.
"""

import os
import requests
from exceptions import CloudAPIError, NetworkError, FolderOperationError


class YandexDisk:
    """Класс для взаимодействия с Яндекс Диском через API."""
    
    def __init__(self, token, folder):
        """
        Конструктор принимает токен и имя папки на Яндекс Диске.
        
        Args:
            token (str): OAuth токен доступа.
            folder (str): Имя папки для синхронизации.
            
        Raises:
            CloudAPIError: Если не удалось подключиться к API.
        """
        self.token = token
        self.folder = folder
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {"Authorization": f"OAuth {self.token}"}
        
        try:
            self._ensure_folder_exists()
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка подключения к Яндекс Диску: {e}")
        except Exception as e:
            raise CloudAPIError(f"Неожиданная ошибка при инициализации: {e}")

    def _ensure_folder_exists(self):
        """
        Проверяет существование папки и создаёт её, если её нет.
        
        Raises:
            FolderOperationError: Если не удалось создать или проверить папку.
        """
        try:
            params = {"path": f"app:/{self.folder}"}
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 404:
                self._create_folder()
            elif response.status_code != 200:
                raise CloudAPIError(f"Ошибка проверки папки: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise NetworkError("Превышено время ожидания ответа от Яндекс Диска")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Не удалось подключиться к Яндекс Диску. Проверьте интернет-соединение")
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка при проверке папки: {e}")

    def _create_folder(self):
        """
        Создаёт корневую папку на Яндекс Диске.
        
        Raises:
            FolderOperationError: Если не удалось создать папку.
        """
        try:
            params = {"path": f"app:/{self.folder}"}
            response = requests.put(
                self.base_url, 
                headers=self.headers, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise NetworkError("Превышено время ожидания при создании папки")
        except requests.exceptions.RequestException as e:
            raise FolderOperationError(f"Не удалось создать папку '{self.folder}': {e}")

    def create_folder(self, relative_path):
        """
        Создаёт папку внутри основной папки на Яндекс Диске.
        
        Args:
            relative_path (str): Относительный путь к папке.
            
        Raises:
            FolderOperationError: Если не удалось создать папку.
        """
        try:
            params = {"path": f"app:/{self.folder}/{relative_path}"}
            response = requests.put(
                self.base_url, 
                headers=self.headers, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                # Папка уже существует
                pass
            else:
                raise FolderOperationError(f"Не удалось создать папку '{relative_path}': {e}")
        except requests.exceptions.Timeout:
            raise NetworkError(f"Превышено время ожидания при создании папки '{relative_path}'")
        except requests.exceptions.RequestException as e:
            raise FolderOperationError(f"Ошибка при создании папки '{relative_path}': {e}")

    def create_folder_recursive(self, relative_path):
        """
        Рекурсивно создаёт все промежуточные папки для указанного пути.
        
        Args:
            relative_path (str): Полный относительный путь (например, "A/B/C").
            
        Raises:
            FolderOperationError: Если не удалось создать одну из папок.
        """
        parts = relative_path.split('/')
        current_path = ""

        for part in parts:
            current_path = f"{current_path}/{part}" if current_path else part
            try:
                self.create_folder(current_path)
            except FolderOperationError:
                raise
            except Exception as e:
                raise FolderOperationError(f"Ошибка при создании папки '{current_path}': {e}")

    def _get_items_at_path(self, cloud_path):
        """
        Вспомогательный метод: получает элементы по конкретному пути в облаке.
        
        Args:
            cloud_path (str): Полный путь в облаке.
            
        Returns:
            list: Список элементов (файлов и папок). Если папка не найдена - пустой список.
            
        Raises:
            NetworkError: При проблемах с сетью.
            CloudAPIError: При ошибках API (кроме 404).
        """
        try:
            params = {
                "path": cloud_path,
                "limit": 1000,
                "fields": "items.name,items.modified,items.type,items.path"
            }
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                params=params,
                timeout=30
            )
            
            # Если папка не найдена (404) - возвращаем пустой список
            # Это нормальная ситуация - папка могла быть удалена между получением списка и обходом
            if response.status_code == 404:
                logger.warning(f"⚠️ Папка не найдена (возможно удалена): {cloud_path}")
                return []
            
            response.raise_for_status()
            data = response.json()
            return data.get("_embedded", {}).get("items", [])
            
        except requests.exceptions.Timeout:
            raise NetworkError(f"Превышено время ожидания при чтении '{cloud_path}'")
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка при получении данных из '{cloud_path}': {e}")
        except ValueError as e:
            raise CloudAPIError(f"Ошибка разбора ответа API: {e}")

    def get_all_cloud_files(self):
        """
        Рекурсивно получает все файлы из облака.
        
        Returns:
            dict: Словарь {относительный_путь: время_изменения}.
            
        Raises:
            NetworkError: При проблемах с сетью.
            CloudAPIError: При ошибках API.
        """
        files = {}
        try:
            self._collect_files_recursive(f"app:/{self.folder}", "", files)
            return files
        except Exception as e:
            raise CloudAPIError(f"Ошибка получения списка файлов: {e}")

    def _collect_files_recursive(self, cloud_path, relative_prefix, files_dict):
        """
        Вспомогательный рекурсивный метод для сбора файлов.
        
        Args:
            cloud_path (str): Полный путь в облаке.
            relative_prefix (str): Относительный путь от корня.
            files_dict (dict): Словарь для накопления результатов.
        """
        items = self._get_items_at_path(cloud_path)

        for item in items:
            item_name = item["name"]

            if item["type"] == "dir":
                # Рекурсивно обходим подпапку
                subfolder_path = item.get("path", f"{cloud_path}/{item_name}")
                subfolder_relative = f"{relative_prefix}/{item_name}" if relative_prefix else item_name
                self._collect_files_recursive(subfolder_path, subfolder_relative, files_dict)
            else:
                # Это файл - добавляем в словарь
                file_relative = f"{relative_prefix}/{item_name}" if relative_prefix else item_name
                files_dict[file_relative] = item.get("modified")

    def get_all_cloud_folders(self):
        """
        Рекурсивно получает все папки из облака.
        
        Returns:
            set: Множество относительных путей к папкам.
            
        Raises:
            NetworkError: При проблемах с сетью.
            CloudAPIError: При ошибках API.
        """
        folders = set()
        try:
            self._collect_folders_recursive(f"app:/{self.folder}", "", folders)
            return folders
        except Exception as e:
            raise CloudAPIError(f"Ошибка получения списка папок: {e}")

    def _collect_folders_recursive(self, cloud_path, relative_prefix, folders_set):
        """
        Вспомогательный рекурсивный метод для сбора папок.
        
        Args:
            cloud_path (str): Полный путь в облаке.
            relative_prefix (str): Относительный путь от корня.
            folders_set (set): Множество для накопления результатов.
        """
        items = self._get_items_at_path(cloud_path)

        for item in items:
            if item["type"] == "dir":
                item_name = item["name"]
                folder_relative = f"{relative_prefix}/{item_name}" if relative_prefix else item_name
                folders_set.add(folder_relative)

                # Рекурсивно обходим подпапку
                subfolder_path = item.get("path", f"{cloud_path}/{item_name}")
                self._collect_folders_recursive(subfolder_path, folder_relative, folders_set)

    def _get_upload_link(self, relative_path):
        """
        Вспомогательный метод: получает ссылку для загрузки файла.
        
        Args:
            relative_path (str): Путь относительно корневой папки.
            
        Returns:
            str: Ссылка для загрузки.
            
        Raises:
            NetworkError: При проблемах с сетью.
            CloudAPIError: При ошибках API.
        """
        try:
            full_path = f"app:/{self.folder}/{relative_path}"
            params = {
                "path": full_path,
                "overwrite": "true"
            }
            response = requests.get(
                f"{self.base_url}/upload",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()["href"]
            
        except requests.exceptions.Timeout:
            raise NetworkError(f"Превышено время ожидания при получении ссылки для загрузки '{relative_path}'")
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка при получении ссылки для загрузки '{relative_path}': {e}")
        except (KeyError, ValueError) as e:
            raise CloudAPIError(f"Ошибка разбора ответа API: {e}")

    def load(self, path, relative_path):
        """
        Загружает файл из локальной папки в облако.
        
        Args:
            path (str): Полный путь к локальному файлу.
            relative_path (str): Путь относительно корневой папки.
            
        Raises:
            FileNotFoundError: Если файл не существует.
            CloudAPIError: При ошибках загрузки.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл '{path}' не существует")
        
        try:
            upload_url = self._get_upload_link(relative_path)

            with open(path, "rb") as file:
                response = requests.put(
                    upload_url, 
                    data=file,
                    timeout=300  # 5 минут для больших файлов
                )
                response.raise_for_status()
                
        except FileNotFoundError:
            raise
        except requests.exceptions.Timeout:
            raise NetworkError(f"Превышено время ожидания при загрузке файла '{relative_path}'")
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка при загрузке файла '{relative_path}': {e}")

    def reload(self, path, relative_path):
        """
        Перезаписывает файл в облаке (переиспользует метод load).
        
        Args:
            path (str): Полный путь к локальному файлу.
            relative_path (str): Путь относительно корневой папки.
        """
        self.load(path, relative_path)

    def delete(self, relative_path):
        """
        Удаляет файл или папку из облачного хранилища.
        
        Args:
            relative_path (str): Путь относительно корневой папки.
            
        Raises:
            CloudAPIError: При ошибках удаления.
        """
        try:
            params = {
                "path": f"app:/{self.folder}/{relative_path}",
                "permanently": "true"
            }
            response = requests.delete(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # Файл/папка уже удалена
                raise CloudAPIError(f"Файл/папка '{relative_path}' не найдена (уже удалена)")
            else:
                raise CloudAPIError(f"Ошибка при удалении '{relative_path}': {e}")
        except requests.exceptions.Timeout:
            raise NetworkError(f"Превышено время ожидания при удалении '{relative_path}'")
        except requests.exceptions.RequestException as e:
            raise CloudAPIError(f"Ошибка при удалении '{relative_path}': {e}")