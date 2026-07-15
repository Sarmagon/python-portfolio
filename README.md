```markdown
# 🐍 Python Portfolio

Коллекция учебных проектов, реализованных в ходе обучения на курсе «Python-разработчик» (Skillbox). Каждый проект демонстрирует применение конкретных технологий и подходов backend-разработки.

---

## 🛠️ Стек технологий

- **Язык**: Python 3 (ООП, асинхронность, многопоточность)
- **Веб-фреймворки**: Flask, Flask-RESTful, FastAPI
- **Базы данных**: PostgreSQL, SQLite, SQLAlchemy ORM, Peewee ORM
- **Очереди задач**: Celery, Redis, Flower
- **Контейнеризация**: Docker, Docker Compose
- **API**: REST API, Telegram Bot API, внешние API (TheMealDB, Star Wars API)
- **Тестирование**: pytest, unittest
- **Инструменты**: Git, GitHub, Linux, SSH

---

##  Проекты

### 1.  Cookbook API (FastAPI + async SQLAlchemy)
**Папка**: `module_26_cookbook_api`

Асинхронное REST API для управления кулинарной книгой с умной сортировкой и автосчетчиком просмотров.

**Особенности**:
- Dependency Injection для сессий БД (рекомендация FastAPI)
- Управление жизненным циклом через `lifespan`
- Оптимизация запросов через `selectinload` (предотвращение N+1)
- Интеграционные тесты (pytest + TestClient)

**Стек**: FastAPI, SQLAlchemy (Async), aiosqlite, Pydantic, pytest

---

### 2. 🤖 Telegram-бот для поиска рецептов (Дипломный проект)
**Папка**: `module_telegram_bot`

Telegram-бот для поиска рецептов через TheMealDB API с сохранением истории запросов.

**Особенности**:
- Чистая архитектура: handlers, keyboards, api, database, config_data
- FSM для управления состояниями пользователя
- Поддержка двух языков (RU/EN)
- ORM Peewee для работы с SQLite

**Стек**: Python, pyTelegramBotAPI, Peewee ORM, SQLite, Requests

---

### 3. 🖼️ Сервис обработки изображений с фоновыми задачами
**Папка**: `module_22_celery`

REST API для загрузки и асинхронной обработки изображений с отправкой результатов на email.

**Особенности**:
- Celery + Redis для фоновой обработки без блокировки
- Celery Beat для автоматической email-рассылки
- Flower для мониторинга выполнения задач
- Создание ZIP-архивов с обработанными изображениями

**Стек**: Flask, Celery, Redis, Flower, Pillow, SMTP, SQLAlchemy

---

### 4.  REST API библиотеки с ORM
**Папка**: `module_21_orm`

REST API для управления библиотекой с оптимизированными запросами к базе данных.

**Особенности**:
- Реляционная схема БД со связями и каскадами
- Сериализация через marshmallow
- Оптимизация через `joinedload` и массовую вставку
- Endpoints для книг, авторов и студентов

**Стек**: Flask, Flask-RESTful, marshmallow, SQLAlchemy, PostgreSQL

---

### 5.  Многопоточное приложение с приоритетными очередями
**Папка**: `module_12_multitasking`

Реализация задач многопоточного программирования с примитивами синхронизации.

**Особенности**:
- Задача об обедающих философах
- Система Producer-Consumer на базе PriorityQueue
- Параллельный парсер Star Wars API с замером производительности
- Система сортировки логов от 10 параллельных потоков

**Стек**: Python, threading, multiprocessing, Queue, Lock, Semaphore

---

### 6. 🐳 Деплой веб-приложения и контейнеризация
**Папка**: `module_09_docker`

Настройка SSH, создание Docker-образа и деплой Flask-приложения на удалённый сервер.

**Особенности**:
- SSH-подключение по RSA-ключам
- Оптимизированный Dockerfile с правильным порядком слоёв
- Загрузка образа на Docker Hub
- Мониторинг контейнера через docker exec и htop

**Стек**: Linux, SSH, Flask, Docker, Dockerfile

---

### 7. 🔄 File Sync Service
**Папка**: `file-sync-service`

Сервис для синхронизации файлов между директориями.

**Стек**: Python, файловые операции, логирование

---

##  Об авторе

**Станислав Смирнов**  
Junior Backend Developer / Python Developer  
📍 Москва, РФ

- 📧 **Email**: [stasus.sv@mail.ru](mailto:stasus.sv@mail.ru)
- ️ **Telegram**: [@Sarmagon](https://t.me/Sarmagon)
- 💼 **Опыт**: 18 лет руководящей работы в технической сфере (ГУП «Московский метрополитен»)

Параллельно с основной работой развиваюсь в направлении Backend-разработки на Python. Реализовал 20+ проектов: от алгоритмов и ООП до веб-приложений на Flask/FastAPI, работы с ORM, многопоточности, Celery, Docker и Telegram-ботов.

---

##  Планы по развитию

- [ ] Переход на PostgreSQL во всех проектах
- [ ] Настройка CI/CD (GitHub Actions / GitLab CI)
- [ ] Добавление интеграционных тестов во все проекты
- [ ] Изучение Django и создание полноценного веб-приложения
- [ ] Работа с микросервисной архитектурой

---

*Все проекты созданы в учебных целях и демонстрируют применение изученных технологий.* 