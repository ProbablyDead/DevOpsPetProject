import os
import asyncio
import requests
from threading import Thread
from dotenv import load_dotenv

load_dotenv()

PAYMENT_HOST = os.getenv('PAYMENT_HOST')
PAYMENT_PORT = os.getenv('PAYMENT_PORT')
PAYMENT_CONNECTION_STRING = f"http://{PAYMENT_HOST}:{PAYMENT_PORT}"

PRICE = os.getenv('PRICE')
RETURN_URL = os.getenv('RETURN_URL')


class Payment:
    @classmethod
    def create_payment(_, user_id, user_name, callback):
        data = {
            "user_id": user_id,
            "user_name": user_name,
            "price": PRICE,
            "web_hook": "http://google.com",
            "return_url": RETURN_URL
        }

        responce = requests.post(
            PAYMENT_CONNECTION_STRING+"/create_payment", json=data)

        return responce.content.decode("utf-8")
