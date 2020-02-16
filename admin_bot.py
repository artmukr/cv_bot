from telebot import TeleBot
from bot_code import admin_code
from db_connection \
    import list_of_vacancies, serialize, show_selected_vacancies, \
    update_columns, get_list_of_columns, update_vacancy_requirements, \
    show_columns_of_vacancy, opened_vacancies, open_vacancy_db, \
    close_vacancy_db, show_selected_cvs, delete_user, show_cvs

bot = TeleBot(admin_code)


@bot.message_handler(commands=['start', 'help'])
def start(message):

    bot.reply_to(message, '_________________________commands:'
                          '_________________________\n\n'
                          '/vacancies  ___________________'
                          'returns list of all opened '
                          'vacancies\n\n'
                          '/look_at_vacancy  <vacancy name>'
                          ' _____returns specific vacancy\n\n'
                          '/update_list_of_columns  <list of columns, '
                          'separated by comma with space>'
                          '   _____________________________'
                          'replaces list of columns'
                          '\n\n'
                          '/update_vacancy  _______changes vacancy field, '
                          'you can exit from\n'
                          '____________________________________ '
                          'command with key-word "exit"\n\n'
                          '/open_vacancy <vacancy name>  _________________'
                          'opens vacancy\n\n'
                          '/close_vacancy <vacancy name>  _________________'
                          'closes vacancy'
                          '\n\n'
                          '/show_all <vacancy name> __________________'
                          'shows all applicants'
                          '\n\n'
                          '/show_one_by_one <vacancy name> ____________'
                          'returns selected\n'
                          ' _______________'
                          'vacancies one-by-one, you can exit with word exit'
                          '\n\n'
                          '/delete_by_id  <user_id> ________________deletes '
                          'user`s cv`s by id\n\n'
                          '/show_selected  <first_vacancy_id> '
                          '<second_vacancy_id>\n   ______________returns 2 '
                          'selected vacancies, needed to copy and\n '
                          '_______________________paste 2 selected _id`s, '
                          'separated by space')


@bot.message_handler(commands=['vacancies'])
def get_vacancies(message):
    bot.reply_to(message, f'{list_of_vacancies()}')


@bot.message_handler(commands=['look_at_vacancy'],)
def look_at_vacancy(message):
    vacancy_description = message.text[17:]
    if vacancy_description in list_of_vacancies():
        bot.reply_to(
            message, (serialize(show_selected_vacancies(vacancy_description))))
    else:
        bot.reply_to(message, 'check your vacancy')


@bot.message_handler(commands=['update_list_of_columns'])
def update_list_of_columns(message):
    columns = message.text[24:]
    if not columns:
        bot.reply_to(message, 'You should write some columns. Try again.')
    else:
        update_columns(columns)
        bot.reply_to(
            message, f'list of columns in database is :'
                     f'\n{get_list_of_columns()}')


@bot.message_handler(commands=['update_vacancy'])
def update_vacancy(message):
    msg = bot.reply_to(message, 'enter vacancy name :')
    bot.register_next_step_handler(msg, get_v_name)


def get_v_name(message):
    vacancy_name = message.text
    if vacancy_name in list_of_vacancies():
        msg = bot.reply_to(message, 'enter vacancy field to edit :')
        bot.register_next_step_handler(msg, get_v_field,  vacancy_name)
    elif vacancy_name == 'exit':
        bot.reply_to(message, 'you had left this scenario')
    else:
        msg = bot.reply_to(message, 'this vacancy does not exist, '
                                    'enter again :')
        bot.register_next_step_handler(msg, get_v_name)


def get_v_field(message, *vacancy_name):
    vacancy_name = vacancy_name[0]
    vacancy_field = message.text
    if vacancy_field in show_columns_of_vacancy(vacancy_name):
        msg = bot.reply_to(message, 'enter new value')
        bot.register_next_step_handler(
            msg, get_v_value, vacancy_name, vacancy_field)
    elif vacancy_field == 'exit':
        bot.reply_to(message, 'you had left this scenario')
    else:
        msg = bot.reply_to(message, 'this field does not exist, enter again :')
        bot.register_next_step_handler(msg, get_v_field, vacancy_name)


def get_v_value(message, *vacancy_name):
    vacancy_field = vacancy_name[1]
    vacancy_name = vacancy_name[0]
    value = message.text
    update_vacancy_requirements(vacancy_name, vacancy_field, value)
    bot.reply_to(message,
                 f'new --{vacancy_name}-- requirements are :\n\n '
                 f'{(serialize(show_selected_vacancies(vacancy_name)))}')


@bot.message_handler(commands=['open_vacancy'])
def open_vacancy(message):
    vacancy_name = message.text[14:]
    if vacancy_name in list_of_vacancies() and \
            vacancy_name not in opened_vacancies():
        bot.reply_to(message, str(open_vacancy_db(vacancy_name)))
    else:
        bot.reply_to(message, 'this vacancy is open '
                              'or it`s requirements was not written')


@bot.message_handler(commands=['close_vacancy'])
def close_vacancy(message):
    vacancy_name = message.text[15:]
    if vacancy_name in list_of_vacancies():
        bot.reply_to(message, str(close_vacancy_db(vacancy_name)))
    else:
        bot.reply_to(message, 'this vacancy was not opened')


@bot.message_handler(commands=['show_all'])
def show_all(message):
    vacancy_name = message.text[10:]
    if vacancy_name in list_of_vacancies():
        bot.reply_to(message, show_selected_cvs(vacancy_name))
    else:
        bot.reply_to(message, 'vacancy does not exists')


@bot.message_handler(commands=['show_one_by_one'])
def show_one_by_one(message):
    vacancy_name = message.text[17:]
    if vacancy_name in list_of_vacancies():
        msg = bot.reply_to(message, 'send any message to look at next cv')
        bot.register_next_step_handler(msg, mover, vacancy_name)
    else:
        bot.reply_to(message, 'vacancy does not exists')


def mover(message, vacancy_name, i=0):
    list_vacancies = show_selected_cvs(vacancy_name).split('\n ')[1:]
    if i < len(list_vacancies):
        if message.text == 'exit':
            bot.reply_to(message, 'you had left this scenario')
        else:
            msg = bot.reply_to(message, f'send any message to look '
                                        f'at next cv:\n{list_vacancies[i]}')
            i += 1
            bot.register_next_step_handler(msg, mover, vacancy_name, i)
    else:
        bot.reply_to(message, 'list is already empty')


@bot.message_handler(commands=['show_selected'])
def show_selected(message):
    if len(message.text[15:].split(' ')) == 2:
        cv_ids = message.text[15:]
        bot.reply_to(message, show_cvs(cv_ids))
    else:
        bot.reply_to(message, 'you should insert only 2 cv`s ids, '
                              'separated by space. Try again.')


@bot.message_handler(commands=['delete_by_id'])
def delete_by_id(message):
    user_id = message.text[14:]
    bot.reply_to(message, delete_user(user_id))


if __name__ == '__main__':
    bot.polling()
