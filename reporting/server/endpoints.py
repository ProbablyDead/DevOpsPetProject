from bottle import Bottle, request
from .google_api.google_api import Google_worker

import asyncio
import json

child_app = Bottle()
api = Google_worker()


async def proceed(function, data):
    function(**json.load(data))


@child_app.post('/update_test')
def update_test():
    asyncio.run(proceed(api.update_test, request.body))


@child_app.post('/add_payment')
def add_payment():
    asyncio.run(proceed(api.add_payment, request.body))
