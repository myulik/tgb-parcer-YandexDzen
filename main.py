#!/home//.virtualenvs//bin/python3

import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import  InputFile
import asyncio
from bs4 import BeautifulSoup
from aiogram import executor
import time
import re
import random


load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

seconds = time.time()
local_time = time.ctime(seconds)
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1107 Yowser/2.5 Safari/537.36"}

url_news = "https://sso.dzen.ru/install?uuid=c7ce5f75-f2b9-4546-aec6-e47d73384981"
url_weather = 'https://yandex.ru/pogoda/?lat=56.847977&lon=60.65871&win=557'
url_sunrise_sunset = 'https://world-weather.ru/pogoda/russia/yekaterinburg/sunrise/?ysclid=m2gtwasife232502601'

data_news = requests.get(url_news, headers=headers).text
soup_news = BeautifulSoup(data_news, 'lxml')
news = soup_news.find("ul", class_="dzen-desktop--card-news__stories-Bu").find_all('p')

rate_dollar = soup_news.find("span", class_="dzen-desktop--currency-rates__rateValue-2X")
rate_dollar = "\n\nКурс доллара - " + rate_dollar.text

data_weather = requests.get(url_weather, headers=headers).text
soup_weather = BeautifulSoup(data_weather, 'lxml')
weather = soup_weather.find("div", class_="fact__temp-wrap")
weather = re.findall('Текущая температура .*?"', str(weather))
weather = ''.join(weather)[:-1]

data_sunset = requests.get(url_sunrise_sunset, headers=headers).text
soup_sunset = BeautifulSoup(data_sunset, 'lxml')
sunset = soup_sunset.find_all("dd")
sunset = sunset[0].text + ' - ' + sunset[1].text + '\n'




if weather == '':
    weather = 'капча не пройдена'
async def send_to_admin(message):
    picture = random.choice([x for x in os.listdir("/home/myulik/Рабочий стол/Мемы")
               if os.path.isfile(os.path.join("/home/myulik/Рабочий стол/Мемы", x))])

    photo = InputFile("/home/myulik/Рабочий стол/Мемы/"+ picture)
    data = sunset + weather + rate_dollar + "\n\nВажные новости на " + str(local_time) + ":\n\n" + "\n".join(["⚡ " + i.text for i in news if len(i.text) > 10])
    await bot.send_message(ADMIN_ID, data)
    await bot.send_photo(chat_id=ADMIN_ID, photo=photo)
   # file = open('/home/myulik/Yandex.Disk/1/Daily/2025-01-27.md', 'r', encoding='utf-8')
  #  content = file.read()
  #  await bot.send_message(ADMIN_ID, content)
   # file.close()
    exit()

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=send_to_admin)
