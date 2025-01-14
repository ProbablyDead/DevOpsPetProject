import gspread
import zoneinfo

from datetime import datetime
from .__init__ import \
    CREDENTIALS_FILE, \
    SPREADSHEET_ID, \
    INGREDIENT_QUESTION_COUNT


class Google_worker:
    def __init__(self) -> None:
        self.__gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.__sh = self.__gc.open_by_key(SPREADSHEET_ID)
        self.__worksheet = self.__sh.get_worksheet_by_id(0)

    def __add_line(self, body) -> None:
        self.__worksheet.append_row(body, table_range='A:A')

    def update_test(self, user_id: str, user_name: str, test: [str], pass_count: int) -> None:
        cell = self.__worksheet.find(user_id)

        new_str = [user_id, user_name] + test + [str(pass_count)]

        if cell:
            self.__worksheet.update(range_name=cell.address, values=[new_str])
        else:
            self.__add_line(new_str)

    def add_payment(self, user_id: str, payment_count: int | str):
        cell = self.__worksheet.find(user_id)

        payment_cell = gspread.Cell(
            cell.row,
            cell.col + INGREDIENT_QUESTION_COUNT + 5
        )

        zone = zoneinfo.ZoneInfo("Europe/Moscow")

        payment_data = [
            payment_count,
            str(datetime.now(zone).date()),
            datetime.now(zone).time().strftime("%H:%M:%S")
        ]

        self.__worksheet.update(
            range_name=payment_cell.address,
            values=[payment_data]
        )
