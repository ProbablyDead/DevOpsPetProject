from google_api import Google_worker, INGREDIENT_QUESTION_COUNT

username = "yakiza_testoviy"
test = list(map(str, range(0, INGREDIENT_QUESTION_COUNT)))
payment_count = 1

Google_worker().update_sheet(username, test)
Google_worker().add_payment(username, payment_count)
