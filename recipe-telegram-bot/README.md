# Recipe Telegram Bot

Итоговый проект курса «Основы Python»: Telegram-бот ищет рецепты через TheMealDB API и сохраняет историю запросов в SQLite.

## Возможности

- Поиск по названию блюда или ингредиенту.
- Русский и английский ввод; русские названия сопоставляются с английскими через встроенные словари, а не универсальный переводчик.
- История запросов, просмотр рецепта, inline/reply-клавиатуры.
- Состояния диалога FSM и обработка ошибок внешнего API.

**Стек:** Python 3.10+, pyTelegramBotAPI, Requests, Peewee ORM, SQLite, python-dotenv.

## Запуск

Из каталога python-portfolio:

```sh
cd recipe-telegram-bot
python -m venv .venv
```

В PowerShell: `.\.venv\Scripts\Activate.ps1`. В Linux/macOS: `source .venv/bin/activate`.

```sh
pip install -r requirements.txt
cp .env.template .env
```

Для PowerShell вместо cp: `Copy-Item .env.template .env`. Получите токен своего бота у [BotFather](https://t.me/BotFather), запишите его в BOT_TOKEN и запустите:

```sh
python main.py
```

При старте создаются таблицы, регистрируются команды и запускается polling. Реальный токен и SQLite с историей пользователей не публикуются.

## Структура

- api/ — запросы TheMealDB и словари названий.
- handlers/ — команды, поиск и callback-обработчики.
- database/ — модели пользователей и истории.
- keyboards/, utils/ — клавиатуры, состояния и команды.
- config_data/, loader.py, main.py — настройки, инициализация и запуск.

## Статус и ограничения

Учебный проект с внешними Telegram и TheMealDB API. Поддержка русских названий ограничена содержимым словарей. Отдельные автоматические тесты и CI для этого проекта не настроены; успешный CI Cookbook или Image Processing их не заменяет. Доступность внешних API и live-сценарии при этой редактуре не проверялись.

[Портфолио](../README.md)
