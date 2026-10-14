# Python Backend Portfolio

Станислав Смирнов · Москва · **Junior Python Backend Developer**.

Завершил программу Python-разработчика (615 академических часов), курсы Django, Python Advanced и архитектуры ПО. Создаю учебные backend-проекты с API, базами данных, фоновыми задачами и тестами. Ищу первую роль в Python backend.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

[Резюме](resume/README.md) · [Сертификаты](certificates/)

## Основные проекты

### Лавка — интернет-магазин на Django

Итоговый проект курса «Python-фреймворк Django», Skillbox.

[Исходный код на GitHub](https://github.com/Sarmagon/lavka-django) · [CI](https://github.com/Sarmagon/lavka-django/actions/workflows/ci.yml) · развитие итогового проекта Megano.

Регистрация, профиль с аватаром, каталог, предложения продавцов, отзывы, корзина, оформление заказа, доставка и история заказов. Серверный расчёт суммы, резервирование остатков и идемпотентное оформление. Учебная оплата обрабатывается через очередь PaymentJob в базе данных и отдельный worker с повторными попытками.

Медиа переведены в S3-совместимое хранилище SeaweedFS; перенос проверяет целостность файлов. Prometheus, Grafana и node-exporter показывают состояние сайта, базы данных, очереди и worker. В версии «Лавка» прошли 72 теста; Django check и проверка изменений моделей — без ошибок. В браузере проверены регистрация при оформлении, заказ и учебная оплата отдельным worker.

**Стек:** Python, Django 5.2, SQLite, Poetry, Pillow, django-storages, Docker Compose, SeaweedFS, Prometheus, Grafana, node-exporter. Интеграция Sentry подготовлена; отправка событий во внешний сервис не проверена. Публичное развёртывание не проверено. Собственный адаптивный интерфейс: Django-шаблоны, CSS и JavaScript, созданные с помощью Codex; предоставленный frontend исключён. Каталог содержит 12 вымышленных товаров и сгенерированные изображения. Платёжный сервис учебный.


### Twitter Clone Backend

[Исходный код](https://github.com/Sarmagon/twitter-clone-backend) · [CI](https://github.com/Sarmagon/twitter-clone-backend/actions/workflows/ci.yml)

Итоговый проект Python Advanced: REST API микроблогов, API-ключи, твиты, лента, лайки, подписки и загрузка изображений. FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker Compose, Nginx. 40 тестов, покрытие 78%, Ruff. Интерфейс основан на предоставленном Vue-шаблоне; собственные изменения frontend сохранены в статистике языков.

### Habit Tracker — Telegram и FastAPI

[Исходный код](https://github.com/Sarmagon/habit-tracker-telegram-fastapi) · [CI](https://github.com/Sarmagon/habit-tracker-telegram-fastapi/actions/workflows/ci.yml)

Привычки, ежедневные отметки, история и напоминания с часовыми поясами IANA. Отдельные Telegram frontend и HTTP backend; JWT, Argon2id для service secret, шифрование токенов бота, идемпотентные отметки. PostgreSQL, SQLAlchemy, Alembic, Poetry, Docker Compose. Проверены 47 тестов и отдельный тест PostgreSQL, Ruff и миграции. Учебный проект; публичное production-развёртывание не заявляется.

### Django CRM

[Исходный код](https://github.com/Sarmagon/django-crm)

Услуги, рекламные кампании, лиды, договоры, активные клиенты и статистика. Авторизация и роли оператора, маркетолога и менеджера, перевод лида в клиента. Django ORM, PostgreSQL, Docker Compose. Проверены 3 теста, системная проверка Django и миграции. Выход выполняется POST с CSRF. CI проверяет существующие тесты на PostgreSQL, системную проверку и миграции. Pylint имеет замечания и проверяется отдельно. Локальное учебное приложение.

### SportTogether Architecture

[Архитектурные материалы](https://github.com/Sarmagon/sport-together-architecture)

Завершённый проект курса «Архитектор программного обеспечения»: требования, стейкхолдеры, ADR, NFR, архитектурные диаграммы, сценарии, риски, компромиссы, стоимость владения и презентация. Это проектирование системы; работающий backend SportTogether не заявляется.

## Дополнительные проекты

| Проект | Что демонстрирует |
|---|---|
| [Cookbook API](cookbook-api/) | Async FastAPI, SQLAlchemy, Pydantic, SQLite; 7 тестов и CI с проверками стиля и типов |
| [Image Processing Service](image-processing-service/) | Flask, Celery, Redis, Pillow, ZIP, SMTP; 10 тестов с подменой SMTP; CI, проверка ошибок обработки и отправки |
| [Django Deployment Lab](https://github.com/Sarmagon/skillbox-django-deploy) | Poetry, Docker Compose, Linux VM/SSH; 10 тестов. Runserver и DEBUG=1 — учебные ограничения |
| [Parking API](parking-api/) | Flask, SQLAlchemy, парковочные сессии; 9 тестов и CI |
| [Recipe Telegram Bot](recipe-telegram-bot/) | Telegram Bot API, Peewee и работа с рецептами |
| [File Sync Service](file-sync-service/) | Синхронизация файлов через API Яндекс Диска, конфигурация, журналирование |

## Технологии

| Область | Практика в проектах |
|---|---|
| Язык и web | Python, FastAPI, Django, Flask, REST API, OpenAPI |
| Данные | PostgreSQL, SQLite, Django ORM, SQLAlchemy и Async SQLAlchemy, Peewee, Alembic |
| Фоновые задачи | Celery, Redis, Celery Beat, Flower; отдельная очередь PaymentJob в Django |
| Интеграции и доступ | Telegram Bot API, HTTP API, SMTP; JWT, Django auth/groups, API-ключи |
| Проверки | pytest, unittest, Ruff; flake8, black, isort, mypy в Cookbook; GitHub Actions |
| Запуск | Docker, Docker Compose, Nginx, Poetry, pip, Linux, SSH, Git |
| Мониторинг и хранение медиа | Prometheus, Grafana, node-exporter, django-storages, S3-совместимое SeaweedFS; Sentry — подготовленная интеграция |
| Архитектура | ADR, NFR, анализ рисков, компромиссов и стоимости владения |

Технологии указаны по конкретным проектам. Prometheus, Grafana, node-exporter и SeaweedFS реализованы в Лавке. Интеграция Sentry подготовлена. Дальнейшее развитие: публичное развёртывание, проверка внешних интеграций и надёжность фоновых задач.

## Образование и сертификаты

| Программа или курс | Дата | Подтверждение |
|---|---|---|
| Профессия Python-разработчик — Индивидуальный Плюс, совместно с GeekBrains (615 академических часов) | 12.10.2026 | [№ SKB0508141](certificates/skillbox-python-profession.png) |
| Python-фреймворк Django | 12.10.2026 | [№ SKB0508141](certificates/skillbox-django.png) |
| Python Advanced | 24.09.2026 | [№ SKB0506025](certificates/skillbox-python-advanced.png) |
| Архитектор программного обеспечения | 22.09.2026 | [№ SKB0505176](certificates/skillbox-software-architect.png) |
| GeekBrains / Skillbox Holding — Python-разработчик | 17.06.2026 | [№ 2835512](certificates/geekbrains-python-developer.pdf) |
| Основы Python — часть 2 | 02.05.2026 | [№ SKB0487169](certificates/skillbox-python-part-2.png) |
| Основы Python — часть 1 | 10.02.2026 | [№ SKB0469958](certificates/skillbox-python-part-1.png) |

## Проверки

[![Cookbook CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/cookbook-ci.yml)
[![Image Processing CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/image-service-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/image-service-ci.yml)

[![Parking CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/parking-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/parking-ci.yml)

Каждый CI относится только к соответствующему проекту. Проекты являются учебными и практическими; публичные production-сервисы и коммерческий опыт не заявляются. Image Processing проверяется с подменой SMTP и отдельным Redis; CI не подтверждает доставку в реальный почтовый ящик.

## Структура и хранение

В этом репозитории: `certificates/`, `resume/`, `cookbook-api/`, `image-processing-service/`, `parking-api/`, `recipe-telegram-bot/`, `file-sync-service/`. Самостоятельные проекты доступны по ссылкам выше.

## Контакты

[GitHub](https://github.com/Sarmagon) · [Telegram @Sarmagon](https://t.me/Sarmagon) · [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)

Обновлено 14 октября 2026 года.
