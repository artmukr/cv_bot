from flask import request, json
from settings import app
from db_connection \
	import list_of_vacancies, serialize, show_selected_vacancies, \
	update_columns, get_list_of_columns, update_vacancy_requirements, \
	show_columns_of_vacancy, opened_vacancies, open_vacancy_db, \
	close_vacancy_db, show_selected_cvs, write_new_cv, write_list_of_columns, \
	delete_user, show_cvs


@app.route('/vacancies', methods=['GET'])
def get_vacancies():
	return str(list_of_vacancies())


@app.route('/look_at_vacancy', methods=['GET'])
def get_single_vacancy(vacancy_name):
	return serialize(show_selected_vacancies(vacancy_name))


@app.route('/opened', methods=['GET'])
def opened():
	return opened_vacancies()


@app.route('/apply_vacancy', methods=['POST'])
def apply_vacancy():
	temp = json.loads(request.data.decode('utf-8'))
	return write_new_cv(temp)


@app.route('/get_list_of_columns', methods=['GET'])
def get_col_list():
	return str(get_list_of_columns()), 200


@app.route('/show_columns_of_vacancy', methods=['GET'])
def show_col_of_vac():
	vacancy = request.args.get('filter')
	return str(show_columns_of_vacancy(vacancy))


@app.route('/write_list_of_columns', methods=['POST'])
def write_columns():
	columns = request.args.get('columns')
	return write_list_of_columns(columns)


@app.route('/update_list_of_columns', methods=['PATCH'])
def update_list_of_columns():
	columns = request.args.get('columns')[1:-1].replace("'", "").split(', ')
	return str(update_columns(columns))


@app.route('/show_selected_vacancies', methods=['GET'])
def show_sel_vacancies():
	vacancy_name = request.args.get('filter')
	return str(serialize(show_selected_vacancies(vacancy_name)))


@app.route('/update_vacancy', methods=['PATCH'])
def update_vacancy():
	args = request.args.get('data').split(', ')
	vacancy_name = args[0]
	vacancy_field = args[1]
	value = args[2]
	return update_vacancy_requirements(vacancy_name, vacancy_field, value)


@app.route('/opened_vacancies', methods=['GET'])
def get_opened_vacancies():
	return str(opened_vacancies())


@app.route('/open_vacancy', methods=['PATCH'])
def open_vacancy():
	vacancy_name = request.args.get('vacancy_name')
	return str(open_vacancy_db(vacancy_name))


@app.route('/close_vacancy', methods=['PATCH'])
def close_vacancy():
	vacancy_name = request.args.get('vacancy_name')
	return str(close_vacancy_db(vacancy_name))


@app.route('/show_all', methods=['GET'])
def show_all():
	vacancy_name = request.args.get('vacancy_name')
	return show_selected_cvs(vacancy_name)


@app.route('/show_one_by_one', methods=['GET'])
def show_one_by_one(vacancy):
	return show_selected_cvs(vacancy)


@app.route('/delete_user', methods=['DELETE'])
def delete_user_by_id():
	user_id = request.args.get('user_id')
	return delete_user(user_id)


@app.route('/show_cvs', methods=['GET'])
def show_cvs_route():
	ids = request.args.get('ids')
	return show_cvs(ids)
