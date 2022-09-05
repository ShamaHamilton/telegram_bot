'''Файл создания экземпляра бота.'''
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

# Создаем экземпляр бота
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
