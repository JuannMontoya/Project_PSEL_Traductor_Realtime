import requests

class ApiManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):
        try:
            response = requests.get(url=self.base_url + endpoint, params=params, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def post(self, endpoint, data=None, headers=None):
        try:
            response = requests.post(url=self.base_url + endpoint, data=data, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None