from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_cities_list():
    response = client.get('/cities/get/?q=Moscow')
    print(response.json())
    assert response.status_code == 200


def test_users_list():
    response = client.get('/users/get/?min_age=20&max_age=40')
    assert response.status_code == 200


def test_picnics_list():
    response = client.get('/picnics/get')
    assert response.status_code == 200


def test_cities_create():
   response = client.post('/cities/create', json={"name": "Санкт-Петербург"})
   assert response.status_code == 200
