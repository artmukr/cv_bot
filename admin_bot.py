from telebot import TeleBot
from bot_code import admin_code
from db_connection \
    import list_of_vacancies, serialize, show_selected_vacancies, \
    update_columns, get_list_of_columns, update_vacancy_requirements, \
    show_columns_of_vacancy

bot = TeleBot(admin_code)


@bot.message_handler(commands=['start', 'help'])
def start(message):

    bot.reply_to(message, 'commands:\n\n'
                          '/vacancies\n\n'
                          '/look_at_vacancy  #vacancy name#\n\n'
                          '/update_list_of_columns  #list of columns, '
                          'separated by comma#\n\n'
                          '/update_vacancy\n\n')


@bot.message_handler(commands=['vacancies'])
def get_vacancies(message):
    bot.reply_to(message, f'{list_of_vacancies()}')


@bot.message_handler(commands=['look_at_vacancy'])
def look_at_vacancy(message):
    bot.reply_to(
        message, (serialize(show_selected_vacancies(message.text[17:]))))


@bot.message_handler(commands=['update_list_of_columns'])
def update_list_of_columns(message):
    update_columns(message.text[24:])
    bot.reply_to(
        message, f'list of columns in database is :\n{get_list_of_columns()}')


@bot.message_handler(commands=['update_vacancy'])
def update_vacancy(message):
    msg = bot.reply_to(message, 'enter vacancy name :')
    bot.register_next_step_handler(msg, get_v_name)


def get_v_name(message):
    vacancy_name = message.text
    if vacancy_name in list_of_vacancies():
        msg = bot.reply_to(message, 'enter vacancy filed to edit :')
        bot.register_next_step_handler(msg, get_v_field,  vacancy_name)
    elif vacancy_name == 'exit':
        bot.reply_to(message, 'you had left this scenario')
    else:
        msg = bot.reply_to(message, 'this vacancy does not exist, '
                                    'enter again :')
        bot.register_next_step_handler(msg, get_v_name)


def get_v_field(message, vacancy_name):
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


def get_v_value(message, vacancy_name, vacancy_field):
    value = message.text
    update_vacancy_requirements(vacancy_name, vacancy_field, value)
    bot.reply_to(message,
                 f'new --{vacancy_name}-- requirements are :\n\n '
                 f'{(serialize(show_selected_vacancies(vacancy_name)))}')


if __name__ == '__main__':
    bot.polling()
