# 🐍 Python Portfolio — Станислав Смирнов

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-enabled-orange.svg)](https://github.com/Sarmagon/fastapi-cookbook-ci)

Портфолио проектов, разработанных в ходе обучения по направлению **Python Backend Development**.

Проекты демонстрируют практическую работу с REST API, базами данных, ORM, асинхронностью, фоновыми задачами, тестированием, контейнеризацией, внешними API и автоматизированными проверками кода.

---

## 🏆 Ключевые проекты

### 1. 🍳 Cookbook API с CI-пайплайном

**📁 Папка:** `module_30_cookbook_ci`  
Также доступен как отдельный репозиторий: [fastapi-cookbook-ci](https://github.com/Sarmagon/fastapi-cookbook-ci)

Асинхронное REST API для управления кулинарной книгой на FastAPI.

**🚀 Ключевые особенности:**

- ✅ Асинхронная работа с БД через SQLAlchemy
- ✅ Dependency Injection для управления сессиями
- ✅ `selectinload` для предотвращения N+1 запросов
- ✅ Интеграционные тесты с pytest и TestClient
- ✅ GitHub Actions: pytest, flake8, black, isort, mypy

**Стек:** FastAPI, SQLAlchemy Async, Pydantic, pytest, GitHub Actions

---

### 2. 🚗 REST API сервиса парковок

**📁 Папка:** `module_29_parking_api`

REST API для системы автоматической парковки с бизнес-логикой регистрации клиентов, заезда, выезда и проверки доступности парковочных мест.

**🚀 Ключевые особенности:**

- ✅ Application Factory для инициализации Flask-приложения
- ✅ SQLAlchemy ORM
- ✅ Alembic для миграций БД
- ✅ Интеграционные тесты на pytest
- ✅ Factory Boy и Faker для генерации тестовых данных

**Стек:** Flask, SQLAlchemy, PostgreSQL, Alembic, pytest, Factory Boy, Faker, Docker

---

### 3. 🤖 Telegram-бот для поиска рецептов

**📁 Папка:** `module_telegram_bot`

Итоговый проект курса **«Основы Python»**.

Telegram-бот для поиска рецептов через TheMealDB API с поддержкой русского и английского языков и сохранением истории запросов.

**🚀 Ключевые особенности:**

- ✅ Разделение проекта на handlers, keyboards, api, database и config_data
- ✅ FSM для управления состояниями пользователя
- ✅ Поиск рецептов по названию и ингредиентам
- ✅ Поддержка RU/EN
- ✅ Peewee ORM + SQLite для хранения истории запросов
- ✅ Интеграция с внешним REST API

**Стек:** Python, pyTelegramBotAPI, Peewee ORM, SQLite, Requests, TheMealDB API

---

### 4. 🖼️ Сервис обработки изображений с Celery

**📁 Папка:** `module_22_celery`

Сервис для асинхронной обработки изображений и выполнения фоновых задач.

**🚀 Ключевые особенности:**

- ✅ Celery + Redis для выполнения фоновых задач
- ✅ Celery Beat для периодических задач
- ✅ Flower для мониторинга очередей и воркеров
- ✅ Обработка изображений через Pillow
- ✅ Отправка результатов по email
- ✅ Создание ZIP-архивов с обработанными файлами

**Стек:** Flask, Celery, Redis, Flower, Pillow, SMTP, SQLAlchemy

---

## 🛠️ Технологический стек

| Категория | Технологии |
|---|---|
| **Язык** | Python 3.10+ |
| **Web Frameworks** | FastAPI, Flask, Flask-RESTful |
| **Базы данных** | PostgreSQL, SQLite |
| **ORM** | SQLAlchemy, Peewee ORM |
| **Миграции** | Alembic |
| **Фоновые задачи** | Celery, Redis, Flower |
| **Контейнеризация** | Docker, Docker Compose |
| **Тестирование** | pytest, Factory Boy, Faker, unittest |
| **Code Quality** | flake8, black, isort, mypy |
| **Автоматизация** | GitHub Actions |
| **API** | REST API, Telegram Bot API, внешние API |
| **Инструменты** | Git, GitHub, Linux, SSH |

---

## 📂 Структура репозитория

```text
python-portfolio/
├── certificates/                 # 🎓 Сертификаты об обучении
├── module_30_cookbook_ci/        # 🍳 FastAPI Cookbook API + GitHub Actions
├── module_29_parking_api/        # 🚗 Parking REST API
├── module_22_celery/             # 🖼️ Celery Image Processing Service
├── module_telegram_bot/          # 🤖 Telegram Recipe Bot
├── .gitignore
└── README.md
```

---

## 📈 Достижения

- ✅ Реализовано **20+ учебных и практических проектов** в ходе обучения
- ✅ Разработаны REST API на Flask и FastAPI
- ✅ Реализована работа с PostgreSQL и SQLite через ORM
- ✅ Настроены интеграционные тесты на pytest
- ✅ Использованы фоновые задачи Celery + Redis
- ✅ Настроены автоматические проверки кода через GitHub Actions
- ✅ Реализованы Telegram-боты и интеграции с внешними API

---

## 🎓 Сертификаты

| Курс | Сертификат | Дата |
|---|---|---:|
| **Skillbox — Основы Python. Часть 1** | [№ SKB0469958](certificates/skillbox-python-part-1.png) | 10.02.2026 |
| **Skillbox — Основы Python. Часть 2** | [№ SKB0487169](certificates/skillbox-python-part-2.png) | 02.05.2026 |

Нажатие на номер сертификата открывает его изображение в GitHub.

---

## 👨‍💻 Об авторе

**Станислав Смирнов**  
📍 Москва, РФ  
💻 Python Backend Developer / Junior Backend Developer  
🎓 Продолжаю обучение по направлениям Python Advanced и Django  
🛠️ 18+ лет опыта в технической сфере, включая руководящую работу  
🏆 «Почётный работник транспорта города Москвы» (2023)

Параллельно с основной профессиональной деятельностью развиваюсь в направлении **Backend-разработки на Python**.

В ходе обучения и практики работаю с REST API, базами данных, ORM, тестированием, фоновыми задачами, Docker, GitHub Actions и Telegram Bot API.

Ищу позицию **стажёра или Junior Python Backend Developer** с возможностью совмещения и дальнейшего профессионального развития в IT.

### 📞 Контакты

- 📧 **Email:** [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)
- ✈️ **Telegram:** [@Sarmagon](https://t.me/Sarmagon)
- 💼 **GitHub:** [github.com/Sarmagon](https://github.com/Sarmagon)

---

## 🚀 В развитии

- [x] REST API на Flask
- [x] REST API на FastAPI
- [x] ORM и миграции БД
- [x] Интеграционные тесты
- [x] Celery + Redis
- [x] Docker
- [x] GitHub Actions
- [x] Telegram Bot API
- [ ] Django
- [ ] PostgreSQL в асинхронных FastAPI-проектах
- [ ] Автоматическое развёртывание приложений
- [ ] Микросервисная архитектура
- [ ] RabbitMQ

---

*Проекты созданы в рамках обучения и самостоятельной практики и демонстрируют применяемые мной технологии и подходы к Backend-разработке.*

*Last updated: September 2026*
