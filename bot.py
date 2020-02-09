from telebot import TeleBot
from db_connection import get_list_of_columns, list_of_vacancies, \
    show_selected_vacancies, serialize, write_new_cv
from bot_code import code

bot = TeleBot(code)


@bot.message_handler(commands=['start', 'help'])
def start(message):

    bot.reply_to(message, 'commands:\n\n'
                          '/vacancies\n\n'
                          '/choose_vacancy #vacancy name#\n\n'
                          '/apply_vacancy #vacancy_name#\n\n')


@bot.message_handler(commands=['vacancies'])
def get_vacancies(message):
    bot.reply_to(message, f'{list_of_vacancies()}')


@bot.message_handler(commands=['choose_vacancy'])
def choose_vacancy(message):
    print(message.text[16:])
    bot.reply_to(
        message, (serialize(show_selected_vacancies(message.text[16:]))))


@bot.message_handler(commands=['apply_vacancy'])
def apply_vacancy(message, index_saver=0, temp=None):
    list_of_columns = get_list_of_columns()
    if temp is None:
        temp = {}
    if index_saver == 0:
        # validation of vacancy
        if message.text[15:] in list_of_vacancies():
            temp[list_of_columns[0]] = message.text[15:]
            index_saver += 1
            msg = bot.reply_to(message, f'{list_of_columns[index_saver]}: ')
            bot.register_next_step_handler(
                msg, apply_vacancy, index_saver, temp)
        else:
            msg = bot.reply_to(message, 'vacancy is not exist. Check it!')
            bot.register_next_step_handler(msg, apply_vacancy)
    elif index_saver < len(list_of_columns) - 1:
        temp[list_of_columns[index_saver]] = message.text
        msg = bot.reply_to(message, f'{list_of_columns[index_saver+1]}: ')
        index_saver += 1
        bot.register_next_step_handler(msg, apply_vacancy, index_saver, temp)
    else:
        bot.reply_to(message, write_new_cv(temp))


if __name__ == '__main__':
    bot.polling()
