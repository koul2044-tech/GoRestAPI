import requests
import time

def test_create_user(api_headers):
    payload = {
        "name": "Иван",
        "gender": "male",
        "email": f"user_{int(time.time())}@test.com",
        "status": "active"
    }
    url = "https://gorest.co.in/public/v2/users"
    post_response = requests.post(url, json=payload, headers=api_headers)
    assert post_response.status_code == 201
    user_id = post_response.json()["id"]
    url_get = f"https://gorest.co.in/public/v2/users/{user_id}"
    get_response = requests.get(url_get, headers=api_headers)
    assert get_response.status_code == 200
    user_data = get_response.json()
    assert "name" in user_data, f"В ответе нет поля name: {user_data}"
    assert user_data["name"] == payload["name"], f"name ожидали {payload['name']}, получили {user_data['name']}"
    assert "gender" in user_data, f"В ответе нет поля gender: {user_data}"
    assert user_data["gender"] == payload["gender"], f"gender ожидали {payload['gender']}, получили {user_data['gender']}"
    assert "email" in user_data, f"В ответе нет поля email: {user_data}"
    assert user_data["email"] == payload["email"], f"email ожидали {payload['email']}, получили {user_data['email']}"
    assert "status" in user_data, f"В ответе нет поля status: {user_data}"
    assert user_data["status"] == payload["status"], f"status ожидали {payload['status']}, получили {user_data['status']}"
    delete_after_test = requests.delete(url_get, headers=api_headers)
    assert delete_after_test.status_code == 204