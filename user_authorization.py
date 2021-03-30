import hashlib
import model


def search_for_matches(us, psw):
    """Поиск совпадений данных из форма авторизации в БД"""
    search = False
    user_id = 0
    data = model.Users.query.order_by(model.Users.username, model.Users.password_hash, model.Users.id).all()
    pre_list = []
    for el in data:
        if el.username == us:
            pre_list.append(el.id)
            pre_list.append(el.password_hash)
            search = True
            break

    if search:
        """Если username есть в БД, сравниваем пароли"""
        if pre_list[1] == hashlib.md5(psw.encode()).hexdigest():
            user_id = pre_list[0]

    return user_id
