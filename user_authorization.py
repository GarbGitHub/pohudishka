import hashlib
import model


def search_for_matches(us, psw):
    """Поиск совпадений данных из форма авторизации в БД"""
    search = False
    user_id = 0
    data = model.Users.query.order_by(model.Users.username, model.Users.password_hash, model.Users.id).all()
    prelist = []
    for el in data:
        if el.username == us:
            prelist.append(el.id)
            prelist.append(el.password_hash)
            search = True
            break

    if search:
        """Если username есть в БД, сравниваем пароли"""
        if prelist[1] == hashlib.md5(psw.encode()).hexdigest():
            user_id = prelist[0]

    return user_id
