# Image Processing Service

[![Image Processing CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/image-service-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/image-service-ci.yml)

Учебный HTTP-сервис: загрузка изображений, размытие в фоне, ZIP-архив и отправка по SMTP. Дополнительно — подписка и еженедельная рассылка.

**Стек:** Python 3.12, Flask, Celery, Redis broker/result backend, Pillow, SQLite + SQLAlchemy, Celery Beat, Flower, SMTP.

## Архитектура

```text
POST /blur → проверка/сохранение изображений → Celery chord
  → параллельные blur_task → process_order → полный ZIP → SMTP
GET /status/<group_id> → результаты обработки и итоговой задачи
Celery Beat → send_weekly_newsletter → активные подписчики SQLite
```

ZIP и письмо создаются callback-задачей после успешной обработки всех файлов. Ошибка изображения или SMTP даёт `failed`; готовность отдельного изображения не означает завершение заказа.

## Запуск локально

Запускайте worker в Linux/WSL: Celery не поддерживает обычный Windows worker. Нужны Redis и SMTP-аккаунт, настроенный для отправки. API и worker должны видеть одни и те же файлы.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Заполните SMTP-параметры; не публикуйте .env.
docker run --rm -p 127.0.0.1:6379:6379 redis:7-alpine
```

В отдельных терминалах с активированным окружением, из каталога проекта:

```sh
flask --app app run --host 127.0.0.1 --port 5000
celery -A celery_app.celery_app worker --loglevel=info
# Необязательно: рассылка и мониторинг
celery -A celery_app.celery_app beat --loglevel=info
celery -A celery_app.celery_app flower
```

`IMAGE_SERVICE_DATA_DIR` задаёт каталог `uploads`, `results`, `orders`; одинаковый абсолютный путь обязателен для API и worker. `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `SUBSCRIBERS_DATABASE_URL` и SMTP-параметры описаны в `.env.example`. По умолчанию Redis использует базы 0 и 1, подписчики — `subscribers.db`.

## API

| Метод | Endpoint | Назначение |
|---|---|---|
| POST | `/blur` | Multipart: `email`, 1–10 полей `images`; ответ `202`, `group_id` |
| GET | `/status/<group_id>` | `processing`, `finalizing`, `completed` или `failed`; прогресс успешных/ошибочных изображений |
| POST | `/subscribe` | JSON/form `email`, подписка |
| POST | `/unsubscribe` | JSON/form `email`, отписка |

```sh
curl -F "email=your-address@example.com" -F "images=@image.png" http://127.0.0.1:5000/blur
curl http://127.0.0.1:5000/status/UUID_ИЗ_ОТВЕТА
```

Лимит запроса — 20 MiB. PNG/JPEG/WEBP проверяются по реальному содержимому и пересохраняются как PNG со случайными именами. Имена клиента не используются как пути, одинаковые имена не перезаписывают друг друга. Некорректные файлы — `400`, превышение размера — `413`, неизвестный заказ — `404`, недоступная очередь/статус — `503`.

## Проверки

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

10 тестов проверяют полный workflow, ZIP с двумя одинаковыми исходными именами, ошибку SMTP, неполные результаты, ошибочный прогресс, входные данные и подписку. Celery выполняется в eager-режиме с memory backend, SMTP подменён; рабочая база не затрагивается. CI запускает эти тесты и три отдельных сценария с настоящим Redis и solo worker: успех, ошибка SMTP и ошибка изображения. Внешняя доставка письма не проверяется; SMTP во всех автоматических проверках подменён.

`test_api.py` — отдельный ручной smoke-сценарий; требует запущенных сервисов и может отправить настоящее письмо. Он не входит в автоматические тесты.

## Ограничения и безопасность

Локальный учебный сервис без аутентификации и подтверждения владения email. Не размещать открыто: нет rate limiting, политики удаления старых заказов и защиты рассылки от злоупотребления. API и worker требуют общего диска; очередь не является транзакционной с локальным manifest. `completed` означает успешное принятие письма SMTP-сервером, не доставку адресату. Повторное автоматическое письмо после неоднозначной ошибки SMTP не предусмотрено.

Файлы, subscriber DB и `.env` исключены из Git. Redis и Flower должны быть доступны только в доверенном окружении. Для production нужны контроль доступа, хранение заданий в БД, резервные копии, cleanup и проверка доставки.

Интеграционную проверку запускайте только с отдельным Redis, например на порту 16379, и без настоящих SMTP credentials:

```sh
IMAGE_TEST_REDIS_URL=redis://127.0.0.1:16379 python tests/redis_workflow_check.py
```
