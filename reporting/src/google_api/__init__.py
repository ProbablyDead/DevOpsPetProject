from dotenv import load_dotenv

import os
load_dotenv()

EMPTY_USER = "__empty__"
CREDENTIALS_FILE = './src/google_api/secrets/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
INGREDIENT_QUESTION_COUNT = int(os.getenv("INGREDIENT_QUESTION_COUNT"))

if not SPREADSHEET_ID:
    print("No spreadsheet id")
    exit()
