import os
import re

from flask import session, redirect, url_for, request, flash
import hashlib
import model


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


def search_bad_symbols_and_username(username):
    """Поиск зарезервированных слов и запрещенных символов"""

    search_bad_symbols_result = 'No'
    bad_username = ['root', 'admin', 'moderator', 'support', 'supports', 'helpdesk']
    bad_symbols = ['&', ' ', '=', '+', '<', '>', ',', '.', '\"', '\'', '?', '!', ':', ';', '/', '\\', '|', '#', '|',
                   '^']

    if bool(re.search('[а-яА-Я]', username)):
        search_bad_symbols_result = f'Ошибка! В поле Login нельзя использовать русские буквы'

    if search_bad_symbols_result == 'No':
        for el in bad_username:
            if el == username:
                search_bad_symbols_result = f'Ошибка! Нельзя использовать {username} - зарезервированное имя!'
                break

    if search_bad_symbols_result == 'No':
        for el in bad_symbols:
            if str(username).find(el) != -1:
                search_bad_symbols_result = f'Ошибка! В поле Login найден запрещенный символ ({el})'
                break

    return search_bad_symbols_result


def binary_search(item, array, is_chek):
    """Бинарный поиск на совпадение username, email"""

    search_user_result = False
    min_ = 0
    max_ = len(array) - 1
    while min_ <= max_:
        mid = (min_ + max_) // 2
        guess = array[mid]
        if not is_chek:
            guess_txt = guess.username.lower()
        else:
            guess_txt = guess.email.lower()
        if guess_txt == item.lower():
            search_user_result = item
            break
        if guess_txt > item.lower():
            max_ = mid - 1
        else:
            min_ = mid + 1
    return search_user_result


def user_verification_on_the_server(username, email):
    """Поиск на совпадение имени пользователя и email в БД при регистрации пользователя"""

    user = model.Users.query.order_by(model.Users.username).all()
    search_user_result = binary_search(item=username, array=user, is_chek=False)

    if not search_user_result:
        """Если в username совпадений нет, осуществляется поиск сравнений по email"""

        user = model.Users.query.order_by(model.Users.email).all()
        search_user_result = binary_search(item=email, array=user, is_chek=True)
    return search_user_result


def user_registration_and_verification():
    """Валидация формы регистрации пользователя"""
    if 'username' in session:
        return redirect(url_for('login_username', username=session['username']))
    if request.method == "POST":
        try:
            username = request.form['username']
            if len(username) > 4 \
                    and len(request.form['password0']) > 4 \
                    and request.form['password0'] == request.form['password']:

                symbols_and_username_result = search_bad_symbols_and_username(username)
                if symbols_and_username_result != 'No':
                    flash(symbols_and_username_result, 'danger')
                else:
                    search_user_result = user_verification_on_the_server(username, request.form['email'])

                    if not search_user_result:  # если username и email уникальные
                        hash_ = hashlib.md5(request.form['password0'].encode()).hexdigest()

                        res = model.Users(
                            username=username,
                            email=request.form['email'],
                            password_hash=hash_
                        )

                        result_registration = model.add_object_to_base(res)

                        if result_registration is not None:  # если запись в БД не успешная
                            flash('Ошибка при регистрации', 'danger')
                        else:
                            user_id = model.Users.query.with_entities(model.Users.id).filter_by(
                                username=username).first()
                            create_profile = model.Profiles(
                                user_id=user_id
                            )
                            result_create_profile = model.add_object_to_base(create_profile)
                            if result_create_profile is not None:  # если запись в БД не успешная
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
        except FileExistsError:
            flash('Папка пользователя была создана ранее', 'danger')
