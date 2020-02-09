from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost')
db = client.mydb
table = db.vacancies


developer_vacancy = {'vacancy description': 'python developer',
                     'education': 'high, beetroot is advantage',
                     'experience': '2 years',
                     'languages': ['portuguese', 'english', 'spanish']
                     }

senior_accounted = {'vacancy description': 'senior accountant',
                    'education': 'MAUP, only Maup',
                    'experience': '1.5 years',
                    'languages': 'english'
                    }

office_manager = {'vacancy description': 'office manager',
                  'education': 'Shevchenko Univercity',
                  'experience': '10 years',
                  'languages': 'english'
                  }


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
    db.vacancies.insert(cv)
    return 'done, we will write to you later'


# returns list of turned-on vacancies
def list_of_vacancies():
    vacancies = []
    for vacancy in table.find():
        a = vacancy.setdefault('vacancy description', None)
        if a is not None:
            vacancies.append(a)
    return vacancies


# write`s to database list of switched columns, that fills in by employer
def write_list_of_columns(columns):
    db.vacancies.insert({'list_of_columns': columns})
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


# update vacancy requirements
def update_vacancy_requirements(vacancy_name, vacancy_field, new_data):
    print(vacancy_name, vacancy_field, new_data)

# update_columns("vacancy, first_name, last_name, phone_number, education, "
#                "experience, languages, achievements")
# if __name__ == '__main__':
#     # x = table.delete_many({})
#     db.vacancies.insert_many([
#         developer_vacancy, senior_accounted, office_manager])
# write_list_of_columns(list_of_columns)
