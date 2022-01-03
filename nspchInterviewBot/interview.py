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
    stateShowPresentation = State()
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
        await cmd_start_job_interview(message)
    async with state.proxy() as data:
        data['social_network'] = message.text
        data['is_streamer'] = "Нет"
        data['is_pusher'] = "Нет"
        data['has_team'] = "Нет"
        data['mutual_subscriptions'] = "Нет"

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
async def process_streamer_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.yes_answ:
        await Form.stateViewersQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.lt_10_answ, Answers.in_10_20_answ,
                Answers.in_20_50_answ, Answers.gt_50_answ,
                Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('007'), 'rb'),
                             caption="Сколько зрителей вас смотрят (в среднем) ?",
                             reply_markup=markup)
    else:
        await Form.stateMutualSubscriptionsQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('010'), 'rb'),
                             caption="Делаете ли вы взаимные подписки для " +
                             "взаимного увеличения подписчиков?",
                             reply_markup=markup)
    async with state.proxy() as data:
        data['is_streamer'] = message.text
 
@dp.message_handler(state=Form.stateViewersQ)
async def process_viewers_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    await Form.stateStreamTimeQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.time_00_06_answ, Answers.time_06_12_answ,
            Answers.time_12_18_answ, Answers.time_18_24_answ,
            Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('008'), 'rb'),
                         caption="В какое время вы ведёте стримы?",
                         reply_markup=markup)
    async with state.proxy() as data:
        data['viewers'] = message.text

@dp.message_handler(state=Form.stateStreamTimeQ)
async def process_stream_time_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    await Form.stateStreamerTeamQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('009'), 'rb'),
                         caption="Есть ли у вас своя команда (модераторов, пушеров) ?",
                         reply_markup=markup)
    async with state.proxy() as data:
        data['streams_time'] = message.text

@dp.message_handler(state=Form.stateStreamerTeamQ)
async def process_streamer_team_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    await cmd_start_marathon(message)
    async with state.proxy() as data:
        data['has_team'] = message.text

@dp.message_handler(state=Form.stateMutualSubscriptionsQ)
async def process_mutual_subscriptions_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.yes_answ:
        await Form.statePusherTeamQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('011'), 'rb'),
                             caption="Есть ли у вас своя команда?",
                             reply_markup=markup)
    else:
        await cmd_start_job_interview(message)
    async with state.proxy() as data:
        data['mutual_subscriptions'] = message.text

@dp.message_handler(state=Form.statePusherTeamQ)
async def process_pusher_team_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.yes_answ:
        await cmd_start_marathon(message)
        async with state.proxy() as data:
            data['is_pusher'] = "Да"
            data['has_team'] = message.text
    else:
        await cmd_start_job_interview(message)

async def cmd_start_marathon(message: types.Message):
    if await check_reset(message): return
    await Form.stateWantTikTokQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.yes_answ, Answers.no_answ, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('012'), 'rb'),
                         caption="Отлично, мы запускаем марафон 24/7 стрим-трансляции, " +
            "команда стримеров/модераторов передаёт актив по эстафете друг другу.\n" +
            "Хотели бы вы поучаствовать в таком широкомасштабном проекте?",
            reply_markup=markup)

@dp.message_handler(state=Form.stateWantTikTokQ)
async def process_want_tiktok_q(message: types.Message):
    if await check_reset(message): return
    if message.text == Answers.yes_answ:
        await Form.stateTikTokAgeQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.age_lt_16_answ, Answers.age_gt_16_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('013'), 'rb'),
                             caption="Ваш возраст?", reply_markup=markup)
    else:
        await cmd_good_luck_end()

@dp.message_handler(state=Form.stateTikTokAgeQ)
async def process_tiktok_age_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    if message.text == Answers.age_gt_16_answ:
        await Form.stateTikTokScreenshotQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('015'), 'rb'),
                             caption="Отправьте нам скриншот своего аккаунта " +
                             "для подтверждения.", reply_markup=markup)
    else:
        await cmd_bring_parents(message)
    async with state.proxy() as data:
        data['age'] = message.text

# TODO: process/filter/check screenshot (not message)
@dp.message_handler(state=Form.stateTikTokScreenshotQ)
async def process_tiktok_screenshot_q(message: types.Message, state: FSMContext):
    if await check_reset(message): return
    await bot.send_voice(message.chat.id, open(get_voice('016'), 'rb'),
                         caption="Сейчас мы дорабатываем алгоритмы, проводим " +
        "финальные тесты.\nКак только мы завершим набор и будет всё готово, мы " +
        "свяжемся с вами!\nНам нужна команда (желательно, в идеале, 12 модераторов " +
        "на каждого стримера).\n\nУ нас есть ваш телефонный номер и мы Вас " +
        "пригласим перед запуском Проекта на видеоконференцию в Telegram.\n" +
        "Пожелание: за это время постараться набрать модераторов.",
         reply_markup=types.ReplyKeyboardRemove())
    await cmd_send_tiktok_data()
    await Form.stateEnd.set()
    await bot.send_voice(message.chat.id, open(get_voice('017'), 'rb'),
                         caption="Данные переданы! Ждите, с Вами свяжутся!",
         reply_markup=types.ReplyKeyboardRemove())

# TODO: send data
async def cmd_send_tiktok_data(message: types.Message):
    await message.reply(italic("Пересылка данных стримера, пушера Виктору"),
                        parse_mode=ParseMode.MARKDOWN)

