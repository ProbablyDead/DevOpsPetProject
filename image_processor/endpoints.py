from bottle import Bottle, request
from result_image import ResultImage
from io import BytesIO
import json

child_app = Bottle()


@child_app.post('/create_image')
def create_image():
    data = json.load(request.body)
    bio = BytesIO()
    bio.name = 'result.jpeg'

    img = ResultImage.result_image(**data)

    img.save(bio, "JPEG")
    bio.seek(0)

    return bio.read()
