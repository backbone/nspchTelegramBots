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
from aiogram.utils.markdown import bold, code, italic, text

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
    back_to_begin_answ = "Вернуться к началу беседы"
    i_looked_video_answ = "Я просмотрел презентацию"
    i_opened_phone_answ = "Я открыл номер телефона"
    yes_answ = "Да"
    no_answ = "Нет"
    ready_answ = "Согласен"
    refuse_answ = "Отказываюсь"
    soc_tiktok_answ = "Tik-Tok"
    soc_telegram_answ = "Telegram"
    soc_vkontakte_answ = "Vkontakte"
    soc_instagram_answ = "Instagram"
    lt_10_answ = "<10"
    in_10_20_answ = "10-20"
    in_20_50_answ = "20-50"
    gt_50_answ = ">50"
    time_00_06_answ = "0:00-6:00"
    time_06_12_answ = "6:00-12:00"
    time_12_18_answ = "12:00-18:00"
    time_18_24_answ = "18:00-24:00"
    age_gt_16_answ = "есть 16 лет"
    age_lt_16_answ = "младше 16 лет"
    prof_it_answ = "IT/Dev/Web"
    prof_jurist_answ = "Юрист"
    prof_mark_answ = "Маркетолог"
    prof_book_keeper_answ = "Бухгалтер"
    prof_smm_answ = "SMM-специалист"
    prof_journalist_answ = "Журналист"
    prof_video_editor_answ = "Аудио/Видео-монтаж"
    prof_speaker_answ = "Диктор"
    prof_teacher_answ = "Педагог"
    salary_1536_answ = "1536€ / мес. (МРОТ 9.6€/ч * 8ч. * 20раб.дн.)"
    salary_3840_answ = "3840€ / мес. (МРОТ 9.6€/ч * 20ч. * 20раб.дн.)"
    salary_5952_answ = "5952€ / мес. (МРОТ 9.6€/ч * 20ч. * 31раб.дн.)"
    hours_1_answ = "1ч./день"
    hours_2_answ = "2ч./день"
    hours_4_answ = "4ч./день"
    hours_8_answ = "8ч./день"
    hours_16_answ = "16ч./день"
    hours_20_answ = "20ч./день"
    other_answ = "Прочее"

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

def get_voice(s="001"):
    h=datetime.datetime.now().hour+1
    hs=str(h)
    if h < 10:
        hs='0'+hs
    return 'data/voice/chnv-001/'+hs+'/'+s+'.mp3'

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.stateSocialNetworkQ.set()
    await bot.send_voice(message.chat.id, open(get_voice('001'), 'rb'),
                         caption="Рады поприветствовать в ПрофСоюзе Правозащитников "+
                                 "без границ!\nПрофсоюз является экстерриториальным " +
                                 "работодателем с профсоюзным взносом  в размере 0.34% от ЗП.")
    await process_closed_number(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.soc_tiktok_answ, Answers.soc_telegram_answ,
               Answers.soc_vkontakte_answ, Answers.soc_instagram_answ,
               Answers.other_answ, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('004'), 'rb'),
                         caption="Где вы получили информацию о нас?",
                         reply_markup=markup)

# TODO: G O D  E Y E ===
@dp.message_handler(state=Form.stateClosedNumber)
async def process_closed_number(message: types.Message):
    await message.reply(italic("// Глаз Бога пока не работает, не вижу, открыт ли номер"),
                        parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(text=[Answers.back_to_begin_answ])
async def check_reset(message: types.Message):
    if message.text == Answers.back_to_begin_answ:
        await cmd_start(message)
        return True
    return False

@dp.message_handler(state=Form.stateSocialNetworkQ)
async def process_social_network_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.soc_tiktok_answ:
        await Form.stateTikTokCodeQ.set()
        await bot.send_voice(message.chat.id, open(get_voice('005'), 'rb'),
                             caption="По коду какой страницы вы пришли?\n"+
                                     "(Это нам нужно для статистики)",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await Form.stateReadyToWorkQ.set()
        await cmd_start_job_interview(message)
    async with state.proxy() as data:
        data['social_network'] = message.text

@dp.message_handler(state=Form.stateTikTokCodeQ)
async def process_tiktok_code_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    await Form.stateStreamerQ.set()
    async with state.proxy() as data:
        data['tiktok_code'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('006'), 'rb'),
                         caption="Ведёте ли вы стримы?",
                         reply_markup=markup)

@dp.message_handler(state=Form.stateStreamerQ)
async def process_tiktok_code_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.yes_answ:
        await Form.stateMutualSubscriptionsQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.lt_10_answ, Answers.in_10_20_answ,
                Answers.in_20_50_answ, Answers.gt_50_answ,
                Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('007'), 'rb'),
                             caption="Сколько зрителей вас смотрят (в среднем) ?",
                             reply_markup=markup)
    else:
        await Form.stateViewersQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('010'), 'rb'),
                             caption="Делаете ли вы взаимные подписки для " +
                             "взаимного увеличения подписчиков?",
                             reply_markup=markup)
    async with state.proxy() as data:
        data['is_streamer'] = message.text
 
async def cmd_start_job_interview(message: types.Message):
    if await check_reset(message): return
    await Form.stateReadyToWorkQ.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.i_looked_video_answ, Answers.back_to_begin_answ)

    video_path = 'data/Greeting/Greeting-'+str(random.randint(0,3))+'.mp4'
    await bot.send_video(message.chat.id, open(video_path, 'rb'),
                         caption="Просмотрите ознакомительную видеопрезентацию.",
                         reply_markup=markup)

@dp.message_handler(lambda message: message.text not in [
    Answers.i_looked_video_answ, Answers.back_to_begin_answ], state=Form.stateReadyToWorkQ)
async def process_begin_job_interview_invalid(message: types.Message):
    return await message.reply("Выберите вариант с экранной клавиатуры.")

@dp.message_handler(state=Form.stateReadyToWorkQ)
async def process_begin_job_interview(message: types.Message):
    if await check_reset(message): return
    if message.text == Answers.i_looked_video_answ:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.ready_answ, Answers.refuse_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('018'), 'rb'),
                             caption="Мы трудоустраиваем вас в нашем Проекте и " +
            "предоставляем вам 24/7 сопровождение командой поддержки до успешного " +
            "состояния, даём вам базу знаний и наработок, выдаём инструменты и шаблоны, " +
            "используя которые совершенно любой человек может хоть завтра начать " +
            "зарабатывать в интернет.\nЕсли у вас нет своего контента для стримов, " +
            "мы предоставим вам контент (с или без вашего участия).\nМы предлагаем " +
            "вам з/п в размере Евр. МРОТ.\nСтоимость всех наших инструментов и услуг " +
            "входит в единовременный Проф.взнос 0,34% от буд. з/п = 1700 ббр.\nВы " +
            "получаете обучение правозащитной деятельности, журналистике, видео-монтажу, " +
            "развиваетесь в IT-сфере, оттачиваете разговорную речь и повышаете " +
            "дикторские способности.\nТрудовой договор заключается после 2-х нед. исп. срока.",
                             reply_markup=markup)
   
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
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