async def cmd_start_job_interview(message: types.Message):
    if await check_reset(message): return
    await Form.stateShowPresentation.set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.i_looked_video_answ, Answers.back_to_begin_answ)

    video_path = 'data/Greeting/Greeting-'+str(random.randint(0,3))+'.mp4'
    await bot.send_video(message.chat.id, open(video_path, 'rb'),
                         caption="Просмотрите ознакомительную видеопрезентацию.",
                         reply_markup=markup)

@dp.message_handler(lambda message: message.text not in [
    Answers.i_looked_video_answ, Answers.back_to_begin_answ], state=Form.stateShowPresentation)
async def process_begin_job_interview_invalid(message: types.Message):
    return await message.reply("Выберите вариант с экранной клавиатуры.")

@dp.message_handler(state=Form.stateShowPresentation)
async def process_begin_job_interview(message: types.Message):
    if await check_reset(message): return
    if message.text == Answers.i_looked_video_answ:
        await Form.stateReadyToWorkQ.set()
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

@dp.message_handler(state=Form.stateReadyToWorkQ)
async def process_ready_to_work_q(message: types.Message):
    if await check_reset(message): return
    if message.text == Answers.ready_answ:
        await Form.stateWorkerAgeQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.age_lt_16_answ, Answers.age_gt_16_answ, Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('013'), 'rb'),
                             caption="Ваш возраст?", reply_markup=markup)
    else:
        cmd_good_luck_end(message)

@dp.message_handler(state=Form.stateWorkerAgeQ)
async def process_worker_age_q(message: types.Message):
    if await check_reset(message): return
    if message.text == Answers.age_gt_16_answ:
        await Form.stateTimeZoneQ.set()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add(Answers.back_to_begin_answ)
        await bot.send_voice(message.chat.id, open(get_voice('019'), 'rb'),
                             caption="Какой у вас часовой пояс?", reply_markup=markup)
    else:
        await cmd_bring_parents(message)
    async with state.proxy() as data:
        data['age'] = message.text

@dp.message_handler(state=Form.stateTimeZoneQ)
async def process_timezone_q(message: types.Message):
    if await check_reset(message): return
    await Form.stateProfessionQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.prof_it_answ, Answers.prof_jurist_answ,
            Answers.prof_mark_answ, Answers.prof_book_keeper_answ,
            Answers.prof_smm_answ, Answers.prof_journalist_answ,
            Answers.prof_video_editor_answ, Answers.prof_speaker_answ,
            Answers.prof_teacher_answ, Ansers.other, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('020'), 'rb'),
                         caption="Основной вид деятельности?", reply_markup=markup)
    async with state.proxy() as data:
        data['timezone'] = message.text

@dp.message_handler(state=Form.stateProfessionQ)
async def process_profession_q(message: types.Message):
    if await check_reset(message): return
    await Form.stateExpectedSalaryQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.salary_1536_answ, Answers.salary_3840_answ,
            Answers.salary_5952_answ, Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('021'), 'rb'),
        caption="Мы являемся ПрофСоюзом/Государственными Представителями..!!!\n" +
        "И у нас существует Проф.Союзный взнос 1700, а это 0,34% от з/п.\n" +
        "ВАШЕ ЛИЧНОЕ ПРЕДСТАВЛЕНИЕ О ДОСТОЙНОЙ ЗАРПЛАТЕ..?!?!?!\n\n" +
        "Сколько бы вы хотели зарабатывать..???",
        reply_markup=markup)
    async with state.proxy() as data:
        data['profession'] = message.text

@dp.message_handler(state=Form.stateExpectedSalaryQ)
async def process_expected_salary_q(message: types.Message):
    if await check_reset(message): return
    await Form.stateExpectedWorkHoursQ.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(Answers.hours_1_answ, Answers.hours_2_answ,
    markup.add(Answers.hours_4_answ, Answers.hours_8_answ,
    markup.add(Answers.hours_16_answ, Answers.hours_20_answ,
               Answers.back_to_begin_answ)
    await bot.send_voice(message.chat.id, open(get_voice('022'), 'rb'),
        caption="Сколько часов в день инвестируя, вы хотели бы у Нас трудиться..???",
        reply_markup=markup)
    async with state.proxy() as data:
        data['expected_salary'] = message.text

@dp.message_handler(state=Form.stateExpectedWorkHoursQ)
async def process_expected_work_hours_q(message: types.Message):
    if await check_reset(message): return
    await Form.stateIURSSContribution.set()

async def cmd_bring_parents(message: types.Message):
    if await check_reset(message): return
    await Form.stateEnd.set()
    await bot.send_voice(message.chat.id, open(get_voice('014'), 'rb'),
                         caption="Участники младше 16 лет допускаются только с согласия " +
                         "родителей.\nПожалуйста, приходите на собеседование с родителями!\n" +
                         "Благодарю за беседу. До встречи!",
                         reply_markup=types.ReplyKeyboardRemove())

async def cmd_good_luck_end(message: types.Message):
    if await check_reset(message): return
    await Form.stateEnd.set()
    await bot.send_voice(message.chat.id, open(get_voice('024'), 'rb'),
                         caption="В С Е Г О   Х О Р О Ш Е Г О !!!",
                         reply_markup=types.ReplyKeyboardRemove())
   
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
