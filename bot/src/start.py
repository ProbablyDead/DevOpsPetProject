from aiogram import F, types
from aiogram.filters import Command

from .poll import router, start_test, reply_keyboard

from .database import Database
from .payment import Payment

from .__main__ import TelegramBot


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветствуем тебя в нашем замечательном боте!", reply_markup=reply_keyboard())


@router.message(F.text.lower() == "пройти тест")
async def start_poll(message: types.Message):
    await start_test(message)


async def payment_callback(user_id, succeed: bool):
    if succeed:
        Database.add_payment(user_id)
        await TelegramBot.bot.send_message(user_id, "Спасибо за покупку!\nДля согласования доставки свяжись, пожалуйста, с ответственным за заказы: @souvenir_perfume_order")
    else:
        await TelegramBot.bot.send_message(user_id, "*К сожалению оплата не прошла.*\n\nЕсли возникла ошибка, напиши, пожалуйста, нашему техническому специалисту: @wrkngYkz", parse_mode="Markdown")


@router.message(F.text.lower() == "заказать аромат")
async def get_contacts(message: types.Message):

    payment_link = Payment.create_payment(str(message.from_user.id),
                                          message.from_user.username, payment_callback)

    await message.answer(f"Конечно! Вот ссылка для оплаты:\n\n{payment_link},\n\nПосле оплаты ты можешь связаться с ответственным за заказы: @souvenir_perfume_order и договориться о способе получения _(самовывоз метро Таганская, Москва и доставка по России)_, а так же обговорить интересующие тебя вопросы и пожелания касательно аромата\n\n_Срок изготовления 2-5 дней_",
                         reply_markup=reply_keyboard(), parse_mode="Markdown")
