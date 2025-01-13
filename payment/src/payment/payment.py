import json
import time
import asyncio
from threading import Thread
from yookassa import Payment as pmt


class Payment:
    def __init__(self):
        self.__DESCRIPTION = "Оплата пользователя"
        self.__payment_id = None

    def create_payment(self, callback, user_name, price, return_url):
        payment = pmt.create({
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
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
        waiting_time = 3
        cycle_sum = 0
        max_cycles = 10*60/waiting_time  # 10 min
        while payment['status'] == 'pending':
            if cycle_sum > max_cycles:
                break
            payment = json.loads((pmt.find_one(self.__payment_id)).json())
            cycle_sum += 1
            time.sleep(waiting_time)

        callback(payment['status'] == 'succeeded')
