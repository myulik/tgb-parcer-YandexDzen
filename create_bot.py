import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')


loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)