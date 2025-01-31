import os
import requests
import aiohttp
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT', 80)

DB_CONNECTION_STRING = f"http://{DATABASE_HOST}:{DATABASE_PORT}"


class Database:
    @classmethod
    def add_pass(_, user_id, user_name, test_result):
        data = {
            "user_id": user_id,
            "user_name": user_name,
            "test_result": test_result
        }
        requests.post(DB_CONNECTION_STRING+"/add_pass", json=data)

    @classmethod
    async def add_payment(_, user_id):
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            data = {"user_id": user_id}
            await session.post(DB_CONNECTION_STRING+'/add_payment', json=data)
