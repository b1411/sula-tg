import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
import requests
from aiogram.methods.close import Close

dp = Dispatcher()

TOKEN = getenv('TOKEN')


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Здравствуйте! Я бот-помощник Султан. Чем могу помочь?")


@dp.message(Command('end'))
async def end(message: types.Message):
    requests.post('https://jasik.alwaysdata.net/clear-ig-session',
                  json={"contactId": message.from_user.id})
    await message.answer("Сессия завершена. Для начала новой сессии напишите /start")
    await message.bot.close()


@dp.message()
async def message_handler(message: types.Message):
    req = {
        "message": message.text,
        "contactId": message.from_user.id
    }
    res = requests.post('https://jasik.alwaysdata.net/qazai', json=req)
    await message.answer(res.json()['message'])


async def main():
    bot = Bot(token='6836762747:AAHnwXUj_QWwJTnpVmpq-kw6xROpvLVCnY0')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
