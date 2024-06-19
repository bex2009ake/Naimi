from aiogram import Bot, Dispatcher, types, executor
from random import randint
import requests



API_TOKEN = '7090835491:AAGCExep9lTwb5q41TcfSF9JzfIbE0j1TSs'
DB_URL = 'http://127.0.0.1:8000/api/code/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def start_func(msg: types.Message):
    kb = [
        [types.KeyboardButton(text="Дать телефон номер 📞", request_contact=True)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await msg.answer(f'Hello {msg.from_user.username}, its Naimi bot !!!', reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_func(msg: types.Message):
    phone = msg.contact.phone_number
    num = randint(100000, 999999)

    requests.post(url='http://127.0.0.1:8000/api/code/', data={
        'phone': phone,
        'code': num,
        'city': 1
    })

    await msg.answer(f'Ваш код {num}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)


# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NjIwMzYwLCJpYXQiOjE3MTg3NTYzNjAsImp0aSI6IjQzZjQwMmVlYjg0ZjRjNWI5ZGI5NGEwNDZiNjExNzBlIiwidXNlcl9pZCI6MTB9.dr9drhn4fwgM1KphMz7kjD1sQGBm3QZRh8a6fUB7HAA",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDA1MjM2MCwiaWF0IjoxNzE4NzU2MzYwLCJqdGkiOiI3ZjQ2N2VhNWFlNTA0ODJkYTViNjMwODU0NTliZjE2ZiIsInVzZXJfaWQiOjEwfQ.k7pt_89voRLWcja6XfJx-UfROZZEx_inqlGVVV_XGg8"
# }