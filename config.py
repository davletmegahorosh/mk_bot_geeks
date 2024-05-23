from pathlib import Path
from decouple import config
from aiogram import Bot, Dispatcher
from db.database import Database

token = config('TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
database = Database()