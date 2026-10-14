# Parking API

[![Parking CI](https://github.com/Sarmagon/python-portfolio/actions/workflows/parking-ci.yml/badge.svg)](https://github.com/Sarmagon/python-portfolio/actions/workflows/parking-ci.yml)

Учебный REST API парковочных сессий на Flask. Клиенты, парковки, заезд и выезд автомобиля; проверка свободных мест и наличия учебного поля карты перед выездом.

## Возможности и стек

- Получение списка клиентов и клиента по ID, создание клиента и парковки.
- Регистрация заезда и выезда, проверка состояния парковки и повторного активного заезда.
- Изменение количества свободных мест при открытии и закрытии сессии.
- Application Factory, Flask-SQLAlchemy/SQLAlchemy, SQLite, pytest, Factory Boy и Faker.

## Проверка

Python 3.11 или 3.12. Из корня этого репозитория перейдите в parking-api:

```sh
cd parking-api
python -m venv .venv
```

В PowerShell: `.\.venv\Scripts\Activate.ps1`. В Linux/macOS: `source .venv/bin/activate`.

```sh
pip install -r requirements.txt
python -m pytest -q
```

Существуют девять API-тестов. Каждый тест использует отдельное Flask-приложение и SQLite в памяти; таблицы и вымышленные данные создаются фикстурами. Работа с реальными платёжными сервисами не выполняется.

[Примеры запросов и модели](docs/api.md)

## Структура

- app/__init__.py — фабрика приложения и подключение маршрутов.
- app/models.py — модели Client, Parking и ClientParking.
- app/routes.py — API и логика парковочных сессий.
- tests/ — фикстуры, фабрики и тесты API.
- config.py — тестовая конфигурация, requirements.txt — зависимости.
- [task.md](task.md) — исходная учебная задача.

## Статус и ограничения

Проект предназначен для демонстрации backend-логики и тестирования. По умолчанию фабрика использует TestingConfig и не создаёт таблицы автоматически: это делают тестовые фикстуры. Постоянная БД, миграции, авторизация, публичное развёртывание и реальная банковская оплата не настроены. В поле credit_card нельзя помещать настоящие карточные данные. Зависимости сохранены по учебному проекту; перед внешним размещением нужен отдельный аудит и обновление.

[Портфолио](../README.md)
