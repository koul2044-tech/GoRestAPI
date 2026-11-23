import requests

from config import BASE_URL


class UsersClient:
    def __init__(self,headers):
        self.headers = headers
        self.base_url = f"{BASE_URL}/users"

    def get_user_by_id(self,user_id):
        return self._request("GET", path=f"/{user_id}")

    def create_user(self,payload):
        return self._request("POST",json=payload)

    def delete_user_by_id(self,user_id):
        return self._request("DELETE", path=f"/{user_id}")

    def patch_user_by_id(self,user_id,payload):
        return self._request("PATCH", json=payload, path=f"/{user_id}")

    def _request(self,method,path="",json=None,params=None):
        url = f"{self.base_url}{path}"
        return requests.request(method,url,json=json,params=params,headers=self.headers)