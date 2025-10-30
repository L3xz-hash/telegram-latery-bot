# ======================== #
# ======================== #
# # # # # # # # # # # # # # #
#        Клавиатуры
# # # # # # # # # # # # # # # 
# ======================== #
# ======================== #


# ----------------------

from telebot.types import ( InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton )


main_pinned_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_pinned_keyboard.add(KeyboardButton(text='💵 Оплатить участие'))
main_pinned_keyboard.add(KeyboardButton(text='💱 Проверить участие'))


join_latery_inline_keyboard = InlineKeyboardMarkup(row_width=2)
join_latery_inline_keyboard.add(InlineKeyboardButton(text='Да, готов ! 🤑', callback_data='ready_payment'))

payments_inline_keyboard = InlineKeyboardMarkup(row_width=1)
payments_inline_keyboard.add(InlineKeyboardButton(text='Оплата картой 💳', callback_data='card_pay'))
payments_inline_keyboard.add(InlineKeyboardButton(text='Оплата телеграм-звёздами ⭐️', callback_data='stars_pay'))
payments_inline_keyboard.add(InlineKeyboardButton(text='Оплата криптой 🪙', callback_data='crypto_pay'))