import asyncio
import json
import os
from .database import Database
import requests
from dotenv import load_dotenv
from bottle import Bottle, request
from threading import Thread

load_dotenv()

PAYMENT_HOST = os.getenv('PAYMENT_HOST')
PAYMENT_PORT = os.getenv('PAYMENT_PORT')
PAYMENT_CONNECTION_STRING = f"http://{PAYMENT_HOST}:{PAYMENT_PORT}"

PRICE = os.getenv('PRICE')
RETURN_URL = os.getenv('RETURN_URL')

WEB_HOOK_PATH = "/souvenir/web_hook"
PAYMENT_WEB_HOOK_HOST = os.getenv("PAYMENT_WEB_HOOK_HOST")
PAYMENT_WEB_HOOK_PORT = int(os.getenv("PAYMENT_WEB_HOOK_PORT"))


class Payment:
    success_payment_callback = None
    failure_payment_callback = None

    @classmethod
    def create_payment(_, user_id, user_name):
        data = {
            "user_id": user_id,
            "user_name": user_name,
            "price": PRICE,
            "web_hook": f"http://{PAYMENT_WEB_HOOK_HOST}:{PAYMENT_WEB_HOOK_PORT}{WEB_HOOK_PATH}",
            "return_url": RETURN_URL
        }

        responce = requests.post(
            PAYMENT_CONNECTION_STRING+"/create_payment", json=data)

        return responce.content.decode("utf-8")


app = Bottle()


@app.route("/")
def root():
    return "root"


async def web_hook_callback(user_id, result):
    if result:
        await Database.add_payment(user_id)
        await Payment.success_payment_callback(user_id)
    else:
        await Payment.failure_payment_callback(user_id)


@app.post(WEB_HOOK_PATH)
def web_hook():
    global ll
    data = json.load(request.body)
    asyncio.run(
        web_hook_callback(data['user_id'], data['result']))


s = Thread(target=app.run,
           kwargs={"host": '0.0.0.0', "port": PAYMENT_WEB_HOOK_PORT},
           daemon=True)
s.start()
