import requests
import json
path = 'http://localhost:5000'


def get_admin():
    return requests.get(f'{path}/admin_id').text


def show_selected_vacancies(vacancy_name: str) -> str:
    str_list = requests.get(
        f'{path}/show_selected_vacancies?filter={vacancy_name}').text
    return str_list


def show_columns_of_vacancy(vacancy_name: str) -> str:
    str_list = requests.get(
        f'{path}/show_columns_of_vacancy?filter={vacancy_name}').text[1:-1]
    return str_list.replace("'", "").split(', ')


def write_new_cv(cv: dict) -> str:
    cv = json.dumps(cv)
    return requests.post(f'{path}/apply_vacancy', data=cv).text


def list_of_vacancies() -> str:
    str_list = requests.get(f'{path}/vacancies').text[1:-1]
    return str_list.replace("'", "").split(', ')


def write_list_of_columns(columns: list) -> str:
    columns = ', '.join(columns)
    return requests.post(
        f'{path}/write_list_of_columns', data=columns).text


def get_list_of_columns() -> str:
    columns = requests.get(
        f'{path}/get_list_of_columns').text[1:-1].replace("'", "").split(', ')
    return columns


def update_columns(columns: dict) -> str:
    columns = str(columns)
    columns = requests.patch(
        f'{path}/update_list_of_columns', data=columns).text[1:-1]
    columns = columns.replace("'", "").split(', ')
    return columns


def update_vacancy_requirements(
        vacancy_name: str, vacancy_field: str, new_data: str) -> str:
    data = f'{vacancy_name}, {vacancy_field}, {new_data})'
    return requests.patch(f'{path}/update_vacancy', data=data).text


def opened_vacancies() -> str:
    vacancies = requests.get(
        f'{path}/opened_vacancies').text[1:-1].replace("'", "").split(', ')
    return vacancies


def open_vacancy_db(vacancy_name: str) -> list:
    vacancies = requests.patch(
        f'{path}/open_vacancy',
        data=vacancy_name).text[1:-1].replace("'", "").split(', ')
    return vacancies


def close_vacancy_db(vacancy_name: str) -> list:
    vacancies = requests.patch(
        f'{path}/close_vacancy',
        data=vacancy_name).text[1:-1].replace(
        "'", "").split(', ')
    return vacancies


def show_selected_cvs(vacancy_name: str) -> str:
    cvs = requests.get(
        f'{path}/show_all?vacancy_name={vacancy_name}').text
    return cvs


def delete_user(user_id: str) -> str:
    return requests.delete(f'{path}/delete_user?user_id={user_id}').text


def show_cvs(ids: str) -> str:
    return requests.get(f'{path}/show_cvs?ids={ids}').text
