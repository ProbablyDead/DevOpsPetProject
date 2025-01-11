import os
import requests
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')


class Database:
    def __init__(self):
        self.connection_string = f"http://{DATABASE_HOST}:{DATABASE_PORT}"

    def add_pass(self, user_id, user_name, test_result):
        data = {
            "user_id": user_id,
            "user_name": user_name,
            "test_result": test_result
        }
        requests.post(self.connection_string+"/add_pass", json=data)

    def add_payment(self, user_id):
        data = {
            "user_id": user_id
        }
        requests.post(self.connection_string+"/add_payment", json=data)
