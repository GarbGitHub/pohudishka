from app_init import app
import funcs


@app.route('/index', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():
    return funcs.route_index()


@app.route('/add/', methods=["POST", "GET"])
def add():
    return funcs.route_add()


@app.route('/add_target/', methods=["POST", "GET"])
def add_target():
    return funcs.route_add_target()


@app.route('/profile/', methods=["GET"])
def profile():
    return funcs.route_profile()


@app.route('/profile/<username>/')
def login_username(username):
    return funcs.route_profile_username(username)


@app.route('/profile/<username>/weight/', methods=["POST", "GET"])
def weight(username):
    return funcs.route_weight()


@app.route('/profile/<username>/edit_profile/', methods=["POST", "GET"])
def edit_profile(username):
    return funcs.edit_profile(username)


@app.route("/login/", methods=["POST", "GET"])
def login():
    return funcs.route_login()


@app.route("/logout/")
def logout():
    return funcs.rout_logout()


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    return funcs.rout_registration()


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    return funcs.rout_admin()


@app.errorhandler(404)
def pageNoteFound(error):
    return funcs.rout_pageNoteFound(error)


if __name__ == '__main__':  # Запуск сервера на локальном устройстве
    app.run(debug=True)  # отображение ошибок
