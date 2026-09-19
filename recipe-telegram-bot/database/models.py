from peewee import Model, SqliteDatabase, CharField, DateTimeField, IntegerField, ForeignKeyField
from datetime import datetime

# Создаем базу данных (файл будет создан в папке database/)
database = SqliteDatabase('database/bot_database.sqlite3')


class BaseModel(Model):
    """Базовый класс для всех моделей"""
    class Meta:
        database = database


class User(BaseModel):
    """Модель пользователя Telegram"""
    user_id = IntegerField(primary_key=True, help_text="ID пользователя Telegram")
    username = CharField(null=True, help_text="Никнейм пользователя")
    first_name = CharField(help_text="Имя пользователя")
    last_name = CharField(null=True, help_text="Фамилия пользователя")
    created_at = DateTimeField(default=datetime.now, help_text="Дата регистрации")

    class Meta:
        table_name = 'users'


class SearchHistory(BaseModel):
    """Модель для хранения истории поиска пользователей"""
    user = ForeignKeyField(User, backref='histories', on_delete='CASCADE')
    query = CharField(help_text="Поисковый запрос (ингредиент или название)")
    result_summary = CharField(help_text="Краткое описание результата (название блюда)")
    created_at = DateTimeField(default=datetime.now, help_text="Дата и время запроса")

    class Meta:
        table_name = 'search_history'


def initialize_database() -> None:
    """Инициализация таблиц базы данных"""
    database.connect()
    database.create_tables([User, SearchHistory], safe=True)
    database.close()