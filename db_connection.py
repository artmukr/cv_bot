from bson import ObjectId
from settings import table


# get admin`s id
def get_admin() -> str:
    return str(table.find_one(
        {'_id': ObjectId("5e49af12eb686b16c4cd41d6")})['admin_id'])


# shows vacancy descriptions
def show_selected_vacancies(vacancy: str) -> list:
    return [a for a in table.find({'vacancy description': vacancy})]


# shows columns that employee should fill in
def show_columns_of_vacancy(vacancy: str) -> list:
    dict_obj = ([a.keys() for a in
                 table.find({'vacancy description': vacancy})])
    return [a for a in dict_obj[0] if a != '_id']


# returns vacancy description in good-looking form
def serialize(vacancies: list) -> list:
    st = []
    for el in vacancies:
        st = str(st) + f"vacancy description -- {el['vacancy description']} " \
             f"\n\n education -- {el['education']}\n\n experience -- " \
             f"{el['experience']}\n\n languages -- {el['languages']}\n\n\n\n"
    return st[2:]


# writes employer`s cv to database
def write_new_cv(cv: dict) -> str:
    table.insert(cv)
    return 'done, we will write/call to you later'


# returns list of  vacancies with requirements
def list_of_vacancies() -> list:
    vacancies = []
    for vacancy in table.find():
        a = vacancy.setdefault('vacancy description', None)
        if a is not None:
            vacancies.append(a)
    return vacancies


# write`s to database list of switched columns, that fills in by employer
def write_list_of_columns(columns: str) -> str:
    table.update({'_id': ObjectId("5e3ed670fad73e98c9ec433")},
                 {'$set': {'list_of_columns': columns}}, upsert=False)
    return 'columns was written'


# returns list of columns, that employer should fill in
def get_list_of_columns() -> list:
    return [a.get('list_of_columns') for a in table.find({})
            if a.get('list_of_columns') is not None][0]


# updates list_of_columns
def update_columns(columns: str) -> list:
    list_of_columns = columns.split(', ')
    table.update_one({'_id': ObjectId("5e3ed670fad73e98c9ec4337")},
                     {'$set': {'list_of_columns': list_of_columns}},
                     upsert=False)
    return get_list_of_columns()


# update vacancy requirements
def update_vacancy_requirements(
        vacancy_name: str, vacancy_field: str, new_data: str) -> list:
    table.update_one({'vacancy description': vacancy_name},
                     {'$set': {vacancy_field: new_data}}, upsert=False)
    return serialize(show_selected_vacancies(vacancy_name))


# returns vacancies with status 'open'
def opened_vacancies() -> list:
    return [a.get('opened_vacancies') for a in table.find(
        {'_id': ObjectId("5e408dfe5cd5be458777b9a7")})][0]


# opens closed vacancy
def open_vacancy_db(vacancy_name: str) -> str or list:
    if vacancy_name not in opened_vacancies():
        table.update({'_id': ObjectId("5e408dfe5cd5be458777b9a7")},
                     {'$push': {'opened_vacancies': vacancy_name}})
        return opened_vacancies()
    else:
        return ' vacancy is already opened '


# close opened vacancy
def close_vacancy_db(vacancy_name: str) -> str or list:
    if vacancy_name in opened_vacancies():
        table.update({'_id': ObjectId("5e408dfe5cd5be458777b9a7")},
                     {'$pull': {'opened_vacancies': vacancy_name}})
        return opened_vacancies()
    else:
        return ' vacancy was not opened '


# returns cv`s of current vacancy
def show_selected_cvs(vacancy: str) -> str:
    output = ''
    for applicant in table.find({'vacancy': vacancy}):
        output = f'{output}\n {support_prev(applicant)}'
    return output


# supports show_selected_cvs
def support_prev(data: dict) -> str:
    out_str = ''
    for col in data.items():
        out_str = f'{out_str}\n{col}'.replace(", ", " -- ")
    return out_str


# deletes user`s vacancies by id
def delete_user(user_id: str) -> str:
    if table.find_one({'user_id': user_id}) is not None:
        table.delete_many({'user_id': {'$eq': user_id}})
        return 'successful'
    else:
        return 'user not found'


# return vacancies by cv id
def show_cvs(cvs: str) -> str:
    list_of_ids = cvs.split(' ')
    if len(list_of_ids[0]) == 24:
        first_id = ObjectId(list_of_ids[0])
    else:
        return 'first id is not valid, check number of symbols'
    if len(list_of_ids[1]) == 24:
        second_id = ObjectId(list_of_ids[1])
    else:
        return 'second id is not valid, check number of symbols'

    if show_selected_by_id_cvs(first_id) != '':
        first_cv = show_selected_by_id_cvs(first_id)
    else:
        first_cv = 'cv not found'
    if show_selected_by_id_cvs(second_id) != '':
        second_cv = show_selected_by_id_cvs(second_id)
    else:
        second_cv = 'cv not found'
    return f'first vacancy: \n{first_cv}\n\n' \
           f'second vacancy \n{second_cv}\n\n'


# returns cv`s by id
def show_selected_by_id_cvs(cv_id: ObjectId) -> str:
    output = ''
    for applicant in table.find({'_id': {'$eq': cv_id}}):
        data = support_prev_by_id(applicant)
        output = f'{output}\n {data}'
    return output


# supports show_selected_cvs_by_id
def support_prev_by_id(data: dict) -> str:
    out_str = ''
    for col in data.items():
        out_str = f'{out_str}\n{col}'.replace(", ", " -- ")
    return out_str
