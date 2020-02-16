import requests
import json

path = 'http://localhost:5000'


def show_selected_vacancies(vacancy_name):
    str_list = requests.get(
        f'{path}/show_selected_vacancies?filter={vacancy_name}').text[1:-1]
    return str_list.replace("'", "").split(', ')


def show_columns_of_vacancy(vacancy_name):
    str_list = requests.get(
        f'{path}/show_columns_of_vacancy?filter={vacancy_name}').text[1:-1]
    return str_list.replace("'", "").split(', ')


def serialize(vacancies):
    st = []
    for el in vacancies:
        st = str(st) + f"vacancy description -- {el['vacancy description']} " \
             f"\n\n education -- {el['education']}\n\n experience -- " \
             f"{el['experience']}\n\n languages -- {el['languages']}\n\n\n\n"
    return st[2:]


# testing needed
def write_new_cv(cv):
    return requests.post(f'{path}/apply_vacancy', data=json.dumps(cv))


def list_of_vacancies():
    str_list = requests.get(f'{path}/vacancies').text[1:-1]
    return str_list.replace("'", "").split(', ')


def write_list_of_columns(columns):
    columns = ', '.join(columns)
    return requests.post(
        f'{path}/write_list_of_columns?data={columns}', columns=columns).text


def get_list_of_columns():
    columns = requests.get(
        f'{path}/get_list_of_columns').text[1:-1].replace("'", "").split(', ')
    return columns


def update_columns(columns):
    columns = str(columns)
    columns = requests.patch(
        f'{path}/update_list_of_columns?columns={columns}'
    ).text[1:-1]
    columns = columns.replace("'", "").split(', ')
    return columns


def update_vacancy_requirements(vacancy_name, vacancy_field, new_data):
    data = f'{vacancy_name}, {vacancy_field}, {new_data})'
    return requests.patch(f'{path}/update_vacancy?data={data}').text


def opened_vacancies():
    vacancies = requests.get(
        f'{path}/opened_vacancies').text[1:-1].replace("'", "").split(', ')
    return vacancies


def open_vacancy_db(vacancy_name):
    vacancies = requests.patch(
        f'{path}/open_vacancy?'
        f'vacancy_name={vacancy_name}').text[1:-1].replace("'", "").split(', ')
    return vacancies


def close_vacancy_db(vacancy_name):
    vacancies = requests.patch(
        f'{path}/close_vacancy'
        f'?vacancy_name={vacancy_name}').text[1:-1].replace(
        "'", "").split(', ')
    return vacancies


def show_selected_cvs(vacancy_name):
    cvs = requests.get(
        f'{path}/show_all?vacancy_name={vacancy_name}').text
    return cvs


def delete_user(user_id):
    return requests.delete(f'{path}/delete_user?user_id={user_id}').text

