import pytest
from flask.testing import FlaskClient
import tests as create_app
from typing import Generator

@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Trackly" in response.data

def test_about_page(client: FlaskClient):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Us" in response.data

def test_contact_page(client: FlaskClient):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"Contact Us" in response.data

def test_404_page(client: FlaskClient):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert b"Not Found" in response.data