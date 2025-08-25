import os

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode


bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # если создать файл .env
# bot = Bot(token=os.getenv('you_token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) если не создавать файл .env


