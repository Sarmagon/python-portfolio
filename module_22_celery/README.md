# 🖼️ Image Processing Service — Celery + Redis

Сервис асинхронной обработки изображений на Flask.

Пользователь загружает одно или несколько изображений и указывает email. Изображения ставятся в очередь Celery, обрабатываются в фоне, объединяются в ZIP-архив и отправляются пользователю по электронной почте.

Дополнительно реализована подписка на еженедельную email-рассылку.

---

## 🚀 Возможности

- ✅ Асинхронная обработка изображений через Celery
- ✅ Redis как broker и result backend
- ✅ Параллельная обработка нескольких изображений через Celery Group
- ✅ Отслеживание прогресса выполнения задач
- ✅ Создание ZIP-архива с обработанными изображениями
- ✅ Отправка результата пользователю по email
- ✅ Подписка и отписка от рассылки
- ✅ Celery Beat для периодических задач
- ✅ Flower для мониторинга Celery
- ✅ SQLite + SQLAlchemy для хранения подписчиков
- ✅ Автоматический smoke-test основных API endpoint

---

## 🛠️ Стек

- Python
- Flask
- Celery
- Redis
- Celery Beat
- Flower
- SQLAlchemy
- SQLite
- Pillow
- SMTP
- Requests

---

## 🏗️ Как работает сервис

```text
Клиент
  │
  │ POST /blur
  ▼
Flask API
  │
  ├── сохраняет изображения
  │
  └── создаёт группу Celery-задач
              │
              ▼
         Redis Broker
              │
              ▼
        Celery Worker
              │
              ├── обработка изображений
              ├── создание ZIP
              └── отправка результата по email
```

Отдельно Celery Beat запускает периодическую задачу еженедельной рассылки активным подписчикам.

---

## 📡 API

| Метод | Endpoint | Назначение |
|---|---|---|
| `POST` | `/blur` | Загружает изображения и ставит их в очередь на обработку |
| `GET` | `/status/<group_id>` | Возвращает статус и прогресс группы задач |
| `POST` | `/subscribe` | Подписывает email на рассылку |
| `POST` | `/unsubscribe` | Отключает подписку |

---

## 📤 POST /blur

Принимает:

- `email` — email пользователя
- `images` — одно или несколько изображений

Пример:

```bash
curl -X POST http://127.0.0.1:5000/blur \
  -F "email=test@example.com" \
  -F "images=@test1.jpg" \
  -F "images=@test2.jpg"
```

Пример ответа:

```json
{
  "group_id": "task-group-id",
  "total_images": 2,
  "message": "Задачи поставлены в очередь"
}
```

---

## 📊 GET /status/<group_id>

Позволяет проверить состояние обработки изображений.

```bash
curl http://127.0.0.1:5000/status/<group_id>
```

Пример ответа:

```json
{
  "group_id": "task-group-id",
  "status": "processing",
  "progress": {
    "completed": 1,
    "total": 2
  }
}
```

После завершения всех задач статус изменяется на:

```text
completed
```

---

## ✉️ Подписка на рассылку

### Подписаться

```bash
curl -X POST http://127.0.0.1:5000/subscribe \
  -F "email=test@example.com"
```

### Отписаться

```bash
curl -X POST http://127.0.0.1:5000/unsubscribe \
  -F "email=test@example.com"
```

Активные подписчики хранятся в SQLite.

Celery Beat запускает еженедельную рассылку:

```text
Понедельник — 09:00
```

---

## ⚙️ Установка

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

### 2. Настроить SMTP

Создайте `.env`:

```env
SMTP_USER=your_email@yandex.ru
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=587
```

Не добавляйте `.env` с реальными учётными данными в Git.

---

## ▶️ Запуск

Для полной работы сервиса необходимо запустить несколько процессов.

### Redis

```bash
redis-server
```

### Celery Worker

```bash
celery -A celery_app worker --loglevel=info --pool=solo
```

### Celery Beat

```bash
celery -A celery_app beat --loglevel=info
```

### Flower

```bash
celery -A celery_app flower --port=5555
```

### Flask API

```bash
python app.py
```

После запуска API доступен по адресу:

```text
http://127.0.0.1:5000
```

Flower:

```text
http://127.0.0.1:5555
```

---

## 🧪 Проверка API

В проект добавлен smoke-test основных endpoint:

```bash
python test_api.py
```

Он проверяет:

- `POST /blur`
- `GET /status/<group_id>`
- `POST /subscribe`
- `POST /unsubscribe`

При успешном выполнении:

```text
✅ POST /blur — OK
✅ GET /status — completed
✅ POST /subscribe — OK
✅ POST /unsubscribe — OK

🎉 Все тесты пройдены!
```

---

## 📂 Структура проекта

```text
module_22_celery/
├── app.py             # Flask API
├── celery_app.py      # конфигурация Celery и Celery Beat
├── tasks.py           # фоновые Celery-задачи
├── image.py           # обработка изображений
├── mail.py            # отправка email
├── subscribers.py     # модель и работа с подписчиками
├── config.py          # конфигурация
├── test_api.py        # smoke-test API
├── test1.jpg          # тестовое изображение
├── test2.jpg          # тестовое изображение
└── requirements.txt   # зависимости
```

---

## 🎯 Что демонстрирует проект

Проект показывает практическую работу с:

- очередями фоновых задач;
- асинхронной обработкой длительных операций;
- message broker;
- периодическими задачами;
- мониторингом Celery;
- REST API;
- ORM и базой данных;
- интеграцией с SMTP;
- обработкой файлов.

---

Проект выполнен в рамках обучения Python-разработке и доработан как демонстрационный backend-проект для портфолио.
