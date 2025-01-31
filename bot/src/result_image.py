import requests
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("IMAGE_PROCESSOR_HOST")
PORT = os.getenv("IMAGE_PROCESSOR_PORT", 80)

IMAGE_CONNECTION_STRING = f"http://{HOST}:{PORT}/create_image"


class ResultImage:
    @staticmethod
    def result_image(result):
        img = requests.post(
            IMAGE_CONNECTION_STRING, json=result)
        return img.content
