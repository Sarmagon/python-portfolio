# 🐍 Python Portfolio — Станислав Смирнов

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-enabled-orange.svg)](https://github.com/Sarmagon/fastapi-cookbook-ci)

Коллекция **production-ready** проектов, разработанных в ходе обучения на курсе «Python-разработчик» (Skillbox). Каждый проект демонстрирует применение современных практик backend-разработки: асинхронность, тестирование, CI/CD, контейнеризация.

---

## 🏆 Ключевые проекты (Portfolio Highlights)

### 1. 🍳 Cookbook API с CI/CD пайплайном
**📁 Папка**: `module_30_cookbook_ci` *(Также доступен как отдельный репозиторий: [fastapi-cookbook-ci](https://github.com/Sarmagon/fastapi-cookbook-ci))*

Асинхронное REST API для управления кулинарной книгой с **полным циклом CI/CD**.

**🚀 Ключевые особенности**:
- ✅ **CI/CD**: GitHub Actions (pytest, flake8, black, isort, mypy)
- ✅ **Quality Gates**: код не попадает в main без прохождения всех проверок
- ✅ **Async SQLAlchemy**: управление сессиями через Dependency Injection
- ✅ **Оптимизация**: selectinload для предотвращения N+1 запросов
- ✅ **Тесты**: интеграционное тестирование с TestClient

**Стек**: FastAPI, SQLAlchemy (Async), Pydantic, pytest, GitHub Actions

---

### 2. 🚗 REST API сервиса парковок
**📁 Папка**: `module_29_parking_api`

REST API для системы автоматической парковки с бизнес-логикой заезда/выезда и оплатой.

**🚀 Ключевые особенности**:
- ✅ **Application Factory**: отложенная инициализация Flask-приложения
- ✅ **Alembic**: миграции БД с разрешением merge-конфликтов
- ✅ **Full testing**: pytest с фикстурами, параметризацией, Factory Boy
- ✅ **Business logic**: проверка доступности мест, оплата картой

**Стек**: Flask, SQLAlchemy, PostgreSQL, Alembic, pytest, Factory Boy, Faker

---

### 3. 🤖 Telegram-бот для поиска рецептов (Дипломный проект)
**📁 Папка**: `module_telegram_bot`

Telegram-бот для поиска рецептов через TheMealDB API с сохранением истории запросов.

**🚀 Ключевые особенности**:
- ✅ **Чистая архитектура**: handlers, keyboards, api, database, config_data
- ✅ **FSM**: управление состояниями пользователя
- ✅ **i18n**: поддержка двух языков (RU/EN)
- ✅ **ORM**: Peewee для работы с SQLite

**Стек**: pyTelegramBotAPI, Peewee ORM, SQLite, Requests

---

### 4. 🖼️ Сервис обработки изображений с Celery
**📁 Папка**: `module_22_celery`

REST API для загрузки и асинхронной обработки изображений с отправкой результатов на email.

**🚀 Ключевые особенности**:
- ✅ **Async tasks**: Celery + Redis для фоновой обработки
- ✅ **Scheduler**: Celery Beat для автоматической email-рассылки
- ✅ **Monitoring**: Flower для мониторинга задач
- ✅ **Automation**: создание ZIP-архивов с обработанными изображениями

**Стек**: Flask, Celery, Redis, Flower, Pillow, SMTP, SQLAlchemy

---

## 🛠️ Технологический стек

| Категория | Технологии |
|-----------|------------|
| **Язык** | Python 3.10+ (ООП, декораторы, генераторы, асинхронность) |
| **Web Frameworks** | FastAPI, Flask, Flask-RESTful |
| **Базы данных** | PostgreSQL, SQLite, SQLAlchemy (Core + ORM), Peewee ORM, Alembic |
| **Очереди задач** | Celery, Redis, Flower |
| **Контейнеризация** | Docker, Docker Compose |
| **Тестирование** | pytest (fixtures, parametrize, markers), Factory Boy, Faker, unittest |
| **Code Quality** | flake8, black, isort, mypy |
| **CI/CD** | GitHub Actions |
| **API** | REST API, Telegram Bot API, внешние API |
| **Инструменты** | Git, GitHub, Linux, SSH |

---

## 📂 Структура репозитория

```text
python-portfolio/
├── module_30_cookbook_ci/       # 🍳 Cookbook API with CI/CD (FastAPI + GitHub Actions)
├── module_29_parking_api/       # 🚗 Parking API (Flask + pytest + Alembic)
├── module_22_celery/            # 🖼️ Image Processing Service (Celery + Redis)
└── module_telegram_bot/         # 🤖 Recipe Bot (Telegram API + Peewee)
```

---

## 📈 Достижения и метрики

- ✅ **20+ проектов** реализовано в ходе обучения
- ✅ **CI/CD настроен** для Cookbook API (GitHub Actions)
- ✅ **Code Quality**: ключевые проекты проходят flake8, black, isort, mypy
- ✅ **Test Coverage**: проекты покрыты интеграционными тестами (pytest, Factory Boy)
- ✅ **Production-ready**: Application Factory, Dependency Injection, миграции БД

---

## 👨‍💻 Об авторе

**Станислав Смирнов**  
📍 Москва, РФ  
🎓 **Опыт**: 18 лет руководящей работы в технической сфере (ГУП «Московский метрополитен»)  
🏆 **Награда**: «Почётный работник транспорта города Москвы» (2023)

Параллельно с основной работой развиваюсь в направлении **Backend-разработки на Python**. Ищу позицию **стажёра или Junior-разработчика** с возможностью совмещения.

### 📞 Контакты
- 📧 **Email**: [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)
- ✈️ **Telegram**: [@Sarmagon](https://t.me/Sarmagon)
- 💼 **GitHub**: [github.com/Sarmagon](https://github.com/Sarmagon)

---

## 🚀 Планы по развитию

- [x] Настройка CI/CD (уже реализовано для Cookbook API через GitHub Actions)
- [ ] Миграция всех проектов на PostgreSQL
- [ ] Добавление интеграционных тестов во все REST API проекты
- [ ] Изучение Django и создание полноценного веб-приложения
- [ ] Работа с микросервисной архитектурой и message brokers (RabbitMQ)

---

*Все проекты созданы в учебных целях и демонстрируют применение современных практик backend-разработки.*  
*Last updated: July 2026*