from bottle import Bottle
from .endpoints import child_app

app = Bottle()
app.merge(child_app)


def start_serv():
    app.run(host='0.0.0.0', port=8080)


@app.route('/')
def root():
    return '/'
