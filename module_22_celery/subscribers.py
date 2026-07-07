from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных SQLite для подписчиков
engine = create_engine('sqlite:///subscribers.db')
Base = declarative_base()


class Subscriber(Base):
    """Модель подписчика на рассылку."""
    __tablename__ = 'subscribers'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_subscribers():
    """Возвращает список активных подписчиков (email)."""
    session = Session()
    try:
        return [s.email for s in session.query(Subscriber).filter_by(active=True).all()]
    finally:
        session.close()