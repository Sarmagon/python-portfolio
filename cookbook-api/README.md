# 🍳 Cookbook API — асинхронный REST API на FastAPI

Асинхронный REST API для управления рецептами и ингредиентами.

Проект построен на **FastAPI**, **Async SQLAlchemy** и **Pydantic** и демонстрирует работу с асинхронной базой данных, Dependency Injection, валидацией данных, оптимизацией ORM-запросов и интеграционными тестами.

---

## 🚀 Возможности

- ✅ Создание рецептов с ингредиентами
- ✅ Получение списка рецептов
- ✅ Получение детальной информации о рецепте
- ✅ Асинхронная работа с базой данных
- ✅ Dependency Injection для сессий SQLAlchemy
- ✅ Валидация входных данных через Pydantic
- ✅ Автоматический счётчик просмотров рецепта
- ✅ Сортировка рецептов по популярности и времени приготовления
- ✅ `selectinload` для загрузки связанных ингредиентов
- ✅ Обработка ошибки `404`
- ✅ Swagger / OpenAPI документация
- ✅ Интеграционные тесты на pytest
- ✅ GitHub Actions CI

---

## 🛠️ Стек

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy Async
- SQLite
- aiosqlite
- Pydantic
- pytest
- TestClient / HTTPX
- GitHub Actions

Для автоматических проверок качества кода используются:

- flake8
- black
- isort
- mypy

---

## 🏗️ Архитектура

```text
Client
  │
  ▼
FastAPI
  │
  ├── Pydantic validation
  │
  ▼
Dependency Injection
  │
  ▼
AsyncSession
  │
  ▼
SQLAlchemy ORM
  │
  ▼
SQLite + aiosqlite
```

Для каждой операции с базой данных создаётся асинхронная сессия через:

```python
Depends(get_session)
```

Жизненный цикл приложения управляется через `lifespan`.

---

## 📡 API

| Метод | Endpoint | Назначение |
|---|---|---|
| `POST` | `/recipes` | Создать новый рецепт |
| `GET` | `/recipes` | Получить список рецептов |
| `GET` | `/recipes/{recipe_id}` | Получить рецепт по ID |

---

## ➕ Создание рецепта

### POST `/recipes`

Пример запроса:

```json
{
  "title": "Борщ",
  "cook_time": 120,
  "description": "Классический рецепт",
  "ingredients": [
    {
      "name": "Свёкла",
      "amount": "300 г"
    }
  ]
}
```

При создании рецепта:

- назначается ID;
- счётчик просмотров начинается с `0`;
- ингредиенты сохраняются вместе с рецептом.

---

## 📋 Список рецептов

### GET `/recipes`

Возвращает список рецептов.

Сортировка выполняется:

1. по количеству просмотров — по убыванию;
2. при одинаковом количестве просмотров — по времени приготовления по возрастанию.

То есть более популярные рецепты отображаются выше, а при одинаковой популярности выше будет рецепт с меньшим временем приготовления.

---

## 👁️ Детальная информация

### GET `/recipes/{recipe_id}`

Возвращает:

- ID;
- название;
- время приготовления;
- описание;
- количество просмотров;
- список ингредиентов.

При каждом успешном открытии рецепта:

```text
views += 1
```

Если рецепт не существует, API возвращает:

```text
404 Not Found
```

---

## ⚡ Асинхронная работа с БД

Для подключения используется:

```text
sqlite+aiosqlite
```

SQLAlchemy работает через:

```python
create_async_engine
AsyncSession
sessionmaker
```

Сессия внедряется в endpoint через Dependency Injection.

---

## 🔄 Lifecycle

При запуске приложения через `lifespan` создаются таблицы базы данных.

При завершении работы приложения освобождаются ресурсы SQLAlchemy engine.

---

## 🚀 Оптимизация ORM

При загрузке связанных ингредиентов используется:

```python
selectinload(Recipe.ingredients)
```

Это позволяет заранее загрузить связанные данные и избежать дополнительных запросов при обращении к ингредиентам рецептов.

---

## ✅ Валидация

Pydantic проверяет входные данные.

### `title`

- обязательное поле;
- длина от 1 до 100 символов.

### `cook_time`

- обязательное поле;
- значение должно быть не меньше 1.

Ингредиенты могут быть переданы списком либо отсутствовать.

---

## 🧪 Тестирование

Проект содержит интеграционные тесты на `pytest`.

Проверяются:

- создание рецепта с ингредиентами;
- создание рецепта без ингредиентов;
- получение списка рецептов;
- сортировка;
- увеличение счётчика просмотров;
- обработка отсутствующего рецепта.

Запуск:

```bash
pytest test_main.py -v
```

В текущем наборе реализовано **5 тестовых сценариев**.

---

## 📚 Swagger

После запуска приложения интерактивная документация доступна по адресу:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## ⚙️ Установка

### 1. Клонировать портфолио

```bash
git clone https://github.com/Sarmagon/python-portfolio.git
cd python-portfolio/cookbook-api
```

### 2. Создать виртуальное окружение

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

Для запуска инструментов проверки качества кода:

```bash
pip install -r requirements-dev.txt
```

### 4. Запустить API

```bash
uvicorn main:app --reload
```

---

## 📂 Структура проекта

```text
python-portfolio/
├── .github/
│   └── workflows/
│       └── cookbook-ci.yml
│
└── cookbook-api/
    ├── database.py
    ├── main.py
    ├── models.py
    ├── schemas.py
    ├── test_main.py
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── task.md
    ├── .gitignore
    └── README.md
```

### Назначение основных файлов

- `main.py` — FastAPI-приложение и endpoints
- `database.py` — async engine, сессии и Dependency Injection
- `models.py` — SQLAlchemy ORM-модели
- `schemas.py` — Pydantic-схемы
- `test_main.py` — интеграционные тесты
- `requirements.txt` — зависимости приложения
- `requirements-dev.txt` — инструменты разработки и проверки качества
- `task.md` — исходное учебное задание

---

## 🔍 GitHub Actions CI

В репозитории настроен GitHub Actions workflow:

```text
.github/workflows/cookbook-ci.yml
```

При каждом `push` и `pull request` в ветки `main` и `master` автоматически выполняются:

- `pytest`
- `flake8`
- `black`
- `isort`
- `mypy`

Workflow запускает команды из каталога:

```text
cookbook-api/
```

Это позволяет автоматически проверять тесты, стиль кода, форматирование, порядок импортов и типизацию.

---

## 🎯 Что демонстрирует проект

Проект показывает практическую работу с:

- FastAPI;
- REST API;
- асинхронным Python;
- Async SQLAlchemy;
- ORM;
- Dependency Injection;
- Pydantic;
- связями между моделями;
- оптимизацией SQL-запросов;
- lifecycle приложения;
- HTTP status codes;
- OpenAPI;
- интеграционным тестированием;
- GitHub Actions;
- автоматическими проверками качества кода.

---

Проект выполнен в рамках обучения Python Backend Development и оформлен как демонстрационный backend-проект для портфолио.