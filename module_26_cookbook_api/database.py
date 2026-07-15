"""
Модуль настройки асинхронного подключения к базе данных.

Используется:
- SQLAlchemy 1.4 с асинхронным расширением (create_async_engine)
- aiosqlite как асинхронный драйвер для SQLite
- declarative_base для объявления ORM-моделей
- Dependency Injection для создания сессий (рекомендация FastAPI)
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL подключения к асинхронной SQLite базе данных
# Формат: sqlite+aiosqlite:///./<имя_файла>.db
DATABASE_URL = "sqlite+aiosqlite:///./cookbook.db"

# Создание асинхронного движка (engine) для работы с БД
# echo=False — не выводить SQL-запросы в консоль (для продакшена)
# echo=True — включить для отладки SQL
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика асинхронных сессий
# expire_on_commit=False — атрибуты объектов не будут "протухать" после коммита,
# что важно при работе с async сессиями
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Базовый класс для всех ORM-моделей
Base = declarative_base()


# Функция для внедрения зависимостей (Dependency Injection)
# Создает новую сессию для каждого запроса и гарантированно закрывает её после
# Это безопаснее, чем использовать глобальную сессию
async def get_session() -> AsyncSession:
    """
    Dependency для получения асинхронной сессии БД.
    
    Используется в эндпоинтах через Depends(get_session).
    Создает новую сессию для каждого запроса и закрывает её после завершения.
    
    Yields:
        AsyncSession: асинхронная сессия SQLAlchemy
    """
    async with async_session() as session:
        yield session