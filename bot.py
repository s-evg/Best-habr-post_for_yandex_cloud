import json
import os
from aiogram import Bot, Dispatcher, types
TOKEN = os.getenv("TOKEN")

import pars


HELP = """
Привет!
Я покажу новые посты по твоим интересам на Хабре.
/new\_post — новые посты
/mess — инфа о сообщении
"""


bot = Bot(TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.answer(HELP)


@dp.message_handler(commands=['mess'])
async def mess(message: types.Message):
    await message.answer(message)


@dp.message_handler(commands=['new_post'])
async def new_post_command(message: types.Message):
    await message.reply("Минуточку, собираю информацию ⏱...")
    posts = pars.new_post()
    await message.answer('\n'.join(posts))


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


async def process_event(event, dp: Dispatcher):
    update = json.loads(event['body'])
    Bot.set_current(dp.bot)
    update = types.Update.to_object(update)
    await dp.process_update(update)


async def main(event, context):
    print(event)
    await process_event(event, dp)
    return {'statusCode': 200, 'body': 'ok'}
