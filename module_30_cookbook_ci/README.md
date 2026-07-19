# 🍳 Cookbook API

Асинхронное REST API для управления кулинарной книгой, разработанное на **FastAPI** и **Async SQLAlchemy**. 

Проект создан в рамках портфолио Backend-разработчика и демонстрирует применение лучших практик индустрии: внедрение зависимостей (Dependency Injection), управление жизненным циклом через `lifespan`, строгую типизацию, предотвращение проблемы N+1 запросов и покрытие интеграционными тестами.

---

## 🚀 Ключевые особенности

- ✅ **Асинхронная работа с БД**: Использование `asyncio`, `SQLAlchemy 1.4+` и `aiosqlite` (архитектура готова к миграции на PostgreSQL).
- ✅ **Профессиональная архитектура**: Использование Dependency Injection (`Depends(get_session)`) для изоляции сессий БД и контекстного менеджера `lifespan` для инициализации.
- ✅ **Умная сортировка**: Рецепты сортируются по убыванию просмотров (`views DESC`), а при равенстве — по возрастанию времени приготовления (`cook_time ASC`).
- ✅ **Автосчетчик просмотров**: Поле `views` инкрементируется при каждом запросе деталей рецепта (`GET /recipes/{id}`).
- ✅ **Оптимизация запросов**: Использование `selectinload` для жадной подгрузки (eager loading) ингредиентов, что полностью исключает проблему N+1 запросов.
- ✅ **Интеграционное тестирование**: Покрытие основных сценариев (CRUD, сортировка, инкремент, обработка ошибок) с помощью `pytest` и `TestClient`.
- ✅ **Автодокументация**: Полная OpenAPI (Swagger/ReDoc) документация, доступная "из коробки".

---

## 🛠️ Стек технологий

- **Язык**: Python 3.10+
- **Фреймворк**: FastAPI + Uvicorn
- **База данных**: SQLAlchemy (Async Core/ORM) + SQLite (`aiosqlite`)
- **Валидация и сериализация**: Pydantic V1
- **Тестирование**: Pytest + HTTPX (`TestClient`)
- **Инструменты**: Git, GitHub, GitHub Actions, flake8, black, isort, mypy, venv

---

## 📂 Структура проекта

```text
fastapi-cookbook-ci/
├── database.py       # Настройка асинхронного движка и Dependency Injection для сессий
├── models.py         # ORM-Modelli SQLAlchemy (Recipe, Ingredient) с docstrings
├── schemas.py        # Pydantic-схемы для валидации и сериализации данных (с Field descriptions)
├── main.py           # Точки входа (endpoints) и управление жизненным циклом (lifespan)
├── test_main.py      # Интеграционные тесты API (5 тестовых сценариев)
├── requirements.txt  # Зависимости проекта с фиксацией версий
├── .gitignore        # Исключение БД (.db), кэша и venv из репозитория
└── README.md         # Документация проекта
```

---

## ⚙️ Установка и локальный запуск

1. **Клонируйте репозиторий** и перейдите в папку проекта:
   ```bash
   git clone https://github.com/Sarmagon/fastapi-cookbook-ci.git
   cd fastapi-cookbook-ci
   ```

2. **Создайте и активируйте виртуальное окружение**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите сервер разработки**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Откройте интерактивную документацию API** в браузере:
   👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Запуск тестов

Проект покрыт интеграционными тестами, проверяющими бизнес-логику и корректность работы с БД. Для их запуска выполните:

```bash
pytest test_main.py -v
```
*Ожидаемый результат: `5 passed`.*

---

## 📈 Roadmap (Планы по развитию)

Для приведения проекта к стандартам production-среды и соответствия требованиям современных Backend-вакансий планируется:

- [ ] **Миграция на PostgreSQL**: Замена `aiosqlite` на `asyncpg` и вынос конфигурации БД в `.env`.
- [ ] **Контейнеризация**: Написание `Dockerfile` и создание `docker-compose.yml` для поднятия приложения и БД одной командой.
- [x] **CI/CD**: Настроен GitHub Actions для автоматического прогона тестов и линтеров (flake8, black, isort, mypy) при каждом push.
- [ ] **Расширение API**: Добавление пагинации, фильтрации по ингредиентам и эндпоинтов `PUT`/`DELETE` для рецептов.

---

## 👤 Автор

**Станислав Смирнов**  
Junior Backend Developer / Python Developer  
📍 Москва, РФ

- 📧 **Email**: [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)
- ✈️ **Telegram**: [@Sarmagon](https://t.me/Sarmagon)
- 💻 **GitHub**: [github.com/Sarmagon/fastapi-cookbook-ci](https://github.com/Sarmagon/fastapi-cookbook-ci)