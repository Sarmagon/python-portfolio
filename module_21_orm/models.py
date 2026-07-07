from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event
from datetime import datetime
import re

engine = create_engine('sqlite:///library.db', echo=False)
Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    
    # Связь 1-to-many: у автора много книг
    # cascade='all, delete-orphan' - при удалении автора удалятся его книги
    books = relationship('Book', back_populates='author', 
                        cascade='all, delete-orphan',
                        lazy='joined')  # Жадная подгрузка через JOIN


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    
    # Обратная связь к автору
    author = relationship('Author', back_populates='books')
    
    # Связь с историей выдач
    receiving_history = relationship('ReceivingBook', back_populates='book',
                                    lazy='subquery')  # Подгрузка через подзапрос


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    
    # Связь с историей выдач
    received_books = relationship('ReceivingBook', back_populates='student',
                                 lazy='selectin')  # Эффективная подгрузка коллекции
    
    # ASSOCIATION PROXY: many-to-many связь students <-> books
    # через таблицу receiving_books
    books = association_proxy('received_books', 'book')
    
    # Classmethods из прошлого ДЗ
    @classmethod
    def get_students_with_scholarship(cls, session):
        return session.query(cls).filter(cls.scholarship == True).all()
    
    @classmethod
    def get_students_with_higher_score(cls, session, min_score):
        return session.query(cls).filter(cls.average_score > min_score).all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)
    
    # Связи
    book = relationship('Book', back_populates='receiving_history')
    student = relationship('Student', back_populates='received_books')
    
    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is not None:
            delta = self.date_of_return - self.date_of_issue
        else:
            delta = datetime.now() - self.date_of_issue
        return delta.days


# СОБЫТИЕ (Event) для валидации телефона
@event.listens_for(Student, 'before_insert')
def validate_phone(mapper, connection, target):
    """Проверка формата телефона: +7(9XX)-XXX-XX-XX"""
    pattern = r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, target.phone):
        raise ValueError(f"Неверный формат телефона: {target.phone}. Ожидается +7(9XX)-XXX-XX-XX")


Base.metadata.create_all(engine)