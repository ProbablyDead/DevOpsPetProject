import asyncio
import aiohttp
import logging

import os

from dotenv import load_dotenv

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from .payment import Payment

from .poll import router
from .start import *


class TelegramBot:
    def __init__(self) -> None:
        load_dotenv()
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')

        if self.BOT_TOKEN is None:
            print("Cannot locate env var BOT_TOKEN")
            exit(1)

        logging.basicConfig(level=logging.INFO)

        self.bot = Bot(token=self.BOT_TOKEN,
                       default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        self.dp = Dispatcher()
        self.dp.include_router(router)

        Payment.success_payment_callback = self.__success_payment
        Payment.failure_payment_callback = self.__failure_payment

    async def __send_user(self, user_id, message):
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"

        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)) as session:
            await session.post(url, json={"chat_id": user_id, "text": message, "parse_mode": "Markdown"})

    async def __success_payment(self, user_id):
        await self.__send_user(user_id, "Спасибо за покупку!\nДля согласования доставки свяжись, пожалуйста, с ответственным за заказы: @souvenir_perfume_order")

    async def __failure_payment(self, user_id):
        await self.__send_user(user_id, "*К сожалению оплата не прошла.*\n\nЕсли возникла ошибка, напиши, пожалуйста, нашему техническому специалисту: @wrkngYkz")

    async def main(self):
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    asyncio.run(TelegramBot().main())
