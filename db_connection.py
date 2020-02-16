from bson import ObjectId
from settings import table


# shows vacancy descriptions
def show_selected_vacancies(vacancy):
    return [a for a in table.find({'vacancy description': vacancy})]


def show_columns_of_vacancy(vacancy):
    dict_obj = ([a.keys() for a in
                 table.find({'vacancy description': vacancy})])
    return [a for a in dict_obj[0] if a != '_id']


# returns vacancy description in good-looking form
def serialize(vacancies):
    st = []
    for el in vacancies:
        st = str(st) + f"vacancy description -- {el['vacancy description']} " \
             f"\n\n education -- {el['education']}\n\n experience -- " \
             f"{el['experience']}\n\n languages -- {el['languages']}\n\n\n\n"
    return st[2:]


# writes employer`s cv to database
def write_new_cv(cv):
    table.insert(cv)
    return 'done, we will write to you later'


# returns list of  vacancies with requirements
def list_of_vacancies():
    vacancies = []
    for vacancy in table.find():
        a = vacancy.setdefault('vacancy description', None)
        if a is not None:
            vacancies.append(a)
    return vacancies


# write`s to database list of switched columns, that fills in by employer
def write_list_of_columns(columns):
    table.insert({'list_of_columns': columns})
    return 'columns was written'


# returns list of columns, that employer should fill in
def get_list_of_columns():
    return [a.get('list_of_columns') for a in table.find({})
            if a.get('list_of_columns') is not None][0]


# updates list_of_columns
def update_columns(columns):
    list_of_columns = columns.split(', ')
    table.update_one({'_id': ObjectId("5e3ed670fad73e98c9ec4337")},
                     {'$set': {'list_of_columns': list_of_columns}},
                     upsert=False)
    return get_list_of_columns()


# update vacancy requirements
def update_vacancy_requirements(vacancy_name, vacancy_field, new_data):
    table.update_one({'vacancy description': vacancy_name},
                     {'$set': {vacancy_field: new_data}}, upsert=False)
    return serialize(show_selected_vacancies(vacancy_name))


# returns vacancies with status 'open'
def opened_vacancies():
    return ([a.get('opened_vacancies') for a in table.find(
        {'_id': ObjectId("5e408dfe5cd5be458777b9a7")})][0])


# opens closed vacancy
def open_vacancy_db(vacancy_name):
    if vacancy_name not in opened_vacancies():
        table.update({'_id': ObjectId("5e408dfe5cd5be458777b9a7")},
                     {'$push': {'opened_vacancies': vacancy_name}})
        return opened_vacancies()
    else:
        return ' vacancy is already opened '


# close opened vacancy
def close_vacancy_db(vacancy_name):
    if vacancy_name in opened_vacancies():
        table.update({'_id': ObjectId("5e408dfe5cd5be458777b9a7")},
                     {'$pull': {'opened_vacancies': vacancy_name}})
        return opened_vacancies()
    else:
        return ' vacancy was not opened '


# returns cv`s of current vacancy
def show_selected_cvs(vacancy):
    output = ''
    for applicant in table.find({'vacancy': vacancy}):
        output = f'{output}\n {support_prev(applicant)}'
    return output


# supports show_selected_cvs
def support_prev(data):
    out_str = ''
    for col in data.items():
        out_str = f'{out_str}\n{col}'.replace(", ", " -- ")
    return out_str


# deletes user`s vacancies by id
def delete_user(user_id):
    if table.find_one({'user_id': user_id}) is not None:
        table.delete_many({'user_id': {'$eq': user_id}})
        return 'successful'
    else:
        return 'user not found'



