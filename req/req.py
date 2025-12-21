import requests
import json

API_URL = "http://127.0.0.1:5000/"

class Req():
    token = None

    @staticmethod
    def send_get_request(path):
        try:
            return requests.get(API_URL + path, headers={'Authorization': f'Bearer {Req.token}'}).json()
        except:
            return None

    @staticmethod
    def send_post_request(path, data):
        try:
            return requests.post(API_URL + path, data=json.dumps(data), headers={'Authorization': f'Bearer {Req.token}'}).json()
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def generate_token(login, password):
        responce = requests.post(API_URL + "token", data='{"login": "' + login + '", "password": "' + password + '"}').json()
        if "access_token" in responce:
            Req.token = responce["access_token"]
            return True
        return False

    @staticmethod
    def clear_token():
        Req.token = None