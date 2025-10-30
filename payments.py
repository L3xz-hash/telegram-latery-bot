from yookassa import Payment, Configuration
import uuid
import time
import random
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from texts import *
import config as cfg
from randomizer import randomize


bot = TeleBot(token=cfg.api_telegram_bot_token)
data_directory_path = f'Данные/part_data.txt'


Configuration.account_id = cfg.yookassa_shop_id
Configuration.secret_key = cfg.yookassa_api_key


def create_and_check_card_payment(call: any, price: str = '500.00', name: str = 'Оплата участия'):
    # Создаем платеж
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": name
    }, uuid.uuid4())
    
    print(payment)
    print('--------------')

    yookassa_url = payment.confirmation.confirmation_url

    user_id = call.from_user.id
    user_chat_id = call.message.chat.id
    user_nikname = call.from_user.username

    pay_yookassa_inline_keyboard = InlineKeyboardMarkup(row_width=1)
    pay_yookassa_inline_keyboard.add(InlineKeyboardButton(text='Оплатить сейчас ✔️', url=yookassa_url))

    bot.send_message(chat_id=call.message.chat.id, text=f'📥 Принимает оплату через:\n- Банковские карты\n- СБП\n- MirPay\n- SberPay\n- Наличными в банкоматах\n- Оплату через приложение с телефона\n\nСсылка на оплату 👇🏻', reply_markup=pay_yookassa_inline_keyboard)

    # Проверяем статус платежа несколько раз с интервалами
    for i in range(120):
        time.sleep(5)
        
        # Важно: получаем актуальную информацию о платеже
        payment = Payment.find_one(payment.id)
        
        # print(payment.paid)
        # print(payment.status)
        
        if payment.status == 'succeeded':
            # Тут Сохранение
            user_gift_id = randomize(chat_id=user_chat_id)
            with open(data_directory_path, 'w', encoding='utf-8') as joiners_data_file:
                joiners_data_file.write(f'Клиент @{user_nikname} | Chat ID - {user_chat_id} | ID - {user_id} | Сумма {price} | Номер билета - {user_gift_id}\n')
                joiners_data_file.close()
            bot.send_message(chat_id=call.message.chat.id, text=seccusfully_accepted_latery_invite_text + f'\n\nВаш номер билета - {user_gift_id}')

            print('Оплачено')
            # bot.send_message(chat_id=cfg.owners_id['Стас'], text=f'Уважаемый Станислав Олегович, какой-то @{call.from_user.username} (c ID - {call.from_user.id}) Оплатил участие "{name}" ')
            # bot.send_message(chat_id=cfg.owners_id['Лысый'], text=f'Уважаемый и всеми любимый Лысый (Артём), какой-то нищеброд @{call.from_user.username} (c ID - {call.from_user.id}) Оплатил участие в латерее "{name}" ')
            # bot.send_message(chat_id=cfg.owners_id['Стас'], text=f'Уважаемый Данил (Комарик),  сегодня какой-то нищеброд под ником @{call.from_user.username} (c ID - {call.from_user.id}) Оплатил участие в ебучей латерее "{name}" ')


            return True  # Выходим из функции, если оплата прошла
        

    if payment.status != 'succeeded':
        bot.send_message(chat_id=call.message.chat.id, text='Оплата не прошла, попробуйте снова')
        # print('Ожидание оплаты...')


