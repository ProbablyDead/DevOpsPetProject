from bottle import Bottle, request
from .payment.payment import Payment
from http import client
import json

child_app = Bottle()


@child_app.post('/create_payment')
def create_payment():
    data = json.load(request.body)

    user_name = data['user_name']
    user_id = data['user_id']
    web_hook = data['web_hook']
    price = data['price']
    return_url = data['return_url']

    def callback(result):
        body = json.dumps({"user_id": user_id, "result": result})
        headers = {'Content-type': 'application/json'}

        client.HTTPConnection(web_hook['host']). \
            request("POST", "/" + web_hook['url'], body=body, headers=headers)

    return Payment().create_payment(callback, user_name, price, return_url)
