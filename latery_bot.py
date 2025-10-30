import os
import telebot
import threading
import random
import time

import config as cfg
from keyboards import *
from texts import *
from payments import create_and_check_card_payment
from telebot.types import LabeledPrice
from randomizer import randomize, choose_winner

# ===========>
# CASINO BOT | blyat
# ===========>


# ====> Vairables <==== #
owners_chat_id = [cfg.owners_id['Стас'], cfg.owners_id['Лысый'], cfg.owners_id['Комар']]
telegram_bot_token = cfg.api_telegram_bot_token


bot = telebot.TeleBot(token=telegram_bot_token)

# Создание файла с данными
folder_data_directory_path = f'Данные'
if not os.path.exists(folder_data_directory_path):
    os.mkdir(folder_data_directory_path)

data_directory_path = f'{folder_data_directory_path}/part_data.txt'
if os.path.exists(data_directory_path):
    # data_file = open(data_directory_path, 'wb') 
    print('(V)  Данные загружены ')
else:
    with open(data_directory_path, 'wb') as data_file:
        print('Файл с данными успешно создан')
        time.sleep(1)



ticker_price = '70'


# ====> Function\s <==== #
def check_inviting(data_file_path: str, chat_id : any):
    with open(data_file_path, 'r', encoding='utf-8') as f:
        data_file_text = f.read()
    
    if str(chat_id) in data_file_text:
        bot.send_message(chat_id, 'Вы успешно учавствуете в разогрыше')
    else:
        bot.send_message(chat_id, 'Вы пока что не учавствуете в нашем розыгрыше')


# ====> Bot logic <==== #
@bot.message_handler(commands=['start', 'restart'])
def cmd_start(message):
    bot.send_message(chat_id=message.chat.id, text=hello_text, reply_markup=main_pinned_keyboard)
    

@bot.message_handler(commands=['latery', 'join', 'get_ticket'])
def cmd_join_latery(message):
    bot.send_message(chat_id=message.chat.id, text=enjoy_information_text, reply_markup=join_latery_inline_keyboard)


@bot.message_handler(commands=['pay'])
def cmd_help(message):
    bot.send_message(message.chat.id, "Выберите удобный для вас способ оплаты 👇🏻", reply_markup=payments_inline_keyboard)

@bot.message_handler(commands=['check'])
def cmd_help(message):
    check_inviting(data_file_path=data_directory_path, chat_id=message.chat.id)

@bot.message_handler(commands=['channel'])
def cmd_help(message):
    bot.send_message(chat_id=message.chat.id, text=f'💎 Телеграм канал со всеми резульатами рогызрышей\n{cfg.channel_name}') 

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(chat_id=message.chat.id, text=help_text) 
    


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "💵 Оплатить участие":
        bot.send_message(chat_id=message.chat.id, text=enjoy_information_text, reply_markup=join_latery_inline_keyboard)
        
    if message.text == '💱 Проверить участие':
        check_inviting(data_file_path=data_directory_path, chat_id=message.chat.id)
        

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Обработка запрсоов в callback
    if call.data == "ready_payment":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id, "Выберите удобный для вас способ оплаты 👇🏻", reply_markup=payments_inline_keyboard)

    
    if call.data == 'card_pay':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        payment_thread = threading.Thread(target=create_and_check_card_payment, args=(call, ticker_price, 'Оплата участия в конкурсе',))
        payment_thread.start()
    
    if call.data == 'stars_pay':
        # create_and_check_card_payment(call=call, price='299.99', name='Оплата участия в конкурсе')
        prices = [LabeledPrice(label="Доступ", amount=int( ( int(ticker_price) // 1.78 ) + cfg.STARS_COMMISION  )  )]
        bot.send_invoice(
            chat_id=call.message.chat.id,
            title="Платный доступ",
            description="Доступ на месяц - оплата Telegram Stars",
            invoice_payload="payment_access_1m",
            provider_token="STARS",  # токен не требуется для Stars, можно оставить пустым
            currency="XTR",          # Stars
            prices=prices,
            start_parameter="access",
            need_email=False,
            need_name=False
        )


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    user_id = message.from_user.id
    user_chat_id = message.chat.id
    user_nikname = message.from_user.username

    user_gift_id = randomize(chat_id=user_chat_id)
    with open(data_directory_path, 'w', encoding='utf-8') as joiners_data_file:
        joiners_data_file.write(f'Клиент @{user_nikname} | Chat ID - {user_chat_id} | ID - {user_id} | Сумма {ticker_price} | Номер билета - {user_gift_id}\n')
        joiners_data_file.close()
    bot.send_message(chat_id=message.chat.id, text=seccusfully_accepted_latery_invite_text + f'\n\nВаш номер билета - {user_gift_id}')


# ====> Bot Start polling <==== #
if __name__ == '__main__':
    os.system('cls')
    print('Латерейный Бот запущен\n')

    bot.infinity_polling(timeout=0)