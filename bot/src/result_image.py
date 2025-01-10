import requests
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("IMAGE_PROCESSOR_HOST")
PORT = os.getenv("IMAGE_PROCESSOR_PORT")


class ResultImage:
    @staticmethod
    def result_image(result):
        img = requests.post(
            f"http://{HOST}:{PORT}/create_image", json=result)
        return img.content
