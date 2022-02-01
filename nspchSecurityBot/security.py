"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from custom.config_example import *
from custom.config import *

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

chat_ids = CHNV_CHAT_IDS


#@dp.message_handler(commands=['start', 'help'])
#async def send_welcome(message: types.Message):
#    """
#    This handler will be called when user sends `/start` or `/help` command
#    """
#    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


#@dp.message_handler(regexp='(^cat[s]?$|puss)')
#@dp.message_handler(regexp='(вступ|join|присоед|приглаш)')
#async def show_interview(message: types.Message):
#    keyboard = types.InlineKeyboardMarkup()
#    button = types.InlineKeyboardButton('Пройти собеседование', url='https://t.me/nspchInterviewBot')
#    keyboard.add(button)
#    with open('data/Interview-1.webp', 'rb') as photo:
#        '''
#        # Old fashioned way:
#        await bot.send_photo(
#            message.chat.id,
#            photo,
#            caption='СОБЕСЕДОВАНИЕ',
#            reply_to_message_id=message.message_id,
#        )
#        '''
#
#        await message.reply_photo(photo, caption='', reply_markup=keyboard)
#

#@dp.message_handler()
#async def echo(message: types.Message):
#    # old style:
#    # await bot.send_message(message.chat.id, message.text)
#
#    await message.answer(message.text)

#async def posting(sleep_for, queue):
#    while True:
#        await show_interview()
#        time.sleep(10)

async def show_interview(sleep_for, queue):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Пройти собеседование', url='https://t.me/nspchInterviewBot')
    keyboard.add(button)
    while True:
        await asyncio.sleep(sleep_for)
        now = datetime.utcnow()
        for id in chat_ids:
            with open('data/Interview-1.webp', 'rb') as photo:
                '''
                # Old fashioned way:
                await bot.send_photo(
                    message.chat.id,
                    photo,
                    caption='СОБЕСЕДОВАНИЕ',
                    reply_to_message_id=message.message_id,
                )
                '''
                await bot.send_photo(id, photo, caption='', reply_markup=keyboard, disable_notification=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    loop.create_task(show_interview(POST_TIMEOUT, queue))
    executor.start_polling(dp, skip_updates=True)
