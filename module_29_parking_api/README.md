# 🚗 Parking API — REST API сервиса парковок

REST API для системы автоматической парковки с бизнес-логикой заезда/выезда, проверкой доступности мест и автоматической оплатой.

## 📋 Функционал

- **Регистрация клиентов** — создание профиля с привязкой карты и автомобиля.
- **Управление парковками** — создание парковочных зон с указанием количества мест.
- **Заезд на парковку** — автоматическая проверка доступности мест и фиксация времени въезда.
- **Выезд с парковки** — расчёт времени парковки, проверка наличия привязанной карты для оплаты, освобождение места.
- **API Endpoints** — получение списков клиентов, парковок и логов.

## 🛠️ Стек технологий

- **Backend:** Python 3, Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL (основная), SQLite (in-memory для тестов)
- **Testing:** pytest, Factory Boy, Faker
- **Migrations:** Alembic
- **Deployment:** Docker

## 📦 Установка и запуск

1. Клонировать репозиторий портфолио:
   ```bash
   git clone https://github.com/Sarmagon/python-portfolio.git
   cd python-portfolio/module_29_parking_api
   ```

2. Создать и активировать виртуальное окружение:
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для macOS/Linux:
   source venv/bin/activate
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустить приложение:
   ```bash
   python main.py
   ```

## 🧪 Тестирование

Запустить все тесты с подробным выводом:
```bash
pytest -v
```

Запустить тесты с проверкой покрытия кода:
```bash
pytest --cov=.
```

## 📡 API Endpoints

| Метод  | Endpoint             | Описание                                     |
|--------|----------------------|----------------------------------------------|
| GET    | `/clients`           | Список всех клиентов                         |
| GET    | `/clients/<id>`      | Информация о клиенте по ID                   |
| POST   | `/clients`           | Создать нового клиента                       |
| POST   | `/parkings`          | Создать новую парковку                       |
| POST   | `/client_parkings`   | Заезд на парковку                            |
| DELETE | `/client_parkings`   | Выезд с парковки (с проверкой оплаты)        |

## 📁 Структура проекта

```text
module_29_parking_api/
├── app/
│   ├── __init__.py          # Application Factory (отложенная инициализация)
│   ├── models.py            # ORM-модели (Client, Parking, ClientParking)
│   └── routes.py            # API endpoints и бизнес-логика
├── tests/
│   ├── conftest.py          # Фикстуры pytest (инициализация тестовой БД)
│   ├── factories.py         # Factory Boy фабрики для генерации данных
│   └── test_api.py          # Интеграционные тесты API
├── config.py                # Конфигурация приложения
├── requirements.txt         # Зависимости проекта
└── main.py                  # Точка входа в приложение
```

## 💡 Особенности реализации

- **Application Factory** — паттерн для отложенной инициализации Flask-приложения и расширений.
- **ORM SQLAlchemy** — декларативное описание моделей и связей.
- **Alembic** — управление миграциями схемы базы данных.
- **pytest fixtures** — полная изоляция тестов с использованием in-memory SQLite БД.
- **Factory Boy + Faker** — генерация реалистичных и уникальных тестовых данных.

## 👨‍💻 Автор

**Станислав Смирнов**  
GitHub: [github.com/Sarmagon](https://github.com/Sarmagon)  
Telegram: [@Sarmagon](https://t.me/Sarmagon)