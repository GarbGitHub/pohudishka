from flask import session, redirect, url_for, request, flash
import hashlib
import model


def user_verification_on_the_server(us, em):
    """Поиск на совпадение имени пользователя и email в БД при регистрации пользователя"""

    search_user_result = True
    user = model.Users.query.order_by(model.Users.username, model.Users.email).all()

    for el in user:
        if el.username == us:
            """Если username уже есть в базе - записываем в переменную и прекращаем цикл"""

            search_user_result = us
            break

    if search_user_result:
        """Если в username совпадений нет, осуществляется поиск сравнений по email"""

        for el in user:
            if el.email == em:
                search_user_result = em
                break
    return search_user_result


def user_registration_and_verification():
    """Валидация формы регистрации пользователя"""
    if 'username' in session:
        return redirect(url_for('login_username', username=session['username']))
    if request.method == "POST":
        try:
            if len(request.form['username']) > 4 \
                    and len(request.form['email']) > 4 \
                    and len(request.form['password0']) > 4 \
                    and request.form['password0'] == request.form['password']:
                print('ok')
                user_db = user_verification_on_the_server(request.form['username'], request.form['email'])

                if user_db:  # если username и email уникальные
                    hash = hashlib.md5(request.form['password0'].encode()).hexdigest()
                    print(str(hash))

                    res = model.Users(
                        username=request.form['username'],
                        email=request.form['email'],
                        password_hash=hash
                        )

                    result_registration = model.add_object_to_base(res)

                    if result_registration is not None:  # если запись в БД не успешная
                        flash('Ошибка при регистрации', 'danger')
                    else:
                        flash('Вы успешно зарегистрированы', category='success')
                else:
                    flash(f'Запись ({user_db}) уже есть в базе', category='danger')
            else:
                flash('Ошибка ввода данных', 'danger')
        except TypeError:
            flash('Unicode-объекты должны быть закодированы перед хешированием', 'danger')
        except ValueError:
            flash('Не верный тип данных', 'danger')