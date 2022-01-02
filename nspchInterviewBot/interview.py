import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import random, datetime

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    stateBegin = State()
    stateClosedNumber = State()
    stateSocialNetworkQ = State()
    stateTikTokCodeQ = State()
    stateStreamerQ = State()
    stateViewersQ = State()
    stateStreamTimeQ = State()
    stateStreamerTeamQ = State()
    stateMutualSubscriptionsQ = State()
    statePusherTeamQ = State()
    stateWantTikTokQ = State()
    stateTikTokAgeQ = State()
    stateTikTokScreenshotQ = State()
    stateReadyToWorkQ = State()
    stateWorkerAgeQ = State()
    stateTimeZoneQ = State()
    stateProfessionQ = State()
    stateExpectedSalaryQ = State()
    stateExpectedWorkHoursQ = State()
    stateIURSSContribution = State()
    stateEnd = State()

# Answers
class Answers():
    back_to_gegin_txt = "Вернуться к началу беседы"
    i_looked_video_txt = "Я просмотрел презентацию"

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_voice(message.chat.id, open(get_voice('001'), 'rb'),
                         caption="Рады поприветствовать в ПрофСоюзе Правозащитников \
без границ!\nПрофсоюз является экстерриториальным работодателем с профсоюзным взносом \
в размере 0.34% от ЗП.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.i_looked_video_txt, Answers.back_to_gegin_txt)

    video_path = 'data/Greeting/Greeting-'+str(random.randint(0,3))+'.mp4'
    await bot.send_video(message.chat.id, open(video_path, 'rb'),
                         caption="Просмотрите ознакомительную видеопрезентацию.",
                         reply_markup=markup)


    await Form.stateBegin.set()

def get_voice(s="001"):
    return 'data/voice/chnv-001/'+str(datetime.datetime.now().hour+1)+'/'+s+'.mp3'

async def check_reset(message):
    if message.text == Answers.back_to_gegin_txt:
        await Form.stateBegin.set()
        await cmd_start(message)

@dp.message_handler(lambda message: message.text not in [
    Answers.i_looked_video_txt, Answers.back_to_gegin_txt], state=Form.stateBegin)
async def process_begin_invalid(message: types.Message):
    return await message.reply("Выберите вариант с экранной клавиатуры.")

@dp.message_handler(state=Form.stateBegin)
async def process_begin(message: types.Message):
    await check_reset(message)
    if message.text == Answers.i_looked_video_txt:
        markup = types.ReplyKeyboardRemove()
        #await process_closed_number(message)
        await bot.send_voice(message.chat.id, open(get_voice('004'), 'rb'),
                             caption="Где вы получили информацию о нас?",
                             reply_markup=markup)
        await Form.stateSocialNetworkQ.set()

# TODO: G O D  E Y E ===
#@dp.message_handler(state=Form.stateClosedNumber)
#async def process_closed_number(message: types.Message):
#    if check_reset(message): return
#    await message.reply("Глаз Бога пока не работает (не вижу, открыт ли номер)...")

#@dp.message_handler(state=Form.stateSocialNetworkQ)
#async def process_social_network_q(message: types.Message):

#------------------------------------------------------------------------------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================

#@dp.message_handler(state=Form.name)
#async def process_name(message: types.Message, state: FSMContext):
#    """
#    Process user name
#    """
#    async with state.proxy() as data:
#        data['name'] = message.text
#
#    await Form.next()
#    await message.reply("How old are you?")
#
#
# Check age. Age gotta be digit
#@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
#async def process_age_invalid(message: types.Message):
#    """
#    If age is invalid
#    """
#    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


#@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
#async def process_age(message: types.Message, state: FSMContext):
#    # Update state and data
#    await Form.next()
#    await state.update_data(age=int(message.text))
#
#    # Configure ReplyKeyboardMarkup
#    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#    markup.add("Male", "Female")
#    markup.add("Other")
#
#    await message.reply("What is your gender?", reply_markup=markup)


#@dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
#async def process_gender_invalid(message: types.Message):
#    """
#    In this example gender has to be one of: Male, Female, Other.
#    """
#    return await message.reply("Bad gender name. Choose your gender from the keyboard.")
#
#
#@dp.message_handler(state=Form.gender)
#async def process_gender(message: types.Message, state: FSMContext):
#    async with state.proxy() as data:
#        data['gender'] = message.text
#
#        # Remove keyboard
#        markup = types.ReplyKeyboardRemove()
#
#        # And send message
#        await bot.send_message(
#            message.chat.id,
#            md.text(
#                md.text('Hi! Nice to meet you,', md.bold(data['name'])),
#                md.text('Age:', md.code(data['age'])),
#                md.text('Gender:', data['gender']),
#                sep='\n',
#            ),
#            reply_markup=markup,
#            parse_mode=ParseMode.MARKDOWN,
#        )
#
#    # Finish conversation
#    await state.finish()
