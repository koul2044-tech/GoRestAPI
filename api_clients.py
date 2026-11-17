import requests

from config import BASE_URL


class UsersClient:
    def __init__(self,headers):
        self.headers = headers
        self.base_url = f"{BASE_URL}/users"

    def get_user_by_id(self,user_id):
        url = f"{self.base_url}/{user_id}"
        return requests.get(url,headers=self.headers)

    def create_user(self,payload):
        url = f"{self.base_url}"
        return requests.post(url,json=payload,headers=self.headers)

    def delete_user_by_id(self,user_id):
        url = f"{self.base_url}/{user_id}"
        return requests.delete(url,headers=self.headers)