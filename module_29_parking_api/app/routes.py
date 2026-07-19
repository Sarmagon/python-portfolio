from flask import jsonify, request
from datetime import datetime
from .models import db, Client, Parking, ClientParking


def create_routes(app):
    """
    Функция для регистрации всех роутов приложения.
    Вынесена в отдельную функцию для избежания циклических импортов.
    """

    @app.route('/clients', methods=['GET'])
    def get_clients():
        """GET /clients — список всех клиентов"""
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients]), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        """GET /clients/<client_id> — информация клиента по ID"""
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        return jsonify(client.to_dict()), 200

    @app.route('/clients', methods=['POST'])
    def create_client():
        """POST /clients — создать нового клиента"""
        data = request.get_json()
        
        name = data.get('name')
        surname = data.get('surname')
        credit_card = data.get('credit_card')
        car_number = data.get('car_number')

        if not name or not surname:
            return jsonify({'error': 'Name and surname are required'}), 400

        new_client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )

        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client.to_dict()), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        """POST /parkings — создать новую парковочную зону"""
        data = request.get_json()
        
        address = data.get('address')
        opened = data.get('opened', True)
        count_places = data.get('count_places')
        count_available_places = data.get('count_available_places', count_places)

        if not address or count_places is None:
            return jsonify({'error': 'Address and count_places are required'}), 400

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places
        )

        db.session.add(new_parking)
        db.session.commit()

        return jsonify(new_parking.to_dict()), 201

    @app.route('/client_parkings', methods=['POST'])
    def client_parking_check_in():
        """
        POST /client_parkings — заезд на парковку.
        Проверяет:
        1. Открыта ли парковка
        2. Наличие свободных мест
        3. Уменьшает количество свободных мест
        4. Фиксирует время заезда
        """
        data = request.get_json()
        
        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        if not client_id or not parking_id:
            return jsonify({'error': 'client_id and parking_id are required'}), 400

        # Проверяем существование клиента и парковки
        client = Client.query.get(client_id)
        if not client:
            return jsonify({'error': 'Client not found'}), 404

        parking = Parking.query.get(parking_id)
        if not parking:
            return jsonify({'error': 'Parking not found'}), 404

        # Проверяем, открыта ли парковка
        if not parking.opened:
            return jsonify({'error': 'Parking is closed'}), 400

        # Проверяем наличие свободных мест
        if parking.count_available_places <= 0:
            return jsonify({'error': 'No available parking spaces'}), 400

        # Проверяем, не запаркован ли уже этот клиент на этой парковке
        existing_log = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first()
        
        if existing_log:
            return jsonify({'error': 'Client already parked here'}), 400

        # Создаем запись о заезде
        new_log = ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.utcnow(),
            time_out=None
        )

        # Уменьшаем количество свободных мест
        parking.count_available_places -= 1

        db.session.add(new_log)
        db.session.commit()

        return jsonify(new_log.to_dict()), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def client_parking_check_out():
        """
        DELETE /client_parkings — выезд с парковки.
        Проверяет:
        1. Наличие активной записи о парковке
        2. Увеличивает количество свободных мест
        3. Проставляет время выезда
        4. Проверяет наличие карты у клиента для оплаты
        """
        data = request.get_json()
        
        client_id = data.get('client_id')
        parking_id = data.get('parking_id')

        if not client_id or not parking_id:
            return jsonify({'error': 'client_id and parking_id are required'}), 400

        # Ищем активную запись о парковке (без time_out)
        parking_log = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first()

        if not parking_log:
            return jsonify({'error': 'No active parking session found'}), 404

        # Проверяем наличие карты у клиента для оплаты
        client = Client.query.get(client_id)
        if not client.credit_card:
            return jsonify({'error': 'No credit card attached for payment'}), 400

        # Получаем парковку
        parking = Parking.query.get(parking_id)
        if not parking:
            return jsonify({'error': 'Parking not found'}), 404

        # Проставляем время выезда
        parking_log.time_out = datetime.utcnow()

        # Увеличиваем количество свободных мест
        parking.count_available_places += 1

        db.session.commit()

        return jsonify(parking_log.to_dict()), 200

    return app