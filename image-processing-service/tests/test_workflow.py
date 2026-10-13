import io
import json
import os
import tempfile
import uuid
import zipfile
from pathlib import Path

import pytest
from PIL import Image

# Imports must never open the user's subscriber database or SMTP configuration.
os.environ['CELERY_BROKER_URL'] = 'memory://'
os.environ['CELERY_RESULT_BACKEND'] = 'cache+memory://'
test_root = Path(tempfile.mkdtemp(prefix='image-service-tests-'))
os.environ['SUBSCRIBERS_DATABASE_URL'] = f"sqlite:///{test_root / 'subscribers.db'}"

import app as application
import tasks
from celery_app import celery_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    application.app.config.update(TESTING=True, DATA_DIR=str(tmp_path))
    celery_app.conf.update(task_always_eager=True, task_store_eager_result=True,
                           task_eager_propagates=False)
    monkeypatch.setattr(tasks, 'send_email', lambda *args: None)
    return application.app.test_client()


def image_bytes():
    data = io.BytesIO()
    Image.new('RGB', (12, 12), 'red').save(data, 'PNG')
    data.seek(0)
    return data


def test_full_workflow_and_duplicate_untrusted_names(client, tmp_path, monkeypatch):
    sent = []
    monkeypatch.setattr(tasks, 'send_email', lambda *args: sent.append(args))
    response = client.post('/blur', data={'email': 'test@example.com',
        'images': [(image_bytes(), '../../same.png'), (image_bytes(), '../../same.png')]})
    assert response.status_code == 202
    status = client.get('/status/' + response.json['group_id']).json
    assert status['status'] == 'completed'
    assert status['progress'] == {'completed': 2, 'failed': 0, 'total': 2}
    assert len(sent) == 1
    with zipfile.ZipFile(sent[0][2]) as archive:
        assert len(archive.namelist()) == len(set(archive.namelist())) == 2
    assert len(list(tmp_path.glob('uploads/*/*.png'))) == 2
    assert not (tmp_path / 'same.png').exists()


def test_smtp_failure_is_not_completed(client, monkeypatch):
    def fail(*args):
        raise OSError('SMTP unavailable')
    monkeypatch.setattr(tasks, 'send_email', fail)
    response = client.post('/blur', data={'email': 'test@example.com',
                                        'images': (image_bytes(), 'test.png')})
    assert response.status_code == 202
    assert client.get('/status/' + response.json['group_id']).json['status'] == 'failed'


def test_incomplete_results_do_not_create_zip_or_send_email(tmp_path, monkeypatch):
    sent = []
    monkeypatch.setattr(tasks, 'send_email', lambda *args: sent.append(args))
    with pytest.raises(ValueError):
        tasks.process_order.run([str(tmp_path / 'missing.png')], 'order', 'test@example.com')
    assert not list(tmp_path.glob('*.zip'))
    assert not sent


@pytest.mark.parametrize('email, files', [('', True), ('invalid', True),
                                         ('test@example.com', False)])
def test_invalid_request(client, email, files):
    data = {'email': email}
    if files:
        data['images'] = (image_bytes(), 'image.png')
    assert client.post('/blur', data=data).status_code == 400


def test_invalid_image_cleans_uploads(client, tmp_path):
    response = client.post('/blur', data={'email': 'test@example.com',
                         'images': (io.BytesIO(b'not an image'), 'fake.png')})
    assert response.status_code == 400
    assert not list(tmp_path.glob('uploads/*'))
    assert not list(tmp_path.glob('orders/*'))


def test_unknown_job(client):
    assert client.get('/status/' + str(uuid.uuid4())).status_code == 404


def test_failed_image_is_not_successful_progress(client, tmp_path):
    image_id, result_id = str(uuid.uuid4()), str(uuid.uuid4())
    celery_app.backend.store_result(image_id, ValueError('bad image'), 'FAILURE')
    orders = tmp_path / 'orders'; orders.mkdir()
    (orders / f'{result_id}.json').write_text(json.dumps(
        {'task_ids': [image_id], 'result_id': result_id}), encoding='utf-8')
    response = client.get('/status/' + result_id)
    assert response.json['status'] == 'failed'
    assert response.json['progress']['completed'] == 0


def test_subscription_round_trip(client):
    payload = {'email': f'{uuid.uuid4().hex}@example.com'}
    assert client.post('/subscribe', json=payload).status_code == 201
    assert client.post('/unsubscribe', json=payload).status_code == 200
    assert client.post('/subscribe', json=payload).status_code == 200
