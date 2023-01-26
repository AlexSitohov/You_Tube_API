from main import app
from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database import Base, get_db
from datetime import datetime


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@test_postgres/test_youtube'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/test_youtube"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_registration(client):
    response = client.post('/registration',
                           json={
                               "first_name": "alexander",
                               "last_name": "merc",
                               "username": "merc",
                               "password": "123",
                               "date_time_registration": str(datetime.now())
                           })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('first_name') == 'alexander'
    assert response.json().get('last_name') == 'merc'


def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0].get('first_name') == 'alexander'


def test_get_user(client):
    response = client.get('/user/1')
    assert response.status_code == status.HTTP_200_OK


def test_get_contents(client):
    response = client.get('/contents')

    assert response.status_code == status.HTTP_200_OK
