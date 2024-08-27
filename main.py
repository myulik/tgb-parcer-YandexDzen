#!/home//.virtualenvs//bin/python3

import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio
from bs4 import BeautifulSoup
from aiogram import executor
import time
import re


load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

seconds = time.time()
local_time = time.ctime(seconds)
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1107 Yowser/2.5 Safari/537.36"}

url_news = "https:\u002F\u002Fsso.dzen.ru\u002Finstall?uuid=c7ce5f75-f2b9-4546-aec6-e47d73384981"
url_weather = 'https://yandex.ru/pogoda/?lat=56.847977&lon=60.65871&win=557'

data_news = requests.get(url_news, headers=headers).text
soup_news = BeautifulSoup(data_news, 'lxml')
news = soup_news.find("div", class_="dzen-desktop--card-news__tabPane-3_ dzen-desktop--card-news__active-2u").find_all('span')

rate_dollar = soup_news.find("span", class_="dzen-desktop--currency-rates__rateValue-2X")
rate_dollar = "\n\nКурс доллара - " + rate_dollar.text

data_weather = requests.get(url_weather, headers=headers).text
soup_weather = BeautifulSoup(data_weather, 'lxml')
weather = soup_weather.find("div", class_="fact__temp-wrap")
weather = re.findall('Текущая температура .*?"', str(weather))
weather = ''.join(weather)[:-1]

if weather == '':
    weather = 'капча не пройдена'
async def send_to_admin(message):
    data = weather + rate_dollar + "\n\nВажные новости на " + str(local_time) + ":\n\n" + "\n".join(["⚡ " + i.text for i in news if len(i.text) > 10])
    await bot.send_message(ADMIN_ID, data)
    exit()

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=send_to_admin)
