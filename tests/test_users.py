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
