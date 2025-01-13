import os
from dotenv import load_dotenv
from yookassa import Configuration

load_dotenv()

SHOP_ID = os.getenv('SHOP_ID')
SHOP_KEY = os.getenv('SHOP_KEY')

Configuration.configure(SHOP_ID, SHOP_KEY)
