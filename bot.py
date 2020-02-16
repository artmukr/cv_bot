from telebot import TeleBot
from sender_requests import get_list_of_columns, list_of_vacancies, \
    show_selected_vacancies, write_new_cv, opened_vacancies
from bot_code import code

bot = TeleBot(code)


@bot.message_handler(commands=['start', 'help'])
def start(message):

    bot.reply_to(message, '_________________________commands:'
                          '_________________________\n\n'
                          '/vacancies  ___________________'
                          'returns list of all opened vacancies\n\n'
                          '/look_at_vacancy ##vacancy name_____'
                          'returns specific vacancy\n\n'
                          '/apply_vacancy ##vacancy_name _______'
                          'respond to the vacancy\n'
                          '__________________________you can exit at any times'
                          ' with word exit \n\n')


@bot.message_handler(commands=['vacancies'])
def get_vacancies(message):
    bot.reply_to(message, f'{list_of_vacancies()}')


@bot.message_handler(commands=['look_at_vacancy'])
def look_at_vacancy(message):
    vacancy_description = message.text[17:]
    if vacancy_description in list_of_vacancies():
        bot.reply_to(
            message, (show_selected_vacancies(vacancy_description)))
    else:
        bot.reply_to(message, 'check your vacancy')


@bot.message_handler(commands=['apply_vacancy'])
def apply_vacancy(message, index_saver=0, temp=None):
    list_of_columns = get_list_of_columns()
    vacancy_name = message.text[15:]
    if temp is None:
        temp = {}
    if index_saver == 0:
        # validation of vacancy
        if vacancy_name in opened_vacancies():
            temp['user_id'] = message.from_user.id
            temp[list_of_columns[0]] = vacancy_name
            index_saver += 1
            msg = bot.reply_to(message, f'{list_of_columns[index_saver]}: ')
            bot.register_next_step_handler(
                msg, apply_vacancy, index_saver, temp)
        else:
            msg = bot.reply_to(message, 'vacancy is not opened. Check it!')
            bot.register_next_step_handler(msg, apply_vacancy)
    elif index_saver < len(list_of_columns) - 1:
        if message.text != 'exit':
            temp[list_of_columns[index_saver]] = message.text
            msg = bot.reply_to(message, f'{list_of_columns[index_saver+1]}: ')
            index_saver += 1
            bot.register_next_step_handler(
                msg, apply_vacancy, index_saver, temp)
        else:
            bot.reply_to(message, 'you left the Scenario')
    else:
        bot.reply_to(message, write_new_cv(temp))


if __name__ == '__main__':
    bot.polling()
