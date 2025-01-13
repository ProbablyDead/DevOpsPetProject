from bottle import Bottle
from .endpoints import child_app
from dotenv import load_dotenv
import os

load_dotenv()

app = Bottle()
app.merge(child_app)


def start_serv():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT")))


@app.route('/')
def root():
    return '/'
