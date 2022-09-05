from aiogram import types
from aiogram import Dispatcher

from create_bot import dp, bot


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    '''Команды "/start" и "/help".'''
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита')
        await message.delete()
    except:
        await message.reply(
            'Общение с ботом через ЛС, \
            напишите ему:\nhttps://t.me/Test_Master_PizzaBot'
        )


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    '''Команда "/Режим_работы".'''
    await bot.send_message(
        message.from_user.id,
        'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00'
    )


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    '''Команда "/Расположение".'''
    await bot.send_message(
        message.from_user.id,
        'ул. 1-я Синичкина 3к1'
    )


def register_handlers_client(dp: Dispatcher):
    '''Регистрация хендлеров.'''
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])