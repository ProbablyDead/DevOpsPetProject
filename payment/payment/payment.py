import os
import json
import time
import asyncio
from threading import Thread

from dotenv import load_dotenv

from yookassa import Configuration, Payment as pmt

load_dotenv()

SHOP_ID = os.getenv('SHOP_ID')
SHOP_KEY = os.getenv('SHOP_KEY')

Configuration.configure(SHOP_ID, SHOP_KEY)

PRICE = os.getenv('PRICE')
RETURN_URL = os.getenv('RETURN_URL')


class Payment:
    def __init__(self):
        self.__DESCRIPTION = "Оплата пользователя"
        self.__payment_id = None

    def create_payment(self, callback, user_name):
        payment = pmt.create({
            "amount": {
                "value": PRICE,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": RETURN_URL
            },
            "capture": True,
            "description": f"{self.__DESCRIPTION}: {user_name}"
        })

        payment_data = json.loads(payment.json())
        self.__payment_id = payment_data['id']

        # Run in parallel thread
        Thread(target=self.__check_payment,
               args=(callback, asyncio.get_event_loop())).start()

        return (payment_data['confirmation'])['confirmation_url']

    # callback - (bool) => None
    def __check_payment(self, callback, event_loop):
        payment = json.loads((pmt.find_one(self.__payment_id)).json())
        while payment['status'] == 'pending':
            payment = json.loads((pmt.find_one(self.__payment_id)).json())
            time.sleep(3)

        asyncio.run_coroutine_threadsafe(
            callback(payment['status'] == 'succeeded'),
            loop=event_loop)
