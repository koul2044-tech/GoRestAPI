import requests
import time
import pytest
from config import BASE_URL

def test_get_user(users_client, create_user):
    user_id = create_user["id"]
    get_response = users_client.get_user_by_id(user_id)
    assert get_response.status_code == 200
    user_data = get_response.json()
    assert "name" in user_data, f"В ответе нет поля name: {user_data}"
    assert user_data["name"] == create_user["name"], f"name ожидали {create_user['name']}, получили {user_data['name']}"
    assert "gender" in user_data, f"В ответе нет поля gender: {user_data}"
    assert user_data["gender"] == create_user[
        "gender"], f"gender ожидали {create_user['gender']}, получили {user_data['gender']}"
    assert "email" in user_data, f"В ответе нет поля email: {user_data}"
    assert user_data["email"] == create_user[
        "email"], f"email ожидали {create_user['email']}, получили {user_data['email']}"
    assert "status" in user_data, f"В ответе нет поля status: {user_data}"
    assert user_data["status"] == create_user[
        "status"], f"status ожидали {create_user['status']}, получили {user_data['status']}"


def test_patch_user(users_client, create_user):
    user_id = create_user["id"]
    patch_payload = {"name": "Иван Измененный"}
    patch_response = users_client.patch_user_by_id(user_id,patch_payload)
    assert patch_response.status_code == 200
    patch_data = patch_response.json()
    assert "name" in patch_data, f"В ответе нет поля name: {patch_data}"
    assert patch_data["name"] == patch_payload["name"], f"name ожидали {patch_payload['name']}, получили {patch_data['name']}"

def test_create_user_without_token(users_client):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    url = f"{BASE_URL}/users"
    post_response = requests.post(url, json=payload)
    assert post_response.status_code == 401


def test_create_user_with_using_email(users_client):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    post_response = users_client.create_user(payload)
    user_id = post_response.json()["id"]
    assert post_response.status_code == 201

    duplicate_email = users_client.create_user(payload)
    assert duplicate_email.status_code == 422

    delete_after_test = users_client.delete_user_by_id(user_id)
    assert delete_after_test.status_code == 204


def test_nonexistent_user(users_client):
    user_id = "fake"
    get_response = users_client.get_user_by_id(user_id)
    assert get_response.status_code == 404


@pytest.mark.parametrize("field, invalid_value", [("name", ""), ("gender", "unknown"),
("email", "not-an-email"), ("status", "deleted")])
def test_create_user_invalid_data(users_client,field, invalid_value):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active",
        field: invalid_value}
    post_response = users_client.create_user(payload)
    assert post_response.status_code == 422
    errors = post_response.json()
    assert errors[0]["field"] == field, f"Ожидали ошибку по полю {field}, получили {errors}"
