# Станислав Смирнов

**Junior Python Backend Developer** · Москва

[Скачать резюме PDF](stanislav-smirnov-python-backend.pdf)

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
| Архитектура | ADR, NFR, анализ рисков, компромиссов и стоимости владения |

## Проекты

### Habit Tracker — Telegram и FastAPI

[Исходный код](https://github.com/Sarmagon/habit-tracker-telegram-fastapi) · [CI](https://github.com/Sarmagon/habit-tracker-telegram-fastapi/actions/workflows/ci.yml)

Привычки, ежедневные отметки, история и напоминания с часовыми поясами IANA. Отдельные Telegram frontend и HTTP backend; JWT, Argon2id для service secret, шифрование токенов бота, идемпотентные отметки. PostgreSQL, SQLAlchemy, Alembic, Poetry, Docker Compose. Проверены 47 тестов и отдельный тест PostgreSQL, Ruff и миграции. Учебный проект; публичное production-развёртывание не заявляется.

### Twitter Clone Backend

[Исходный код](https://github.com/Sarmagon/twitter-clone-backend) · [CI](https://github.com/Sarmagon/twitter-clone-backend/actions/workflows/ci.yml)

Итоговый проект Python Advanced: REST API микроблогов, API-ключи, твиты, лента, лайки, подписки и загрузка изображений. FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker Compose, Nginx. 40 тестов, покрытие 78%, Ruff. Предоставленный готовый frontend отделён от собственного backend; собственный код не скрыт из статистики языков.

### Django Marketplace — Megano

Принятый итоговый проект Django. Каталог, предложения продавцов, отзывы, профиль, корзина, оформление заказа, доставка, история и учебная оплата. Серверный расчёт суммы, транзакционное резервирование остатков, ключ идемпотентности checkout, очередь PaymentJob в БД с повторными попытками и lease. Django 5.2, SQLite, Poetry, Pillow; 58 тестов прошли.

**Подтверждение:** преподаватель принял работу 12.10.2026, по предоставленному сообщению Skillbox; [курс завершён](https://github.com/Sarmagon/python-portfolio/blob/main/certificates/skillbox-django.png). Слияние GitLab MR#8 не подтверждено. Публичные исходники пока не опубликованы: требуется уточнить лицензию предоставленного frontend. Очередь не использует Celery/Redis, оплата работает через локальный mock-сервис без настоящих банковских данных.

### Django CRM

[Исходный код](https://github.com/Sarmagon/django-crm)

Услуги, рекламные кампании, лиды, договоры, активные клиенты и статистика. Авторизация и роли оператора, маркетолога и менеджера, перевод лида в клиента. Django ORM, PostgreSQL, Docker Compose. Проверены 3 теста, системная проверка Django и миграции. Выход выполняется POST с CSRF. Pylint имеет замечания; зелёный CI не заявляется. Локальное учебное приложение.

### SportTogether Architecture

[Архитектурные материалы](https://github.com/Sarmagon/sport-together-architecture)

Завершённый проект курса «Архитектор программного обеспечения»: требования, стейкхолдеры, ADR, NFR, архитектурные диаграммы, сценарии, риски, компромиссы, стоимость владения и презентация. Это проектирование системы; работающий backend SportTogether не заявляется.

Другие проекты: [Cookbook, обработка изображений, Deployment Lab, Parking API, Telegram-бот, File Sync](https://github.com/Sarmagon/python-portfolio#дополнительные-проекты).

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
