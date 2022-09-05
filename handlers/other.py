from aiogram import types
from aiogram import Dispatcher
import json
import string

from create_bot import dp


# @dp.message_handler()
async def echo_send(message: types.Message):
    '''Функция вычисления мата.'''
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
            .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены!')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    '''Регистрация хендлеров.'''
    dp.register_message_handler(echo_send)
