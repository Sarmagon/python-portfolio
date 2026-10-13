# Cookbook API

[![Cookbook CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml)

Учебный асинхронный API рецептов: создание с ингредиентами, список по популярности и времени приготовления, просмотр рецепта со счётчиком. Дополнительный проект Python backend.

**Стек:** Python 3.10+, FastAPI, Pydantic 2, SQLAlchemy 1.4 Async, SQLite/aiosqlite, Uvicorn. API → Pydantic → AsyncSession → SQLite; связанные ингредиенты загружаются через `selectinload`.

## Запуск

```sh
git clone https://github.com/Sarmagon/python-portfolio.git
cd python-portfolio/cookbook-api
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

[Swagger](http://127.0.0.1:8000/docs). При первом запуске lifespan создаёт таблицы; при остановке освобождает engine. `DATABASE_URL` меняет подключение; по умолчанию `sqlite+aiosqlite:///./cookbook.db` в рабочем каталоге.

## API и пример

| Метод | Endpoint | Назначение |
|---|---|---|
| POST | `/recipes` | Создать рецепт, `201` |
| GET | `/recipes` | Список: просмотры по убыванию, время по возрастанию |
| GET | `/recipes/{id}` | Детали и увеличение просмотров; отсутствующий ID — `404` |

```sh
curl -X POST http://127.0.0.1:8000/recipes -H "Content-Type: application/json" -d '{"title":"Soup","cook_time":30,"ingredients":[{"name":"Water","amount":"1 l"}]}'
curl http://127.0.0.1:8000/recipes
curl http://127.0.0.1:8000/recipes/1
```

Название — 1–100 символов, время — положительное число; неверные данные дают `422`. В PowerShell для приведённых curl-команд используйте `curl.exe`.

## Проверки

```sh
python -m pip install -r requirements-dev.txt
python -m pytest test_main.py -q
python -m flake8 . --select=E9,F63,F7,F82
python -m black --check .
python -m isort --check-only .
python -m mypy . --ignore-missing-imports
```

Семь тестов: API, сортировка, просмотры, 404, новый пустой database и shutdown. Каждый тест использует временную SQLite и настоящий lifespan, без ручного создания таблиц и доступа к пользовательской базе.

CI проверяет этот каталог на Python 3.10 и 3.12 при его изменении. Блокирующий flake8 ограничен указанными кодами ошибок; полный отчёт стиля — информационный. Автоматического deployment нет.

## Статус и ограничения

Локальный учебный API без аутентификации, update/delete, миграций Alembic и production-развёртывания. SQLite и `create_all` подходят для демонстрации; изменение существующей схемы требует отдельной миграции. SQLAlchemy сохранён в ветке 1.4. Поддержка Pydantic переведена на v2, а FastAPI обновлён для фактической работы lifespan.

Исходное задание: [task.md](task.md). Основные файлы: `main.py`, `database.py`, `models.py`, `schemas.py`, `test_main.py`.
