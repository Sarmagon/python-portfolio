import pytest
from app.models import db, Client, Parking, ClientParking
from .factories import ClientFactory, ParkingFactory


# 1. Параметризованный тест для GET-методов
@pytest.mark.parametrize("route", [
    "/clients",
    "/clients/1"
])
def test_get_routes(client, route):
    """Проверяем, что все GET-методы возвращают код 200"""
    response = client.get(route)
    assert response.status_code == 200


# 2. Тест создания клиента
def test_create_client(client, db_session):
    """POST /clients — создание нового клиента"""
    data = {
        "name": "Анна",
        "surname": "Сидорова",
        "credit_card": "1111-2222-3333-4444",
        "car_number": "В777ВВ77"
    }
    response = client.post("/clients", json=data)
    
    assert response.status_code == 201
    assert response.json["name"] == "Анна"
    assert response.json["car_number"] == "В777ВВ77"


# 3. Тест создания парковки
def test_create_parking(client, db_session):
    """POST /parkings — создание новой парковочной зоны"""
    data = {
        "address": "ул. Пушкина, 10",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    }
    response = client.post("/parkings", json=data)
    
    assert response.status_code == 201
    assert response.json["address"] == "ул. Пушкина, 10"
    assert response.json["count_places"] == 50


# 4. Тест заезда на парковку (с маркером parking)
@pytest.mark.parking
def test_check_in(client, db_session):
    """POST /client_parkings — заезд на парковку"""
    # Создаем данные через API и получаем реальные ID
    resp_client = client.post("/clients", json={"name": "Test", "surname": "User", "car_number": "A111AA"})
    resp_parking = client.post("/parkings", json={"address": "Test St", "opened": True, "count_places": 10, "count_available_places": 10})
    
    client_id = resp_client.json["id"]
    parking_id = resp_parking.json["id"]
    
    # Делаем заезд
    response = client.post("/client_parkings", json={"client_id": client_id, "parking_id": parking_id})
    
    assert response.status_code == 201
    
    # Проверяем, что количество свободных мест уменьшилось
    parking = db_session.session.query(Parking).get(parking_id)
    assert parking.count_available_places == 9


# 5. Тест выезда с парковки (с маркером parking)
@pytest.mark.parking
def test_check_out(client, db_session):
    """DELETE /client_parkings — выезд с парковки"""
    # Создаем клиента с картой и парковку через API
    resp_client = client.post("/clients", json={"name": "Out", "surname": "User", "credit_card": "5555", "car_number": "B222BB"})
    resp_parking = client.post("/parkings", json={"address": "Out St", "opened": True, "count_places": 10, "count_available_places": 10})
    
    client_id = resp_client.json["id"]
    parking_id = resp_parking.json["id"]
    
    # Заезжаем
    client.post("/client_parkings", json={"client_id": client_id, "parking_id": parking_id})
    
    # Выезжаем
    response = client.delete("/client_parkings", json={"client_id": client_id, "parking_id": parking_id})
    
    assert response.status_code == 200
    
    # Проверяем, что количество свободных мест увеличилось обратно
    parking = db_session.session.query(Parking).get(parking_id)
    assert parking.count_available_places == 10
    
    # Проверяем время выезда
    log = db_session.session.query(ClientParking).filter_by(
        client_id=client_id, 
        parking_id=parking_id
    ).first()
    assert log.time_out is not None
    assert log.time_out >= log.time_in


# Доп. тест: Выезд без карты (должен вернуть ошибку)
@pytest.mark.parking
def test_check_out_without_card(client, db_session):
    """Проверка оплаты: выезд невозможен без привязанной карты"""
    resp_client = client.post("/clients", json={"name": "NoCard", "surname": "User", "credit_card": None, "car_number": "C333CC"})
    resp_parking = client.post("/parkings", json={"address": "NoCard St", "opened": True, "count_places": 10, "count_available_places": 10})
    
    client_id = resp_client.json["id"]
    parking_id = resp_parking.json["id"]
    
    client.post("/client_parkings", json={"client_id": client_id, "parking_id": parking_id})
    
    response = client.delete("/client_parkings", json={"client_id": client_id, "parking_id": parking_id})
    
    assert response.status_code == 400
    assert "No credit card" in response.json["error"]


# --- Тесты с Factory Boy (Задание 4) ---

def test_create_client_with_factory(client, db_session):
    """Дубликат теста создания клиента, переписанный с использованием ClientFactory"""
    # Создаем клиента через фабрику
    new_client = ClientFactory()
    db_session.session.commit()
    
    # Проверяем, что клиент создан и имеет ID
    assert new_client.id is not None
    assert len(db_session.session.query(Client).all()) > 1
    
    # Проверяем через API, что клиент доступен
    response = client.get(f"/clients/{new_client.id}")
    assert response.status_code == 200
    assert response.json["name"] == new_client.name


def test_create_parking_with_factory(client, db_session):
    """Дубликат теста создания парковки, переписанный с использованием ParkingFactory"""
    # Создаем парковку через фабрику
    new_parking = ParkingFactory()
    db_session.session.commit()
    
    # Проверяем, что парковка создана и имеет ID
    assert new_parking.id is not None
    assert len(db_session.session.query(Parking).all()) > 1
    
    # Проверяем, что LazyAttribute сработал корректно
    assert new_parking.count_available_places <= new_parking.count_places
    
    # Проверяем через API
    response = client.get("/parkings") # Если бы был такой роут, но пока проверим создание
    # Для полноты картины можно проверить, что запись есть в БД
    parking_from_db = db_session.session.query(Parking).get(new_parking.id)
    assert parking_from_db.address == new_parking.address