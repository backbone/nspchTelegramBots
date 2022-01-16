from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor


BOT_TOKEN = ''
PAYMENTS_PROVIDER_TOKEN = ''

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

# Setup prices
prices = [
    types.LabeledPrice(label='ПрофСоюзный взнос 0,34% от З.П.', amount=170000),
]

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id,
                           " Используйте команду /buy для оплаты ПрофСоюзного взноса, "
                           " команду /terms для ознакомления с условиями и положениями.")


@dp.message_handler(commands=['terms'])
async def cmd_terms(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Благодарим за участие в нашей команде:\n'
                           '1. ПрофСоюзный взнос является единоразовым. По окончании'
                           ' испытательного срока заключается договор найма.\n'
                           '2. Испытательный срок длится 2 (две) недели. В течение'
                           ' этого времени от вас ожидается полная выкладка и'
                           ' участие.\n'
                           '3. Успешным завершением испытательного срока'
                           ' считается выполнение следующих условий:\n'
                           '  а) действие по алгоритму (учреждение одного TikTok-аккаунта / сут. и т.п.);\n'
                           '  б) круговая порука 12+1;\n'
                           '  в) отсутствие правонарушений в области уголовного права;\n'
                           '  г) исполнение 29.1 ВДПЧ.\n')

@dp.message_handler(commands=['buy'])
async def cmd_buy(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Оплатите ПрофСоюзный взнос 0,34% от З.П. = 1700 ббр '
                           'и получите готовые инструменты для заработка в '
                           'Internet, обучение, правовую и техническую поддержку! '
                           'Вступите и участвуйте вместе с нами! '
                           'Тестовая карта: `4242 4242 4242 4242`:', parse_mode='Markdown')
    await bot.send_invoice(message.chat.id, title="ПрофСоюзный взнос 0,34% от З.П.",
                           description="Это стоимость всех наших инструментов "
                           'для заработка, включая обучение правозащите, '
                           'журналистике, видео-монтажу, IT, дикторские '
                           'навыки.',
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url='https://telegra.ph//file/a5d8b0d80d93a2875a781.jpg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='union-fee',
                           payload='Заработок, правозащита, успех')

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Чужаки пытались украсть CVV-код вашей карты,"
                                                      " но мы успешно предотвратили атаку,"
                                                      " попробуйте оплатить взнос спустя несколько минут,"
                                                      " нам нужен небольшой отдых.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Отлично! Благодарю за оплату, `{} {}`'
                           'Вы будете перенаправлены на нашего координатора,'
                           'который даст полную информацию и ответит на'
                           'ваши вопросы.',
                           parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
