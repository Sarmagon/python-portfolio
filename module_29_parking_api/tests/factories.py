import random
import factory
from app.models import db, Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    car_number = factory.Faker('license_plate')
    
    # С вероятностью 80% генерируем номер карты, иначе None
    credit_card = factory.LazyAttribute(
        lambda x: factory.Faker('credit_card_number').evaluate(None, None, {'locale': 'en_US'}) 
        if random.random() < 0.8 
        else None
    )


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=10, max=500)
    # LazyAttribute: свободные места не могут быть больше общего количества
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)