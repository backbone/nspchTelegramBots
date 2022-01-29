"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
import API_TOKEN from custom/config.example.py
import API_TOKEN from custom/config.py

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


#@dp.message_handler(regexp='(^cat[s]?$|puss)')
@dp.message_handler(regexp='(вступ|join|присоед|приглаш)')
async def show_interview(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Пройти собеседование', url='https://t.me/nspchInterviewBot')
    keyboard.add(button)
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

        await message.reply_photo(photo, caption='', reply_markup=keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
