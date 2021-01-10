from flask import render_template, session, abort, redirect, url_for, request, flash
from datetime import datetime
import model
import user_authorization
import user_registration


def check_user_authorization():
    if 'username' in session:
        user = session['username']
    else:
        user = None
    return user


menu = [{"name": "Главная", "url": "/"},
        {"name": "Добавить запись", "url": "/add/"}]


def route_index():
    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):
        list = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
            model.UserWeight.created_at.desc()).all()
    else:
        list = []

    return render_template('index.html',
                           title='Вес',
                           menu=menu,
                           list=list,
                           session=check_user_authorization())


def route_add():
    if ('username' in session) and ('user_id' in session):
        pass
    if request.method == 'POST':
        try:
            progress = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
                model.UserWeight.created_at.desc()).first()

            if progress and progress.real_weight != 0.0:
                real_progress = float((str(request.form['weight']))) - progress.real_weight
            else:
                real_progress = 0.0
            obj = model.UserWeight(user_id=session['user_id'],
                                   real_weight=float((str(request.form['weight']))),
                                   real_progress=real_progress,
                                   created_at=datetime.now()
                                   )
            model.add_object_to_base(obj)

            flash(f'Запись успешно добавлена', category='success')
            return redirect(url_for('index'))

        except ValueError:
            flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
        except (TypeError, AttributeError):
            flash(f'В запросе к базе данных произошла ошибка!', category='danger')

    return render_template('add.html',
                           title='Новая запись',
                           menu=menu,
                           session=check_user_authorization())


def route_login_username(username):
    # если пользователь авторизован
    if 'username' not in session or session['username'] != username:
        abort(401)
    submenu = [{"name": "Выйти", "url": "/logout"}]
    return render_template('profile.html',
                           title=f'Профиль пользователя "{username}"',
                           menu=menu,
                           submenu=submenu,
                           username=username,
                           session=check_user_authorization())


def route_login():
    if request.method == 'POST':

        # присваиваем переменным данные из формы
        username = request.form['username']
        psw = request.form['psw']
        user_id = user_authorization.search_for_matches(username, psw)

        if user_id != 0:

            # создаем ключи в объекте session
            session.permanent = True
            session['username'] = request.form['username']
            session['user_id'] = user_id
            return redirect(url_for('login_username', username=session['username']))
        else:
            flash(f'Не верный логин или пароль', category='danger')

    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):

        # направляем в профиль
        return redirect(url_for('login_username', username=session['username']))

    # иначе показываем форму авторизации
    else:
        submenu = [{"name": "Регистрация", "url": "/registration/"}]
        return render_template('login.html',
                               title="Авторизация",
                               menu=menu,
                               submenu=submenu,
                               session=check_user_authorization())


def rout_logout():
    """Выход пользователя из системы, удаление сессии"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


def rout_registration():
    submenu = [{"name": "Войти", "url": "/login"}]
    user_registration.user_registration_and_verification()

    return render_template('registration.html',
                           title='Регистрация',
                           menu=menu,
                           submenu=submenu,
                           session=check_user_authorization())


def rout_pageNoteFound(error):
    return render_template('page_404.html',
                           title='Ошибка 404',
                           menu=menu,
                           session=check_user_authorization()), 404
