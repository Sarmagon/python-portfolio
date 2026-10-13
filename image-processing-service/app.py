import json
import os
import re
import shutil
import uuid
import warnings
from pathlib import Path

from celery import chord
from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError

from celery_app import celery_app
from subscribers import Session, Subscriber
from tasks import blur_task, process_order

app = Flask(__name__)
app.json.ensure_ascii = False
app.config.update(MAX_CONTENT_LENGTH=20 * 1024 * 1024,
                  DATA_DIR=os.getenv('IMAGE_SERVICE_DATA_DIR', '.'))
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@app.errorhandler(413)
def too_large(error):
    return jsonify({'error': 'Лимит запроса: 20 MiB'}), 413


@app.route('/blur', methods=['POST'])
def blur():
    email = request.form.get('email', '').strip()
    if len(email) > 254 or not EMAIL_RE.fullmatch(email):
        return jsonify({'error': 'Укажите корректный email'}), 400
    files = request.files.getlist('images')
    if not 1 <= len(files) <= 10 or any(not f.filename for f in files):
        return jsonify({'error': 'Требуется от 1 до 10 изображений'}), 400

    order_id = str(uuid.uuid4())
    data_dir = Path(app.config['DATA_DIR']).resolve()
    upload_dir = data_dir / 'uploads' / order_id
    output_dir = data_dir / 'results' / order_id
    upload_dir.mkdir(parents=True)
    paths = []
    try:
        for file in files:
            # Never use client filenames as filesystem paths. Decode actual images
            # and re-encode as PNG; duplicate names stay distinct.
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(file.stream) as image:
                    if image.format not in {'PNG', 'JPEG', 'WEBP'}:
                        raise ValueError('Unsupported image format')
                    image.load()
                    destination = upload_dir / f'{uuid.uuid4().hex}.png'
                    image.convert('RGBA').save(destination, format='PNG')
                    paths.append(str(destination))
    except (UnidentifiedImageError, OSError, ValueError,
            Image.DecompressionBombError, Image.DecompressionBombWarning):
        shutil.rmtree(upload_dir)
        return jsonify({'error': 'Допустимы корректные PNG, JPEG или WEBP'}), 400

    task_ids = [str(uuid.uuid4()) for _ in paths]
    result_id = str(uuid.uuid4())
    header = [blur_task.s(path, order_id, str(output_dir)).set(task_id=task_id)
              for path, task_id in zip(paths, task_ids)]
    body = process_order.s(order_id, email).set(task_id=result_id)
    orders = data_dir / 'orders'
    orders.mkdir(exist_ok=True)
    (orders / f'{result_id}.json').write_text(
        json.dumps({'task_ids': task_ids, 'result_id': result_id}), encoding='utf-8')
    try:
        chord(header, body).apply_async()
    except Exception:
        app.logger.exception('Unable to enqueue order %s', order_id)
        return jsonify({'error': 'Очередь недоступна', 'group_id': result_id}), 503
    return jsonify({'group_id': result_id, 'total_images': len(paths),
                    'message': 'Задачи поставлены в очередь'}), 202


@app.route('/status/<group_id>', methods=['GET'])
def status(group_id):
    try:
        uuid.UUID(group_id)
    except ValueError:
        return jsonify({'error': 'Задача не найдена'}), 404
    manifest = Path(app.config['DATA_DIR']).resolve() / 'orders' / f'{group_id}.json'
    if not manifest.is_file():
        return jsonify({'error': 'Задача не найдена'}), 404
    try:
        job = json.loads(manifest.read_text(encoding='utf-8'))
        images = [celery_app.AsyncResult(task_id) for task_id in job['task_ids']]
        delivery = celery_app.AsyncResult(job['result_id'])
        completed = sum(result.successful() for result in images)
        failed = sum(result.failed() for result in images)
        if failed or delivery.failed():
            state = 'failed'
        elif delivery.successful():
            state = 'completed'
        elif completed == len(images):
            state = 'finalizing'
        else:
            state = 'processing'
        return jsonify({'group_id': group_id, 'status': state,
                        'progress': {'completed': completed, 'failed': failed,
                                     'total': len(images)}})
    except Exception:
        app.logger.exception('Unable to read job status')
        return jsonify({'error': 'Статус временно недоступен'}), 503


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
    app.run(debug=False)