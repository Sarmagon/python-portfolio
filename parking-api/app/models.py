from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)

    def to_dict(self):
        """Сериализация объекта в словарь для JSON"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parking'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, nullable=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Сериализация объекта в словарь для JSON"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parking'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=True)
    time_in = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    time_out = db.Column(db.DateTime, nullable=True)

    # Ограничение уникальности из ТЗ
    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    # Связи с другими моделями
    client = db.relationship("Client", backref="parking_logs")
    parking = db.relationship("Parking", backref="client_logs")

    def to_dict(self):
        """Сериализация объекта в словарь для JSON"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'parking_id': self.parking_id,
            'time_in': self.time_in.isoformat() if self.time_in else None,
            'time_out': self.time_out.isoformat() if self.time_out else None
        }