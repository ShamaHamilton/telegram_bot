from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    '''Получаем ID текущего модератора.'''
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Чего желаете, хозяин?',
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def cm_start(message: types.Message):
    '''Начало диалога загрузки нового пункта меню.'''
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')


async def cancel_handler(message: types.Message, state: FSMContext):
    '''Выход из состояний.'''
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


async def load_photo(message: types.Message, state: FSMContext):
    '''Ловим первый ответ (photo) и пишем в словарь.'''
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введите название')


async def load_name(message: types.Message, state: FSMContext):
    '''Ловим второй ответ (name).'''
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание')


async def load_description(message: types.Message, state: FSMContext):
    '''Ловим третий ответ (description).'''
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажите цену')


async def load_price(message: types.Message, state: FSMContext):
    '''Ловим последний ответ (price) и используем полученные данные.'''
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    '''Регистриреум хендлеры админки.'''
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler,
                                Text(equals='отмена', ignore_case=True),
                                state="*")
    dp.register_message_handler(load_photo, content_types=['photo'],
                                state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'],
                                is_chat_admin=True)
