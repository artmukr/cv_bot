from pymongo import MongoClient

client = MongoClient('localhost')
db = client.mydb
table = db.vacancies


# x = table.insert_one(columns)
# print(db.list_collection_names())

list_of_columns = ['vacancy', 'first_name', 'last_name',
                   'phone_number', 'education', 'experience',
                   'languages', 'achievements']

# list_of_vacancies = ['python developer', 'senior accounted', 'office manager']

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


def show_selected_vacancies(vacancy):
    return [a for a in table.find({'vacancy description': vacancy})]


def serialize(vacancies):
    st = []
    for el in vacancies:
        st = str(st) + f"vacancy description -- {el['vacancy description']} " \
             f"\n\n education -- {el['education']}\n\n experience -- " \
             f"{el['experience']}\n\n languages -- {el['languages']}\n\n\n\n"
    return st[2:]


def write_new_cv(cv):
    db.vacancies.insert(cv)
    return 'done, we will write to you later'


def list_of_vacancies():
    vacancies = []
    for vacancy in table.find():
        a = vacancy.setdefault('vacancy description', None)
        if a is not None:
            vacancies.append(a)
    return vacancies


def write_list_of_columns(columns):
    db.vacancies.insert({'list_of_columns': columns})
    return 'columns was written'
# if __name__ == '__main__':
#     # x = table.delete_many({})
#     db.vacancies.insert_many([
#         developer_vacancy, senior_accounted, office_manager])
# write_list_of_columns(list_of_columns)


def get_list_of_columns():
    return [a.get('list_of_columns') for a in table.find({})
            if a.get('list_of_columns') is not None][0]

