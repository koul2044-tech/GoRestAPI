import os
import time
import requests
import pytest
from dotenv import load_dotenv
from api_clients import UsersClient


load_dotenv()


@pytest.fixture
def api_headers():
    """Фиксура которая возвращает общие заголовки для запросов к GoRest API"""
    token = os.getenv("GOREST_TOKEN")

    if not token:
        raise ValueError("GOREST_TOKEN Не найден")

    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

@pytest.fixture
def create_user(users_client):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    response = users_client.create_user(payload)
    assert response.status_code == 201, f"Не удалось создать пользователя в фикстуре: {response.text}"

    user_data = response.json()
    user_id = user_data["id"]

    yield user_data
    users_client.delete_user_by_id(user_id)


@pytest.fixture
def users_client(api_headers):
    return UsersClient(api_headers)
