from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, extract
from models import engine, Book, Student, Author, ReceivingBook
from datetime import datetime
import csv
import io
import re

app = Flask(__name__)
# Поддержка русских букв в JSON (для всех версий Flask)
try:
    # Для Flask 2.2+
    app.json.ensure_ascii = False
except AttributeError:
    # Для старых версий Flask
    app.config['JSON_AS_ASCII'] = False

# Создание сессии
Session = sessionmaker(bind=engine)


# РОУТ 1: Количество книг по автору
@app.route('/author/<int:author_id>/books_count', methods=['GET'])
def get_books_count_by_author(author_id):
    """Получить количество оставшихся книг по автору"""
    session = Session()
    try:
        result = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
        count = result if result else 0
        return jsonify({'author_id': author_id, 'total_books_count': count}), 200
    finally:
        session.close()


# РОУТ 2: Книги, которые студент не читал, но другие книги этого автора уже брал
@app.route('/student/<int:student_id>/unread_books', methods=['GET'])
def get_unread_books_by_author(student_id):
    """Получить список книг, которые студент не читал, но другие книги этого автора уже брал"""
    session = Session()
    try:
        # Находим авторов, книги которых студент уже брал
        read_authors = session.query(Book.author_id).join(ReceivingBook).filter(
            ReceivingBook.student_id == student_id
        ).distinct().subquery()
        
        # Находим книги этих авторов, которые студент НЕ брал
        unread_books = session.query(Book).filter(
            Book.author_id.in_(read_authors),
            Book.id.notin_(
                session.query(ReceivingBook.book_id).filter(
                    ReceivingBook.student_id == student_id
                )
            )
        ).all()
        
        result = [
            {
                'id': book.id,
                'name': book.name,
                'author': f'{book.author.surname} {book.author.name}',
                'count': book.count
            }
            for book in unread_books
        ]
        
        return jsonify(result), 200
    finally:
        session.close()


# РОУТ 3: Среднее количество книг, которые студенты брали в этом месяце
@app.route('/average_books_this_month', methods=['GET'])
def get_average_books_this_month():
    """Получить среднее количество книг, которые студенты брали в этом месяце"""
    session = Session()
    try:
        now = datetime.now()
        # Начало текущего месяца
        start_of_month = datetime(now.year, now.month, 1)
        # Начало следующего месяца
        if now.month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(now.year, now.month + 1, 1)
        
        # Считаем количество выдач в этом месяце
        total_books = session.query(func.count(ReceivingBook.id)).filter(
            ReceivingBook.date_of_issue >= start_of_month,
            ReceivingBook.date_of_issue < start_of_next_month
        ).scalar()
        
        # Считаем количество уникальных студентов
        total_students = session.query(func.count(func.distinct(ReceivingBook.student_id))).filter(
            ReceivingBook.date_of_issue >= start_of_month,
            ReceivingBook.date_of_issue < start_of_next_month
        ).scalar()
        
        average = total_books / total_students if total_students > 0 else 0
        
        return jsonify({
            'month': now.month,
            'year': now.year,
            'total_books_issued': total_books,
            'total_students': total_students,
            'average_books_per_student': round(average, 2)
        }), 200
    finally:
        session.close()


# РОУТ 4: Самая популярная книга среди студентов со средним баллом > 4.0
@app.route('/most_popular_book_high_score', methods=['GET'])
def get_most_popular_book_high_score():
    """Получить самую популярную книгу среди студентов со средним баллом > 4.0"""
    session = Session()
    try:
        result = session.query(
            Book.name,
            func.count(ReceivingBook.id).label('read_count')
        ).join(ReceivingBook).join(Student).filter(
            Student.average_score > 4.0
        ).group_by(Book.id, Book.name).order_by(
            func.count(ReceivingBook.id).desc()
        ).first()
        
        if result:
            return jsonify({
                'book_name': result.name,
                'read_count': result.read_count
            }), 200
        else:
            return jsonify({'message': 'Нет данных'}), 200
    finally:
        session.close()


# РОУТ 5: ТОП-10 самых читающих студентов в этом году
@app.route('/top_10_readers_this_year', methods=['GET'])
def get_top_10_readers_this_year():
    """Получить ТОП-10 самых читающих студентов в этом году"""
    session = Session()
    try:
        now = datetime.now()
        # Начало текущего года
        start_of_year = datetime(now.year, 1, 1)
        # Начало следующего года
        start_of_next_year = datetime(now.year + 1, 1, 1)
        
        result = session.query(
            Student.surname,
            Student.name,
            func.count(ReceivingBook.id).label('books_count')
        ).join(ReceivingBook).filter(
            ReceivingBook.date_of_issue >= start_of_year,
            ReceivingBook.date_of_issue < start_of_next_year
        ).group_by(Student.id, Student.surname, Student.name).order_by(
            func.count(ReceivingBook.id).desc()
        ).limit(10).all()
        
        top_students = [
            {
                'name': f'{surname} {name}',
                'books_read': count
            }
            for surname, name, count in result
        ]
        
        return jsonify(top_students), 200
    finally:
        session.close()


# РОУТ 6: CSV импорт студентов (С ВАЛИДАЦИЕЙ ТЕЛЕФОНА!)
@app.route('/import_students', methods=['POST'])
def import_students():
    """Импорт студентов из CSV файла"""
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не найден'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400
    
    try:
        # Читаем файл
        content = file.read().decode('utf-8-sig')
        csv_data = csv.DictReader(io.StringIO(content), delimiter=';')
        
        # Подготавливаем данные для массовой вставки
        students_data = []
        for row in csv_data:
            # ВАЛИДАЦИЯ ТЕЛЕФОНА: формат +7(9XX)-XXX-XX-XX
            phone = row['phone']
            if not re.match(r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$', phone):
                return jsonify({
                    'error': f'Невалидный телефон: {phone}. Ожидается формат +7(9XX)-XXX-XX-XX'
                }), 400
            
            students_data.append({
                'name': row['name'],
                'surname': row['surname'],
                'phone': row['phone'],
                'email': row['email'],
                'average_score': float(row['average_score']),
                'scholarship': row['scholarship'].lower() == 'true'
            })
        
        # Массовая вставка
        session = Session()
        try:
            session.bulk_insert_mappings(Student, students_data)
            session.commit()
            return jsonify({
                'message': f'Успешно импортировано {len(students_data)} студентов'
            }), 201
        finally:
            session.close()
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)