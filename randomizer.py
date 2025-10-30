import re
import random
import time
import config as cfg

supported_ticket_symbols = ['L', 'H', 'A', 'B', 'C', 'Q', 'y', 'v', 'W', 'F', 'p', 'fa', 'ab', 'ww', 'fas', 'AqD', 'Aj', 'FKl', 'Qby', 'Qp', '<l', '>12', '443f2', 'aa', 'aa4', 'HHz', 'Za', 'Hg', 'VbA', 'm', 'MnD', 'KJa', '$KSF', ':S']

def randomize(chat_id: int, max_value: int = 1000):
    use_special_symbols = False
    string_part = ''

    random_seed_ticket_number = random.randint(100, max_value)
    symbol_1 = random.choice(supported_ticket_symbols)
    symbol_2 = random.choice(supported_ticket_symbols)

    rnd_use_spec_sym = random.randint(1, 5)
    if rnd_use_spec_sym % 2 == 0:
        use_special_symbols = True

    if use_special_symbols:
        string_part = random.choice([f'${symbol_1}-{symbol_2}', f'&^{symbol_1}-{symbol_2}', f'${symbol_1}-{symbol_2}&', f'{symbol_1}-{symbol_2}&&', f'${symbol_1}-{symbol_2}&&' f'$&{symbol_1}-{symbol_2}', f'$${symbol_1}-{symbol_2}'])
    else:
        string_part = f'{symbol_1}-{symbol_2}'

    output_hash = f'ticket_№{str(chat_id)[:-2]}-{random_seed_ticket_number}-{string_part}'

    return output_hash


def choose_winner(message: any, bot_variable: any, data_path: str, numbers_of_winners: int = 1):
    print('Латерея запущена\n')
    with open(data_path, 'r', encoding='utf-8') as data_file:
        data_text = data_file.read()


    tickets_data = re.findall(r'Клиент (@\S+) .*?Номер билета - (ticket_№\S+)', data_text)
    print(tickets_data)

    print(tickets_data[0])



    winners_tickets = list()

    bot_variable.send_message(message.chat.id, f'Через {cfg.DELAY} минут начнёться розыгрыш! ☄️')

    
    time.sleep(60* cfg.DELAY)
    
    time.sleep(1)

    bot_variable.send_message(message.chat.id, f'РОЗЫГРЫШ НАЧАТ!\nОпределяем побидителя')
    
    n_winners_count = 0
    for w in range(1, numbers_of_winners):
        # определяем победителыя
        winner = random.choice(tickets_data)
        print(f'В конкурсе, место №{w} выйграл билет {winner}')
        winners_tickets.append(winner)

        # удаляем его тикер
        tickets_data = tickets_data.replace(winner, '')

        # оповещение..
        bot_variable.send_message(message.chat.id, f'Место №{w} выйграл билет:\n{winner}')

        time.sleep(20)

        n_winners_count += 1
        
        # проверка на сообщение о следующем раунде
        if n_winners_count <= numbers_of_winners:
            bot_variable.send_message(message.chat.id, f'Определяем следующего победителя...')


        # задержка
        time.sleep(60)
    
    time.sleep(2)
    matches = re.findall(r'Клиент (@\S+) .*?Номер билета - (ticket_№\S+)', data_file)
    for user_id, ticket in matches:
        print(f'{ticket}: {user_id}')

    win_txt = '''
В розыгрыше выйграли:\n
1. 
'''
    bot_variable.send_message('')
    with open(data_path, 'rb') as data_file:
        bot_variable.send_document(message.chat.id, data_file, '- Список всех участников, кто мог выйграть')
        