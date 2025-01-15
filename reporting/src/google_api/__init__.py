from dotenv import load_dotenv

import os
load_dotenv()

EMPTY_USER = "__empty__"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
INGREDIENT_QUESTION_COUNT = int(os.getenv("INGREDIENT_QUESTION_COUNT"))

if not SPREADSHEET_ID:
    print("No spreadsheet id")
    exit()
