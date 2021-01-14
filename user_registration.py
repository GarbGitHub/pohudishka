import os

from flask import session, redirect, url_for, request, flash
import hashlib
import model


def search_bad_symbols_and_username(username):
    """Поиск зарезервированных слов и запрещенных символов"""

    search_bad_symbols_result = 'No'
    bad_username = ['root', 'admin', 'moderator', 'support', 'supports', 'helpdesk']
    bad_symbols = ['&', ' ', '=', '+', '<', '>', ',', '.', '\"', '\'', '?', '!', ':', ';', '/', '\\', '|', '#', '|',
                   '^']

    for el in bad_username:
        if el == username:
            search_bad_symbols_result = f'Ошибка! Нельзя использовать {username} - зарезервированное имя!'
            break

    if search_bad_symbols_result == 'No':
        for el in bad_symbols:
            if str(username).find(el) != -1:
                search_bad_symbols_result = f'Ошибка! В Login найден запрещенный символ ({el})'
                break

    return search_bad_symbols_result


def user_verification_on_the_server(us, em):
    """Поиск на совпадение имени пользователя и email в БД при регистрации пользователя"""

    search_user_result = 'uniq'
    user = model.Users.query.order_by(model.Users.username, model.Users.email).all()

    for el in user:
        if el.username.lower() == us.lower():
            """Если username уже есть в базе - записываем в переменную и прекращаем цикл"""

            search_user_result = us
            break

    if search_user_result == 'uniq':
        """Если в username совпадений нет, осуществляется поиск сравнений по email"""

        for el in user:
            if el.email.lower() == em.lower():
                search_user_result = em
                break
    return search_user_result


def user_registration_and_verification():
    """Валидация формы регистрации пользователя"""
    if 'username' in session:
        return redirect(url_for('login_username', username=session['username']))
    if request.method == "POST":
        try:
            username = request.form['username']
            if len(username) > 4 \
                    and len(request.form['email']) > 4 \
                    and len(request.form['password0']) > 4 \
                    and request.form['password0'] == request.form['password']:
                print('ok')

                symbols_and_username_result = search_bad_symbols_and_username(username)
                if symbols_and_username_result != 'No':
                    flash(symbols_and_username_result, 'danger')
                else:
                    search_user_result = user_verification_on_the_server(username, request.form['email'])

                    if search_user_result == 'uniq':  # если username и email уникальные
                        hash = hashlib.md5(request.form['password0'].encode()).hexdigest()
                        print(str(hash))

                        res = model.Users(
                            username=username,
                            email=request.form['email'],
                            password_hash=hash
                        )

                        result_registration = model.add_object_to_base(res)

                        if result_registration is not None:  # если запись в БД не успешная
                            flash('Ошибка при регистрации', 'danger')
                        else:
                            os.mkdir(f'static/users/{username.lower()}')
                            os.mkdir(f'static/users/{username.lower()}/graph')
                            os.mkdir(f'static/users/{username.lower()}/profile')
                            flash('Вы успешно зарегистрированы', category='success')

                    else:
                        flash(f'Запись ({search_user_result}) уже есть в базе', category='danger')
            else:
                flash('Ошибка ввода данных', 'danger')
        except TypeError:
            flash('Unicode-объекты должны быть закодированы перед хешированием', 'danger')
        except ValueError:
            flash('Не верный тип данных', 'danger')
