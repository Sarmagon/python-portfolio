from flask import Flask
from config import TestingConfig
from .models import db


def create_app(config_class=TestingConfig):
    """
    Application Factory для создания Flask приложения.
    Использует отложенную инициализацию SQLAlchemy через init_app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализируем SQLAlchemy с помощью init_app (отложенная инициализация)
    db.init_app(app)

    # Импортируем роуты внутри функции, чтобы избежать циклических импортов
    from .routes import create_routes
    create_routes(app)

    return app