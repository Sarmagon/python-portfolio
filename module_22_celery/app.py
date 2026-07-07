import os
import uuid
from flask import Flask, request, jsonify
from celery import group
from celery.result import GroupResult
from celery_app import celery_app
from tasks import blur_task, process_order
from subscribers import Session, Subscriber

app = Flask(__name__)

# Настройка кодировки JSON для поддержки кириллицы
app.config['JSON_AS_ASCII'] = False  # Для старых версий Flask (< 2.2)
try:
    app.json.ensure_ascii = False  # Для новых версий Flask (>= 2.2)
except AttributeError:
    pass


@app.route('/blur', methods=['POST'])
def blur():
    """
    Ставит в очередь обработку изображений.
    Принимает файлы и email пользователя.
    Возвращает ID группы задач.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email обязателен'}), 400

    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'Хотя бы одно изображение обязательно'}), 400

    order_id = str(uuid.uuid4())
    upload_dir = f'uploads/{order_id}'
    os.makedirs(upload_dir, exist_ok=True)

    image_paths = []
    for file in files:
        if file and file.filename:
            filepath = os.path.join(upload_dir, file.filename)
            file.save(filepath)
            image_paths.append(filepath)

    if not image_paths:
        return jsonify({'error': 'Не удалось сохранить файлы'}), 400

    output_dir = f'results/{order_id}'
    
    # Создаём группу задач для параллельной обработки
    blur_jobs = group(
        blur_task.s(path, order_id, output_dir)
        for path in image_paths
    )
    
    # Запускаем задачи размытия
    result = blur_jobs.apply_async()
    result.save()
    
    # Запускаем задачу создания ZIP и отправки email
    process_order.delay(image_paths, order_id, email)
    
    os.makedirs('orders', exist_ok=True)
    with open(f'orders/{result.id}', 'w') as f:
        f.write(f'{email}\n{len(image_paths)}')

    return jsonify({
        'group_id': result.id,
        'total_images': len(image_paths),
        'message': 'Задачи поставлены в очередь'
    }), 202


@app.route('/status/<group_id>', methods=['GET'])
def status(group_id):
    """
    Возвращает информацию о задаче:
    - прогресс (количество обработанных)
    - статус (в процессе / обработано)
    """
    try:
        result = GroupResult.restore(group_id, app=celery_app)
        
        if result is None:
            return jsonify({'error': 'Задача не найдена'}), 404

        total = len(result)
        completed = sum(1 for r in result.results if r.ready())
        
        if completed == total:
            task_status = 'completed'
        else:
            task_status = 'processing'

        return jsonify({
            'group_id': group_id,
            'status': task_status,
            'progress': {
                'completed': completed,
                'total': total
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Подписка на еженедельную рассылку"""
    # Пытаемся получить email из JSON или form-data
    email = None
    
    if request.is_json:
        data = request.get_json()
        email = data.get('email') if data else None
    else:
        email = request.form.get('email')
    
    if not email:
        return jsonify({'error': 'Email обязателен'}), 400

    session = Session()
    try:
        subscriber = session.query(Subscriber).filter_by(email=email).first()
        
        if subscriber:
            subscriber.active = True
            session.commit()
            return jsonify({'message': 'Подписка возобновлена'}), 200
        else:
            new_subscriber = Subscriber(email=email, active=True)
            session.add(new_subscriber)
            session.commit()
            return jsonify({'message': 'Вы успешно подписались'}), 201
    finally:
        session.close()


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Отписка от рассылки"""
    # Пытаемся получить email из JSON или form-data
    email = None
    
    if request.is_json:
        data = request.get_json()
        email = data.get('email') if data else None
    else:
        email = request.form.get('email')
    
    if not email:
        return jsonify({'error': 'Email обязателен'}), 400

    session = Session()
    try:
        subscriber = session.query(Subscriber).filter_by(email=email).first()
        
        if not subscriber:
            return jsonify({'error': 'Подписчик не найден'}), 404
        
        subscriber.active = False
        session.commit()
        return jsonify({'message': 'Вы отписались от рассылки'}), 200
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)