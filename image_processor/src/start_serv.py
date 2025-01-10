from bottle import Bottle
from .endpoints import child_app
import os

app = Bottle()
app.merge(child_app)

PORT = os.getenv("PORT")


def start_serv():
    app.run(host='0.0.0.0', port=PORT)


@app.route('/')
def root():
    return '/'
