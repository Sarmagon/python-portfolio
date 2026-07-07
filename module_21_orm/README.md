## Описание проекта
Flask-приложение с REST API для управления библиотекой. Использует SQLAlchemy ORM для работы с базой данных, marshmallow для сериализации и валидации данных.

## Технологии
- **Python 3**
- **Flask** + Flask-RESTful
- **SQLAlchemy ORM** (связи, каскады, жадная подгрузка)
- **marshmallow** (сериализация, валидация)
- **SQLite/PostgreSQL**

## Функционал
- CRUD операции для книг и авторов
- Выдача/возврат книг студентам
- Поиск должников (книги более 14 дней)
- Статистика по читателям
- Массовая вставка студентов из CSV

## Структура проекта
```
module_21_orm/
├── app.py              # Flask-приложение + API endpoints
├── models.py           # ORM-модели (Author, Book, Student, ReceivingBook)
├── fill_db.py          # Скрипт заполнения БД тестовыми данными
├── requirements.txt    # Зависимости
── README.md
```

## Запуск
```bash
# Установка зависимостей
pip install -r requirements.txt

# Заполнение БД тестовыми данными
python fill_db.py

# Запуск приложения
python app.py
```

## API Endpoints
- `GET /api/books` — список всех книг
- `GET /api/books/<id>` — информация о книге
- `POST /api/books` — добавить книгу
- `PUT /api/books/<id>` — обновить книгу
- `DELETE /api/books/<id>` — удалить книгу
- `GET /api/authors` — список авторов
- `POST /api/authors` — добавить автора
- `GET /api/debtors` — список должников (>14 дней)
- `POST /api/issue` — выдать книгу студенту
- `POST /api/return` — вернуть книгу

## Чему научился
- ✅ Проектирование реляционной схемы БД
- ✅ ORM-модели с связями One-to-Many и Many-to-Many
- ✅ AssociationProxy для Many-to-Many
- ✅ Каскадное удаление
- ✅ hybrid_property и @classmethod
- ✅ Жадная подгрузка (joinedload, subqueryload)
- ✅ Массовая вставка (bulk_insert_mappings)
- ✅ REST API с Flask-RESTful
- ✅ Сериализация через marshmallow
"@ | Out-File -FilePath "README.md" -Encoding UTF8
```