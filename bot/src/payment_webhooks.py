from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/souvenir_bot/webhook', methods=['POST'])
def respond():
    print(request.json);
    return Response(status=200)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8443)
