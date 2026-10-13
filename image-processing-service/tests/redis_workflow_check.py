"""Run against a disposable Redis; SMTP is always mocked."""
import io
import os
import sys
import tempfile
import time
from pathlib import Path

redis_url = os.environ['IMAGE_TEST_REDIS_URL']
os.environ['CELERY_BROKER_URL'] = redis_url + '/0'
os.environ['CELERY_RESULT_BACKEND'] = redis_url + '/1'
root = Path(tempfile.mkdtemp(prefix='image-worker-tests-'))
os.environ['SUBSCRIBERS_DATABASE_URL'] = f"sqlite:///{root / 'subscribers.db'}"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
from celery.contrib.testing.worker import start_worker
import app
import tasks
from celery_app import celery_app

app.app.config.update(TESTING=True, DATA_DIR=str(root))
celery_app.conf.update(task_always_eager=False, worker_hijack_root_logger=False)
sent = []
tasks.send_email = lambda *args: sent.append(args)


def submit_and_wait(client):
    image = io.BytesIO()
    Image.new('RGB', (20, 20), 'green').save(image, 'PNG')
    image.seek(0)
    response = client.post('/blur', data={'email': 'test@example.com',
                                         'images': (image, 'test.png')})
    assert response.status_code == 202, response.json
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        state = client.get('/status/' + response.json['group_id']).json
        if state['status'] in {'completed', 'failed'}:
            return state
        time.sleep(0.1)
    raise AssertionError('Worker did not finish within 30 seconds')


with start_worker(celery_app, perform_ping_check=False, pool='solo', loglevel='CRITICAL'):
    client = app.app.test_client()
    state = submit_and_wait(client)
    assert state['status'] == 'completed', state
    assert len(sent) == 1 and Path(sent[0][2]).exists()

    def fail_smtp(*args):
        raise OSError('Mock SMTP unavailable')

    tasks.send_email = fail_smtp
    assert submit_and_wait(client)['status'] == 'failed'

    def fail_blur(*args):
        raise ValueError('Mock image processing error')

    tasks.blur_image = fail_blur
    state = submit_and_wait(client)
    assert state['status'] == 'failed' and state['progress']['completed'] == 0
    assert len(sent) == 1

print('3 Redis/worker scenarios passed: success, SMTP failure, image failure. No real email sent.')
