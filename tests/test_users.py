import requests
import time

def test_get_user(api_headers, create_user):
    user_id = create_user["id"]
    url = f"https://gorest.co.in/public/v2/users/{user_id}"
    get_response = requests.get(url, headers=api_headers)
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


def test_patch_user(api_headers, create_user):
    user_id = create_user["id"]
    url = f"https://gorest.co.in/public/v2/users/{user_id}"
    patch_payload = {"name": "Иван Измененный"}
    patch_response = requests.patch(url,json = patch_payload, headers=api_headers)
    assert patch_response.status_code == 200
    patch_data = patch_response.json()
    assert "name" in patch_data, f"В ответе нет поля name: {patch_data}"
    assert patch_data["name"] == patch_payload["name"], f"name ожидали {patch_payload['name']}, получили {patch_data['name']}"

def test_create_user_without_token():
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    url = "https://gorest.co.in/public/v2/users"
    post_response = requests.post(url, json=payload)
    assert post_response.status_code == 401


def test_create_user_with_using_email(api_headers):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    url = "https://gorest.co.in/public/v2/users"
    post_response = requests.post(url, json=payload, headers=api_headers)
    user_id = post_response.json()["id"]
    assert post_response.status_code == 201

    duplicate_email = requests.post(url, json=payload, headers=api_headers)
    assert duplicate_email.status_code == 422

    delete_url = f"https://gorest.co.in/public/v2/users/{user_id}"
    delete_after_test = requests.delete(delete_url, headers=api_headers)
    assert delete_after_test.status_code == 204


def test_nonexistent_user(api_headers):
    user_id = "fake"
    get_url = f"https://gorest.co.in/public/v2/users/{user_id}"
    get_response = requests.get(get_url, headers=api_headers)
    assert get_response.status_code == 404

