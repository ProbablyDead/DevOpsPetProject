import gspread
from gspread import Cell
import os
import zoneinfo

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMPTY_USER = "__empty__"
CREDENTIALS_FILE = './secrets/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
INGREDIENT_QUESTION_COUNT = int(os.getenv("INGREDIENT_QUESTION_COUNT"))

if not SPREADSHEET_ID:
    print("No spreadsheet id")
    exit()


class Google_worker:
    def __init__(self) -> None:
        self.__gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.__sh = self.__gc.open_by_key(SPREADSHEET_ID)
        self.__worksheet = self.__sh.get_worksheet_by_id(0)

    def __add_line(self, body) -> None:
        self.__worksheet.append_row(body, table_range='A:A')

    def update_sheet(self, userName: str, new_values: [str]) -> None:
        cell = self.__worksheet.find(userName)

        new_str = [userName] + new_values

        if cell:
            self.__worksheet.update(range_name=cell.address, values=[new_str])
        else:
            self.__add_line(new_str)

    def add_payment(self, userName: str, new_value: int | str):
        cell = self.__worksheet.find(userName)

        payment_cell = gspread.Cell(
            cell.row,
            cell.col + INGREDIENT_QUESTION_COUNT + 3
        )

        zone = zoneinfo.ZoneInfo("Europe/Moscow")

        payment_data = [
            new_value,
            str(datetime.now(zone).date()),
            datetime.now(zone).time().strftime("%H:%M:%S")
        ]

        self.__worksheet.update(
            range_name=payment_cell.address,
            values=[payment_data]
        )
