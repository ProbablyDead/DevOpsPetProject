import os
import requests
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

DB_CONNECTION_STRING = f"http://{DATABASE_HOST}:{DATABASE_PORT}"


class Database:
    @classmethod
    def add_pass(_, user_id, user_name, test_result):
        data = {
            "user_id": user_id,
            "user_name": user_name,
            "test_result": test_result
        }
        requests.post(DB_CONNECTION_STRING+"/add_pass", json=data)

    @classmethod
    def add_payment(_, user_id):
        data = {
            "user_id": user_id
        }
        requests.post(DB_CONNECTION_STRING+"/add_payment", json=data)
