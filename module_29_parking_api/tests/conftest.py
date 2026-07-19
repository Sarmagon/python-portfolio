import pytest
from app import create_app
from app.models import db, Client, Parking, ClientParking
from datetime import datetime


@pytest.fixture
def app():
    """
    Фикстура приложения.
    Создаёт тестовое приложение, таблицы БД и тестовые данные:
    - клиента
    - парковку
    - парковочный лог с фиксацией времени въезда и выезда
    """
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with _app.app_context():
        db.create_all()

        # Создаём тестового клиента
        test_client = Client(
            id=1,
            name="Иван",
            surname="Петров",
            credit_card="1234-5678-9012-3456",
            car_number="А123БВ77"
        )
        db.session.add(test_client)

        # Создаём тестовую парковку
        parking = Parking(
            id=1,
            address="ул. Ленина, 10",
            opened=True,
            count_places=10,
            count_available_places=9  # одно место уже занято
        )
        db.session.add(parking)

        # Создаём парковочный лог с фиксацией времени въезда и выезда
        log = ClientParking(
            id=1,
            client_id=1,
            parking_id=1,
            time_in=datetime(2026, 7, 19, 10, 0, 0),
            time_out=datetime(2026, 7, 19, 12, 0, 0)
        )
        db.session.add(log)

        db.session.commit()

        yield _app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Фикстура тестового клиента для HTTP-запросов"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Фикстура для работы с БД в тестах."""
    with app.app_context():
        yield db