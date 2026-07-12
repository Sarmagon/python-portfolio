"""
Модуль кастомных исключений для сервиса синхронизации.
"""


class SyncBaseException(Exception):
    """Базовое исключение для всех ошибок синхронизации."""
    pass


class ConfigError(SyncBaseException):
    """Ошибка конфигурации (неверные параметры в .env)."""
    pass


class LocalFolderError(SyncBaseException):
    """Ошибка работы с локальной папкой."""
    pass


class CloudAPIError(SyncBaseException):
    """Ошибка работы с API Яндекс Диска."""
    pass


class FileOperationError(SyncBaseException):
    """Ошибка операции с файлом (чтение/запись/удаление)."""
    pass


class FolderOperationError(SyncBaseException):
    """Ошибка операции с папкой (создание/удаление)."""
    pass


class NetworkError(SyncBaseException):
    """Ошибка сети при работе с облаком."""
    pass