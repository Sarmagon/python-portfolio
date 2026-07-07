from sqlalchemy.orm import sessionmaker
from models import engine, Book, Student, Author, ReceivingBook
from datetime import date, datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()

# Добавим авторов
author1 = Author(name="Лев", surname="Толстой")
author2 = Author(name="Фёдор", surname="Достоевский")
author3 = Author(name="Александр", surname="Пушкин")
session.add_all([author1, author2, author3])
session.commit()

# Добавим книги
book1 = Book(name="Война и мир", count=5, release_date=date(1869, 1, 1), author_id=author1.id)
book2 = Book(name="Анна Каренина", count=3, release_date=date(1877, 1, 1), author_id=author1.id)
book3 = Book(name="Преступление и наказание", count=4, release_date=date(1866, 1, 1), author_id=author2.id)
book4 = Book(name="Братья Карамазовы", count=2, release_date=date(1880, 1, 1), author_id=author2.id)
book5 = Book(name="Евгений Онегин", count=6, release_date=date(1833, 1, 1), author_id=author3.id)
session.add_all([book1, book2, book3, book4, book5])

# Добавим студентов
student1 = Student(
    name="Пётр", surname="Петров", 
    phone="+7(900)-123-45-67", 
    email="petr@example.com", 
    average_score=4.5, 
    scholarship=True
)
student2 = Student(
    name="Анна", surname="Сидорова", 
    phone="+7(901)-234-56-78", 
    email="anna@example.com", 
    average_score=3.8, 
    scholarship=False
)
student3 = Student(
    name="Иван", surname="Иванов", 
    phone="+7(902)-345-67-89", 
    email="ivan@example.com", 
    average_score=4.2, 
    scholarship=True
)
session.add_all([student1, student2, student3])
session.commit()

# Получаем текущую дату
now = datetime.now()

# Добавим выдачи книг
# Студент 1 брал "Война и мир" (Толстой) - в ИЮЛЕ (уже вернул)
receiving1 = ReceivingBook(
    book_id=book1.id,
    student_id=student1.id,
    date_of_issue=datetime(now.year, now.month, 1, 10, 0, 0),  # 1-е число текущего месяца
    date_of_return=datetime(now.year, now.month, 5, 10, 0, 0)  # 5-е число текущего месяца
)

# Студент 1 брал "Преступление и наказание" (Достоевский) - в ИЮЛЕ (не вернул)
receiving2 = ReceivingBook(
    book_id=book3.id,
    student_id=student1.id,
    date_of_issue=datetime(now.year, now.month, 3, 10, 0, 0),  # 3-е число текущего месяца
    date_of_return=None
)

# Студент 2 брал "Евгений Онегин" (Пушкин) - в ИЮЛЕ (вернул)
receiving3 = ReceivingBook(
    book_id=book5.id,
    student_id=student2.id,
    date_of_issue=datetime(now.year, now.month, 2, 10, 0, 0),  # 2-е число текущего месяца
    date_of_return=datetime(now.year, now.month, 10, 10, 0, 0)  # 10-е число текущего месяца
)

# Студент 3 брал "Анна Каренина" (Толстой) - в ИЮЛЕ (не вернул)
receiving4 = ReceivingBook(
    book_id=book2.id,
    student_id=student3.id,
    date_of_issue=datetime(now.year, now.month, 4, 10, 0, 0),  # 4-е число текущего месяца
    date_of_return=None
)

session.add_all([receiving1, receiving2, receiving3, receiving4])
session.commit()

print("✅ Тестовые данные добавлены!")
print(f"Авторов: {session.query(Author).count()}")
print(f"Книг: {session.query(Book).count()}")
print(f"Студентов: {session.query(Student).count()}")
print(f"Выдач: {session.query(ReceivingBook).count()}")
print(f"Все выдачи в {now.month}-м месяце {now.year} года")

session.close()