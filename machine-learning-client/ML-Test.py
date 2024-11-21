import pytest
from flask.testing import FlaskClient
import client as app
import sys
import os
import logging
from typing import Generator
from dotenv import load_dotenv
import pymongo

# Add the directory containing camera_module.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'machine-learning-client')))


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_video_get(client: FlaskClient):
    response = client.get('/process-video')
    assert response.status_code == 200

def test_process_video_post(client: FlaskClient):
    response = client.post('/process-video', data={'video': 'test_video_data'})
    assert response.status_code == 200

def test_process_session_post(client: FlaskClient):
    response = client.post('/process-session', data={'session': 'test_session_data'})
    assert response.status_code == 200

def test_logging_configuration():
    logger = logging.getLogger()
    assert logger.level == logging.INFO
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
    assert any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)

def test_mongo_connection():

    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client['productivity_db']
    collection = db['focus_data']
    assert collection.name == 'focus_data'