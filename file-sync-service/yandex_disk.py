import os
import requests


class YandexDisk:
    def __init__(self, token, folder):
        """
        Конструктор принимает токен и имя папки на Яндекс Диске.
        Сразу настраивает базовый URL и заголовки для всех запросов.
        """
        self.token = token
        self.folder = folder
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {"Authorization": f"OAuth {self.token}"}
        self._ensure_folder_exists()

    def _ensure_folder_exists(self):
        """Проверяет существование папки и создаёт её, если её нет."""
        try:
            params = {"path": f"app:/{self.folder}"}
            response = requests.get(self.base_url, headers=self.headers, params=params)
            if response.status_code == 404:
                self._create_folder()
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при проверке папки: {e}")

    def _create_folder(self):
        """Создаёт корневую папку на Яндекс Диске."""
        params = {"path": f"app:/{self.folder}"}
        response = requests.put(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        print(f"Папка '{self.folder}' создана на Яндекс Диске.")

    def create_folder(self, relative_path):
        """Создаёт папку внутри основной папки на Яндекс Диске."""
        params = {"path": f"app:/{self.folder}/{relative_path}"}
        response = requests.put(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()

    def create_folder_recursive(self, relative_path):
        """
        Рекурсивно создаёт все промежуточные папки для указанного пути.
        Например, для "A/B/C" создаст A, затем A/B, затем A/B/C.
        """
        parts = relative_path.split('/')
        current_path = ""
        
        for part in parts:
            current_path = f"{current_path}/{part}" if current_path else part
            try:
                self.create_folder(current_path)
            except requests.exceptions.HTTPError as e:
                # Если папка уже существует (409), игнорируем ошибку
                if e.response.status_code != 409:
                    raise

    def _get_items_at_path(self, cloud_path):
        """Вспомогательный метод: получает элементы по конкретному пути в облаке."""
        params = {
            "path": cloud_path,
            "limit": 1000,
            "fields": "items.name,items.modified,items.type,items.path"
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("_embedded", {}).get("items", [])

    def get_all_cloud_files(self):
        """
        Рекурсивно получает все файлы из облака.
        Возвращает словарь {относительный_путь: время_изменения}.
        """
        files = {}
        self._collect_files_recursive(f"app:/{self.folder}", "", files)
        return files

    def _collect_files_recursive(self, cloud_path, relative_prefix, files_dict):
        """
        Вспомогательный рекурсивный метод для сбора файлов.
        cloud_path - полный путь в облаке (например, "app:/skillbox_sync")
        relative_prefix - относительный путь от корня (например, "Новая папка")
        files_dict - словарь для накопления результатов
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

    def get_cloud_folders(self):
        """Возвращает множество имён папок в корневой папке облака."""
        items = self._get_items_at_path(f"app:/{self.folder}")
        folders = set()
        for item in items:
            if item["type"] == "dir":
                folders.add(item["name"])
        return folders

    def get_all_cloud_folders(self):
        """
        Рекурсивно получает все папки из облака.
        Возвращает множество относительных путей к папкам.
        """
        folders = set()
        self._collect_folders_recursive(f"app:/{self.folder}", "", folders)
        return folders

    def _collect_folders_recursive(self, cloud_path, relative_prefix, folders_set):
        """
        Вспомогательный рекурсивный метод для сбора папок.
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
        relative_path - путь относительно корневой папки (например, "Новая папка/файл.txt")
        """
        full_path = f"app:/{self.folder}/{relative_path}"
        params = {
            "path": full_path,
            "overwrite": "true"
        }
        response = requests.get(
            f"{self.base_url}/upload", 
            headers=self.headers, 
            params=params
        )
        response.raise_for_status()
        return response.json()["href"]

    def load(self, path, relative_path):
        """
        Загружает файл из локальной папки в облако.
        relative_path - путь относительно корневой папки (например, "Новая папка/файл.txt")
        """
        upload_url = self._get_upload_link(relative_path)
        
        with open(path, "rb") as file:
            response = requests.put(upload_url, data=file)
            response.raise_for_status()

    def reload(self, path, relative_path):
        """
        Перезаписывает файл в облаке (переиспользует метод load).
        """
        self.load(path, relative_path)

    def delete(self, relative_path):
        """
        Удаляет файл или папку из облачного хранилища.
        relative_path - путь относительно корневой папки
        """
        params = {
            "path": f"app:/{self.folder}/{relative_path}",
            "permanently": "true"
        }
        response = requests.delete(
            self.base_url, 
            headers=self.headers, 
            params=params
        )
        response.raise_for_status()