import pytest
from flask.testing import FlaskClient
import tests as app
import sys
import os
from typing import Generator
import logging

# Add the directory containing camera_module.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'machine-learning-client')))

@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_logging_configuration():
    logger = logging.getLogger()
    assert logger.level == logging.INFO

def test_process_video_get(client: FlaskClient):
    response = client.get('/process-video')
    assert response.status_code == 200

def test_process_video_post(client: FlaskClient):
    response = client.post('/process-video', data={'video': 'test_video_data'})
    assert response.status_code == 200

def test_process_session_post(client: FlaskClient):
    response = client.post('/process-session', json={'total_time': 100, 'focused_time': 75})
    assert response.status_code == 200