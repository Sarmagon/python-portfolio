# Станислав Смирнов

**Junior Python Backend Developer** · Москва

Актуальная текстовая версия — ниже. [Предыдущая версия PDF от 12.10.2026](stanislav-smirnov-python-backend.pdf).

[GitHub](https://github.com/Sarmagon) · [Telegram @Sarmagon](https://t.me/Sarmagon) · [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)

## Профессиональный профиль

Завершил программу Python-разработчика Skillbox, курсы Django, Python Advanced и архитектуры ПО. Разрабатываю учебные API и веб-приложения на FastAPI, Django и Flask: ORM, миграции, авторизация, фоновые задачи, тесты и CI. Перехожу в backend-разработку после многолетней работы в технической эксплуатации и управлении. Коммерческого опыта Python-разработки пока нет.

## Навыки

| Область | Практика в проектах |
|---|---|
| Язык и web | Python, FastAPI, Django, Flask, REST API, OpenAPI |
| Данные | PostgreSQL, SQLite, Django ORM, SQLAlchemy и Async SQLAlchemy, Peewee, Alembic |
| Фоновые задачи | Celery, Redis, Celery Beat, Flower; отдельная очередь PaymentJob в Django |
| Интеграции и доступ | Telegram Bot API, HTTP API, SMTP; JWT, Django auth/groups, API-ключи |
| Проверки | pytest, unittest, Ruff; flake8, black, isort, mypy в Cookbook; GitHub Actions |
| Запуск | Docker, Docker Compose, Nginx, Poetry, pip, Linux, SSH, Git |
| Мониторинг и медиа | Prometheus, Grafana, node-exporter, SeaweedFS; Sentry — подготовленная интеграция |
| Архитектура | ADR, NFR, анализ рисков, компромиссов и стоимости владения |

## Проекты

### Megano — интернет-магазин на Django

Итоговый проект курса «Python-фреймворк Django», Skillbox. Регистрация, профиль с аватаром, каталог, корзина, оформление и история заказов. Очередь учебной оплаты в базе данных с отдельным worker. Медиа в SeaweedFS с проверкой целостности при переносе; мониторинг Prometheus, Grafana и node-exporter. Подготовлена интеграция Sentry. В итоговой версии в Ubuntu прошли 66 тестов.

Python, Django 5.2, SQLite, Poetry, Docker Compose, SeaweedFS, Prometheus, Grafana. Предоставленный учебный frontend; платёжный сервис учебный.

[Исходный код на GitLab](https://gitlab.skillbox.ru/stanislav_smirnov_2/python_django_diploma/-/tree/master)

### Twitter Clone Backend

Итоговый проект курса Python Advanced, Skillbox. REST API публикаций, ленты, лайков, подписок и профилей. Проверки прав владельца, валидация изображений, транзакции, миграции и CI с API-тестами и Ruff. Предоставленный интерфейс Vue.

Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Docker Compose, Nginx.

[Исходный код](https://github.com/Sarmagon/twitter-clone-backend)

### Habit Tracker — Telegram-бот и API

Учебный проект. Привычки, ежедневные отметки, история и напоминания с часовыми поясами. JWT, проверка доступа владельца, зашифрованное хранение токенов в боте, миграции и автоматические проверки.

Python, FastAPI, pyTelegramBotAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Poetry, Docker Compose.

[Исходный код](https://github.com/Sarmagon/habit-tracker-telegram-fastapi)

**Django CRM:** услуги, кампании, лиды, договоры, клиенты; роли и статистика рекламы. Django, PostgreSQL, Docker Compose. [Код](https://github.com/Sarmagon/django-crm).

**SportTogether:** итоговый проект курса «Архитектор программного обеспечения», Skillbox. Требования, ADR, NFR, диаграммы, риски, компромиссы и стоимость владения. [Материалы](https://github.com/Sarmagon/sport-together-architecture).

**Image Processing:** сервис обработки изображений на Flask, Celery и Redis. [Код](../image-processing-service/).

[Все проекты и сертификаты](../README.md)

## Опыт работы

**ГУП Московский метрополитен, Москва**

**Заместитель начальника комплекса по технологии и качеству** · июнь 2022 — настоящее время

Техническое руководство комплексом с численностью более 200 сотрудников. Технологическая и нормативная документация, контроль качества, координация подрядчиков и технических работ. Эти обязанности относятся к транспортной отрасли, а не к разработке ПО.

**Технические и руководящие должности** · ноябрь 2007 — июнь 2022

Начальник участка, инженер-технолог, старший электромеханик и другие должности. Эксплуатация, организация работ, наставничество, строительство и ввод оборудования в эксплуатацию.

Награда: «Почётный работник транспорта города Москвы», 2023 год.

## Образование

- РУТ МИИТ, строительство железных дорог, путь и путевое хозяйство — высшее образование, 2009–2014.
- МГТУ им. Н. Э. Баумана, программное обеспечение вычислительной техники и автоматизированных систем — 2020–2021, обучение на первом курсе; неоконченное высшее образование.
- Skillbox — «Профессия Python-разработчик. Тариф Индивидуальный Плюс (совместно с GeekBrains)», 615 академических часов, завершено 12.10.2026.
- Skillbox — Python-фреймворк Django, завершено 12.10.2026; Python Advanced, 24.09.2026; Архитектор программного обеспечения, 22.09.2026.
- [Все сертификаты](https://github.com/Sarmagon/python-portfolio/tree/main/certificates), включая основы Python и GeekBrains.

## Дополнительная информация

Английский — A1. Интересуют REST API, интеграции, автоматизация и backend-системы. Направление развития — production-развёртывание и наблюдаемость.

Обновлено 12 октября 2026 года.

Обновлено 13 октября 2026 года.
