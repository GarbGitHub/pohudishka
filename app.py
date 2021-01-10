from app_init import app
import funcs
from datetime import datetime

@app.route('/index', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():
    return funcs.route_index()


@app.route('/add/', methods=["POST", "GET"])
def add():
    return funcs.route_add()


@app.route('/login/<username>/')
def login_username(username):
    return funcs.route_login_username(username)


@app.route("/login/", methods=["POST", "GET"])
def login():
    return funcs.route_login()


@app.route("/logout/")
def logout():
    return funcs.rout_logout()


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    return funcs.rout_registration()


@app.errorhandler(404)
def pageNoteFound(error):
    return funcs.rout_pageNoteFound(error)


if __name__ == '__main__':  # Запуск сервера на локальном устройстве
    app.run(debug=True)  # отображение ошибок
