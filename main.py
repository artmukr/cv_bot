import requests
from settings import app
from db_connection \
	import list_of_vacancies, serialize, show_selected_vacancies, \
	update_columns, get_list_of_columns, update_vacancy_requirements, \
	show_columns_of_vacancy, opened_vacancies, open_vacancy_db, \
	close_vacancy_db, show_selected_cvs, write_new_cv


@app.route('/vacancies', methods=['GET'])
def get_vacancies():
	return list_of_vacancies()


@app.route('/look_at_vacancy', methods=['GET'])
def get_single_vacancy(vacancy_name):
	return serialize(show_selected_vacancies(vacancy_name))


@app.route('/opened', methods=['GET'])
def opened():
	return opened_vacancies()


@app.route('/apply_vacancy', methods=['POST'])
def apply_vacancy(vacancy_name, temp):
	return write_new_cv(temp)


@app.route('/get_list_of_columns', methods=['GET'])
def get_col_list():
	return get_list_of_columns()


@app.route('/show_columns_of_vacancy', methods=['GET'])
def show_col_of_vac(vacancy):
	return show_columns_of_vacancy(vacancy)


@app.route('/update_list_of_columns', methods=['PATCH'])
def update_list_of_columns(columns):
	return update_columns(columns)


@app.route('/show_selected_vacancy', methods=['vacancy_name'])
def show_sel_vacancy(vacancy_name):
	return serialize(show_selected_vacancies(vacancy_name))


@app.route('/update_vacancy', methods=['PATCH'])
def update_vacancy(*args):
	vacancy_name = args[0]
	vacancy_field = args[1]
	value = args[2]
	return update_vacancy_requirements(vacancy_name, vacancy_field, value)


@app.route('/opened_vacancies', methods=['GET'])
def get_opened_vacancies():
	return opened_vacancies()


@app.route('/open_vacancy', methods=['PATCH'])
def open_vacancy(vacancy_name):
	return str(open_vacancy_db(vacancy_name))


@app.route('/close_vacancy', methods=['PATCH'])
def close_vacancy(vacancy_name):
	return str(close_vacancy_db(vacancy_name))


@app.route('/show_all', methods=['GET'])
def show_all(vacancy_name):
	return show_selected_cvs(vacancy_name)


@app.route('/show_one_by_one', methods=['GET'])
def show_one_by_one():
	pass
