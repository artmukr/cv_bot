from telebot import TeleBot
from bot_code import admin_code
from db_connection \
    import list_of_vacancies, serialize, show_selected_vacancies, \
    update_columns, get_list_of_columns, update_vacancy_requirements, \
    show_columns_of_vacancy, opened_vacancies, open_vacancy_db, \
    close_vacancy_db, show_selected_cvs

bot = TeleBot(admin_code)


@bot.message_handler(commands=['start', 'help'])
def start(message):

    bot.reply_to(message, 'commands:\n\n'
                          '/vacancies\n\n'
                          '/look_at_vacancy  #vacancy name#\n\n'
                          '/update_list_of_columns  #list of columns, '
                          'separated by comma#\n\n'
                          '/update_vacancy  #you can exit from command \n'
                          'with key-word "exit"\n\n'
                          '/open_vacancy #vacancy name\n\n'
                          '/close_vacancy #vacancy name\n\n'
                          '/show_all #vacancy name - shows all applicants\n\n'
                          '/show_one_by_one #vacancy name\n\n')


@bot.message_handler(commands=['vacancies'])
def get_vacancies(message):
    bot.reply_to(message, f'{list_of_vacancies()}')


@bot.message_handler(commands=['look_at_vacancy'])
def look_at_vacancy(message):
    bot.reply_to(
        message, (serialize(show_selected_vacancies(message.text[17:]))))


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
        bot.register_next_step_handler(msg, get_v_field)


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
        msg = bot.reply_to(message, list_vacancies[i])
        i += 1
        bot.register_next_step_handler(msg, mover, vacancy_name, i)
    else:
        bot.reply_to(message, 'list is already empty')


@bot.message_handler(commands=['show_selected'])
def show_selected(message):
    pass


@bot.message_handler(commands=['delete_by_id'])
def delete_by_id(message):
    user_id = message.text[14:]
    # if user_id in


if __name__ == '__main__':
    bot.polling()
