import requests
from bs4 import BeautifulSoup
from aiogram import executor
from create_bot import dp, bot
from create_bot import ADMIN_ID

url = "https:\u002F\u002Fsso.dzen.ru\u002Finstall?uuid=c7ce5f75-f2b9-4546-aec6-e47d73384981"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1107 Yowser/2.5 Safari/537.36"}
a = requests.get(url, headers=headers).text
soup = BeautifulSoup(a, 'lxml')
a = soup.find("div", class_="card-news__tabPane-3_ card-news__active-2u").find_all('span')


async def send_to_admin(message):
    await bot.send_message(ADMIN_ID, 'Бот запущен.')


@dp.message_handler(commands=["start"])
async def dzen_news(message):
    await message.answer("Важные новости к этому моменту:\n")
    text = "\n".join(["⚡ " + i.text for i in a])
    await message.answer(text)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=send_to_admin)
