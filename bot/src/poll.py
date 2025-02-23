from aiogram import F
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from contextlib import suppress
from io import BytesIO
from PIL import Image

from .load_test import QUESTION_COUNT, test
from .database import Database
from .result_image import ResultImage

import asyncio
import os
import json

router = Router()

load_dotenv()
PRICE = os.getenv('PRICE')


def reply_keyboard():
    kb = [
        [
            types.KeyboardButton(text="Пройти тест"),
            types.KeyboardButton(text="Заказать аромат")
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери действие",
    )


class last_question(StatesGroup):
    view_quest = State()


async def start_test(message: types.Message):
    await set_question(0, [], message=message, first=True)


def form_buttons(q_num: int, chooses: list[int]):
    def button(i):
        string = f"answer_{q_num}_?_{
            json.dumps(chooses+[i-1], separators=(',', ':'))}"
        return types.InlineKeyboardButton(text=str(i), callback_data=string)

    back_button = [types.InlineKeyboardButton(
        text="Назад ↩", callback_data=f"answer_{q_num}_!_{chooses[:-1]}")]

    buttons = [[button(i), button(i+1)] for i in range(1, 5, 2)]

    if q_num:
        buttons.append(back_button)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def set_question(num: int,
                       chooses: list[int],
                       message: types.Message,
                       state=None,
                       first: bool = False):
    q = test[num]
    text = f"{num+1}/{QUESTION_COUNT}\n\n<b>{q['title']}</b>"

    if "options" in q:
        options = q["options"]

        for i in range(len(options)):
            text += f'\n\t {i+1}. {options[i]}'

    if q["type"] == "open":
        await state.set_state(last_question.view_quest)
        await state.update_data(chooses=chooses)
        await message.edit_text(text)
        return

    buttons = form_buttons(num, chooses)

    if not first:
        with suppress(TelegramBadRequest):
            await message.edit_text(text, reply_markup=buttons)
    else:
        await message.answer(text, reply_markup=buttons)


@router.callback_query(F.data.startswith("answer"))
async def test_routing(callback: types.CallbackQuery, state: FSMContext):
    _, num, operation, chooses = callback.data.split("_")
    chooses = json.loads(chooses)
    num = int(num)

    if operation == '!':
        await state.clear()
        await set_question(num - 1, chooses, callback.message, state=state)
        return

    await set_question(num + 1, chooses, callback.message, state=state)


@router.message(last_question.view_quest)
async def answer(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 20:
        await message.answer("Пожалуйста, укажи название длинной не более 20 символов")
        return

    user_data = await state.get_data()
    chooses = user_data.get("chooses")

    result = {
        "ingredients": [
            {
                "id": q["ingredientsID"][a],
                "name": q["ingredients"][a]
            } for q, a in zip(test, chooses)
        ],
        "title": message.text
    }

    result_for_db = [
        ingredient["name"] for ingredient in result["ingredients"]
    ] + [result["title"]]

    Database.add_pass(str(message.from_user.id),
                      message.from_user.username, result_for_db)

    async def create_image_and_answer():
        bio = BytesIO()
        bio.name = 'result.jpeg'

        img = Image.open(BytesIO(ResultImage.result_image(result)))

        img.save(bio, "JPEG")
        bio.seek(0)

        await message.answer_photo(photo=types.BufferedInputFile(bio.getvalue(),
                                                                 "result.jpeg"),
                                   caption=f'Спасибо за прохождение теста!\
            Ты сможешь заказать этот аромат объемом 6мл по цене {PRICE.partition(".")[0]} рублей, нажав *"Заказать аромат"*',
                                   reply_markup=reply_keyboard(), parse_mode="Markdown")

        await state.clear()

    asyncio.run_coroutine_threadsafe(
        create_image_and_answer(), loop=asyncio.get_event_loop())
