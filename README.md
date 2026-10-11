# 🐍 Python Portfolio — Станислав Смирнов

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green.svg)](https://fastapi.tiangolo.com/)
[![Django](https://img.shields.io/badge/Django-web-092E20.svg)](https://www.djangoproject.com/)
[![Flask](https://img.shields.io/badge/Flask-REST_API-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Cookbook CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml)

Портфолио учебных и практических проектов по направлению **Python Backend Development**.

Здесь собраны проекты, демонстрирующие работу с REST API, базами данных, ORM, асинхронным Python, фоновыми задачами, внешними API, Telegram-ботами, тестированием, CI и проектированием архитектуры программных систем.

---

## 🏆 Ключевые проекты

### 🤖 Habit Tracker — Telegram + FastAPI

🔗 [habit-tracker-telegram-fastapi](https://github.com/Sarmagon/habit-tracker-telegram-fastapi)

Трекер привычек с отдельным Telegram frontend и HTTP backend: создание и редактирование привычек, ежедневные отметки, история и напоминания с часовыми поясами IANA.

- JWT, проверка внутреннего service secret по Argon2id-хешу и зашифрованное хранилище токенов бота.
- PostgreSQL, SQLAlchemy, миграции Alembic, идемпотентные отметки и блокировки строк.
- Poetry, Docker Compose, pytest и GitHub Actions: Ruff, тесты, миграции и отдельные проверки PostgreSQL.

**Статус:** учебный проект для локального запуска; публичный production deployment не заявляется.
**Стек:** Python 3.12, FastAPI, pyTelegramBotAPI, PostgreSQL, SQLAlchemy, Alembic, SQLite, Poetry, Docker Compose, pytest, Ruff.

---

### 🐦 Twitter Clone Backend

🔗 [`twitter-clone-backend`](https://github.com/Sarmagon/twitter-clone-backend)

Учебный backend корпоративного сервиса микроблогов — итоговый проект Python Advanced.

**Ключевые особенности:**

- ✅ REST API на FastAPI и авторизация по API-ключу
- ✅ публикация и удаление твитов, лайки, подписки и лента
- ✅ загрузка изображений с проверкой содержимого и прав доступа
- ✅ PostgreSQL, SQLAlchemy и миграции Alembic
- ✅ запуск через Docker Compose, Nginx и готовый интерфейс Vue
- ✅ тесты API на pytest, проверки Ruff и Swagger / OpenAPI

**Стек:** Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Docker Compose, Nginx, pytest, Ruff

---

### 📊 Django CRM

🔗 [`django-crm`](https://github.com/Sarmagon/django-crm)

Веб-приложение для учёта услуг, рекламных кампаний, потенциальных и активных клиентов, а также контрактов.

**Ключевые особенности:**

- ✅ авторизация на стандартных средствах Django
- ✅ разделы услуг, рекламных кампаний, лидов, контрактов и активных клиентов
- ✅ перевод лида в активного клиента
- ✅ роли оператора, маркетолога и менеджера
- ✅ статистика рекламных кампаний и отношение дохода по контрактам к рекламному бюджету
- ✅ PostgreSQL и запуск через Docker Compose

**Стек:** Python, Django, PostgreSQL, Docker Compose

---

### 🍳 Cookbook API

📁 [`cookbook-api`](./cookbook-api/)

Асинхронный REST API для управления рецептами и ингредиентами на FastAPI.

**Ключевые особенности:**

- ✅ FastAPI REST API
- ✅ Async SQLAlchemy
- ✅ SQLite + aiosqlite
- ✅ Dependency Injection
- ✅ Pydantic validation
- ✅ связи между рецептами и ингредиентами
- ✅ `selectinload` для оптимизации ORM-запросов
- ✅ автоматический счётчик просмотров
- ✅ сортировка рецептов по популярности и времени приготовления
- ✅ Swagger / OpenAPI
- ✅ интеграционные тесты на pytest
- ✅ GitHub Actions CI
- ✅ flake8, black, isort, mypy

**Стек:** FastAPI, SQLAlchemy Async, SQLite, aiosqlite, Pydantic, pytest, GitHub Actions

---

### 🖼️ Image Processing Service

📁 [`image-processing-service`](./image-processing-service/)

Сервис асинхронной обработки изображений и выполнения фоновых задач.

**Ключевые особенности:**

- ✅ Celery + Redis
- ✅ асинхронная обработка изображений
- ✅ групповые фоновые задачи
- ✅ Celery Beat
- ✅ Flower для мониторинга
- ✅ обработка изображений через Pillow
- ✅ создание ZIP-архивов
- ✅ отправка результатов по email
- ✅ подписка и отписка пользователей
- ✅ тестирование API

**Стек:** Flask, Celery, Redis, Flower, Pillow, SQLAlchemy, SMTP

---

### 🏗️ SportTogether — архитектура программного обеспечения

🔗 [`sport-together-architecture`](https://github.com/Sarmagon/sport-together-architecture)

Архитектурный проект глобального спортивного приложения, выполненный в рамках финальной работы курса **«Архитектор программного обеспечения»**.

Проект охватывает полный цикл проектирования архитектурного решения: от анализа требований и стейкхолдеров до архитектурных решений, рисков, стоимости владения и подготовки материалов для защиты.

**Ключевые особенности:**

- ✅ бизнес-цели и функциональные требования
- ✅ анализ стейкхолдеров
- ✅ концептуальная архитектура
- ✅ критические бизнес-сценарии
- ✅ атрибуты качества
- ✅ нефункциональные требования
- ✅ Architecture Decision Records (ADR)
- ✅ сценарии использования
- ✅ архитектурные представления
- ✅ архитектурные диаграммы
- ✅ анализ рисков и компромиссов
- ✅ расчёт стоимости владения
- ✅ план поэтапной реализации
- ✅ презентация архитектурного решения

**Артефакты:** ADR, NFR, архитектурные диаграммы, сценарии использования, анализ рисков, расчёт стоимости владения, презентация

---

## Django diploma — на ревью

Интернет-магазин Megano: каталог, отзывы, профиль, корзина, оформление заказов, доставка, история и учебная оплата через очередь в БД. Python, Django 5.2, SQLite, Poetry, Pillow; предоставленный учебный frontend адаптирован к backend.

**Статус на 11.10.2026:** финальный этап отправлен на ревью, принятие диплома не подтверждено. Публичный репозиторий будет добавлен после завершения ревью и проверки возможности распространения учебных материалов. Это не интеграция с настоящим платёжным провайдером; Celery/Redis в очереди не используются.

---

## Дополнительные проекты

### 🚢 Django Deployment Lab

🔗 [skillbox-django-deploy](https://github.com/Sarmagon/skillbox-django-deploy)

Учебная упаковка Django-приложения для запуска в Docker Compose и переноса на Linux VM через SSH. Зависимости фиксируются Poetry; миграции и сбор статики выполняются при запуске.

**Стек:** Python 3.11, Django 4.2, Django REST Framework, SQLite, Poetry, Docker Compose.
**Ограничения:** `runserver`, `DEBUG=1`, отсутствие TLS и постоянного тома SQLite. Это deployment practice; production deployment и доступность публичного сервера не заявляются.

---

### 🚗 Parking API

📁 [`parking-api`](./parking-api/)

REST API на Flask для управления клиентами, парковками и парковочными сессиями.

**Ключевые особенности:**

- ✅ Application Factory
- ✅ Flask-SQLAlchemy
- ✅ SQLAlchemy ORM
- ✅ регистрация клиентов
- ✅ создание парковочных зон
- ✅ контроль свободных мест
- ✅ регистрация заезда и выезда
- ✅ проверка наличия банковской карты при выезде
- ✅ фиксация времени парковочной сессии
- ✅ интеграционные тесты на pytest
- ✅ Factory Boy и Faker
- ✅ изолированная SQLite-база для тестирования

**Стек:** Flask, Flask-SQLAlchemy, SQLAlchemy, SQLite, pytest, Factory Boy, Faker

---

### 🤖 Recipe Telegram Bot

📁 [`recipe-telegram-bot`](./recipe-telegram-bot/)

Итоговый проект курса **«Основы Python»**.

Telegram-бот для поиска рецептов через внешний API с поддержкой русского и английского языков и сохранением истории запросов.

**Ключевые особенности:**

- ✅ поиск рецептов по названию
- ✅ поиск по ингредиентам
- ✅ интеграция с TheMealDB API
- ✅ поддержка RU / EN
- ✅ FSM для управления состояниями пользователя
- ✅ inline- и reply-клавиатуры
- ✅ хранение истории запросов
- ✅ Peewee ORM
- ✅ SQLite
- ✅ модульная структура проекта

**Стек:** Python, pyTelegramBotAPI, Peewee ORM, SQLite, Requests, TheMealDB API

---

### 🔄 File Sync Service

📁 [`file-sync-service`](./file-sync-service/)

Сервис синхронизации локальной папки с Яндекс Диском через REST API.

**Ключевые особенности:**

- ✅ рекурсивный обход файлов и вложенных папок
- ✅ загрузка новых и обновление изменённых файлов
- ✅ удаление облачных файлов и папок, отсутствующих локально
- ✅ периодическая синхронизация с настраиваемым интервалом
- ✅ конфигурация через `.env`, логирование и обработка ошибок
- ✅ разделение приложения, бизнес-логики и инфраструктуры

**Стек:** Python, Requests, python-dotenv, Loguru, Яндекс Диск API

---

## 🛠️ Технологический стек

| Категория | Технологии |
|---|---|
| **Язык** | Python |
| **Web / API** | FastAPI, Flask, Django |
| **Базы данных** | SQLite, PostgreSQL |
| **ORM** | Django ORM, SQLAlchemy, Flask-SQLAlchemy, Peewee |
| **Асинхронность** | Async SQLAlchemy, aiosqlite |
| **Фоновые задачи** | Celery, Redis, Celery Beat |
| **Тестирование** | pytest, TestClient, Factory Boy, Faker |
| **Code Quality** | flake8, black, isort, mypy, Ruff |
| **CI** | GitHub Actions |
| **Telegram** | pyTelegramBotAPI |
| **Внешние API** | REST API, TheMealDB, Яндекс Диск API |
| **Миграции БД** | Django migrations, Alembic |
| **Контейнеризация** | Docker, Docker Compose, Nginx |
| **Архитектура** | ADR, NFR, архитектурные диаграммы, анализ рисков |
| **Аутентификация** | Django auth/groups, JWT, Argon2id (Habit Tracker) |
| **Зависимости** | Poetry, pip |
| **Инструменты** | Git, GitHub, Linux, SSH, VS Code |

---

## 📂 Структура репозитория

```text
python-portfolio/
├── .github/
│   └── workflows/
│       └── cookbook-ci.yml
│
├── certificates/
│   └── README.md
│
├── cookbook-api/
│   └── README.md
│
├── parking-api/
│   └── README.md
│
├── file-sync-service/
│   └── README.md
│
├── image-processing-service/
│   └── README.md
│
├── recipe-telegram-bot/
│   └── README.md
│
├── .gitignore
└── README.md
```

Каждый backend-проект содержит собственный README с описанием возможностей, архитектуры, структуры проекта и инструкциями по запуску.

Проекты **Habit Tracker** и **Django Deployment Lab** также расположены в отдельных репозиториях; ссылки приведены выше.

Проект **Twitter Clone Backend** расположен в отдельном репозитории:

[`github.com/Sarmagon/twitter-clone-backend`](https://github.com/Sarmagon/twitter-clone-backend)

Проект **Django CRM** расположен в отдельном репозитории:

[`github.com/Sarmagon/django-crm`](https://github.com/Sarmagon/django-crm)

Архитектурный проект **SportTogether** расположен в отдельном репозитории:

[`github.com/Sarmagon/sport-together-architecture`](https://github.com/Sarmagon/sport-together-architecture)

---

## ⚙️ Continuous Integration

Twitter Clone: [Backend checks](https://github.com/Sarmagon/twitter-clone-backend/actions/workflows/ci.yml) — pytest и Ruff.

Habit Tracker проверяется в собственном [workflow](https://github.com/Sarmagon/habit-tracker-telegram-fastapi/actions/workflows/ci.yml). CI каждого проекта относится только к его коду: badge Cookbook не подтверждает проверки остальных каталогов. Автоматический deployment здесь не настроен.


Для проекта **Cookbook API** настроен GitHub Actions workflow:

```text
.github/workflows/cookbook-ci.yml
```

При изменениях проекта `cookbook-api` или самого workflow автоматически выполняются:

- `pytest`
- `flake8`
- `black`
- `isort`
- `mypy`

CI запускается для:

```text
cookbook-api/**
.github/workflows/cookbook-ci.yml
```

Это позволяет автоматически проверять тесты, форматирование, импорты и типизацию кода.

---

## 🎓 Сертификаты

| Курс | Сертификат | Дата |
|---|---|---:|
| **Skillbox — Основы Python. Часть 1** | [№ SKB0469958](certificates/skillbox-python-part-1.png) | 10.02.2026 |
| **Skillbox — Основы Python. Часть 2** | [№ SKB0487169](certificates/skillbox-python-part-2.png) | 02.05.2026 |
| **GeekBrains / Skillbox Holding — Python-разработчик** | [№ 2835512](certificates/geekbrains-python-developer.pdf) | 17.06.2026 |
| **Skillbox — Архитектор программного обеспечения** | [№ SKB0505176](certificates/skillbox-software-architect.png) | 22.09.2026 |
| **Skillbox — Python Advanced** | [№ SKB0506025](certificates/skillbox-python-advanced.png) | 24.09.2026 |


Дополнительная информация находится в каталоге [`certificates`](./certificates/).

---

## 👨‍💻 Об авторе

**Станислав Смирнов**

📍 Москва, Россия

💻 Python Backend Developer / Junior Backend Developer

🎓 Продолжаю обучение Python и Django

Имею многолетний опыт работы в технической сфере, включая эксплуатацию информационных систем и руководящую работу.

Параллельно с основной профессиональной деятельностью развиваюсь в направлении **Backend-разработки на Python** и архитектуры программных систем.

В учебных и практических проектах работаю с:

- Python
- REST API
- FastAPI, Django и Flask
- SQLAlchemy и ORM
- асинхронным Python
- SQLite и PostgreSQL
- Docker и Docker Compose
- pytest
- Celery и Redis
- GitHub Actions
- Telegram Bot API
- внешними REST API
- Git и Linux
- проектированием архитектуры
- ADR и NFR
- анализом архитектурных рисков

Ищу возможность развиваться как **Junior Python Backend Developer** и применять полученные знания в реальных проектах.

---

## 📞 Контакты

- 📧 **Email:** [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)
- ✈️ **Telegram:** [@Sarmagon](https://t.me/Sarmagon)
- 💼 **GitHub:** [github.com/Sarmagon](https://github.com/Sarmagon)

---

## 🚀 В развитии

- [x] Python
- [x] REST API
- [x] Flask
- [x] FastAPI
- [x] SQLAlchemy ORM
- [x] Async SQLAlchemy
- [x] pytest
- [x] Celery + Redis
- [x] GitHub Actions
- [x] Telegram Bot API
- [x] основы проектирования архитектуры ПО
- [x] ADR и NFR
- [x] Django
- [x] PostgreSQL
- [x] Docker
- [ ] автоматическое развёртывание приложений
- [ ] микросервисная архитектура
- [ ] RabbitMQ

---

*Проекты созданы в рамках обучения и самостоятельной практики и демонстрируют практическое применение технологий Python Backend Development и проектирования программных систем.*

*Last updated: 11 October 2026*
