import numpy as np
from flask import render_template, session, abort, redirect, url_for, request, flash
from datetime import datetime
import model
import modules
from modules import menu, deleting_files, graph
import user_authorization
import user_registration
import matplotlib.pyplot as plt
import random


def check_user_authorization():
    if 'username' in session:
        user = session['username']
    else:
        user = None
    return user


def route_index():
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_weight()

    if request.method == 'POST':
        id_element = request.form['btn_id']  # del

        # если нажата кнопка удалить
        if id_element.split("_")[1] == 'del':
            model.remove_from_db(model.UserWeight, id_element.split("_")[0], session['user_id'])

    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):
        check_user = check_user_authorization()
        folder = f'static/users/{check_user.lower()}/graph/'
        graph_img_name = f'static/users/{check_user.lower()}/graph/g-{random.randint(1, 5000)}.png'

        # чистим пользовательскую папку с графиками
        modules.deleting_files.delete(folder)

        # запрос показателей веса пользователя из БД
        list = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
            model.UserWeight.created_at.desc()).all()

        # создается график
        modules.graph.create_graph(check_user, list, graph_img_name)

    else:
        return redirect(url_for('login'))

    return render_template('index.html',
                           title='Мой вес',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           graph_img_name=graph_img_name,
                           list=list,
                           session=check_user)


def route_weight(username):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_weight()

    if request.method == 'POST':
        id_element = request.form['btn_id']  # del

        # если нажата кнопка удалить
        if id_element.split("_")[1] == 'del':
            model.remove_from_db(model.UserWeight, id_element.split("_")[0], session['user_id'])

    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):
        check_user = check_user_authorization()
        folder = f'static/users/{check_user.lower()}/graph/'
        graph_img_name = f'static/users/{check_user.lower()}/graph/g-{random.randint(1, 5000)}.png'

        # чистим пользовательскую папку с графиками
        modules.deleting_files.delete(folder)

        # запрос показателей веса пользователя из БД
        list = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
            model.UserWeight.created_at.desc()).all()

        # создается график
        modules.graph.create_graph(check_user, list, graph_img_name)

    else:
        return redirect(url_for('login'))

    return render_template('weight_user.html',
                           title='Мой вес',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           graph_img_name=graph_img_name,
                           list=list,
                           session=check_user)


def route_add():
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_add(check_user_authorization())

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
            return redirect(url_for('weight', username=session['username']))

        except ValueError:
            flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
        except (TypeError, AttributeError):
            flash(f'В запросе к базе данных произошла ошибка!', category='danger')

    return render_template('add.html',
                           title='Новая запись',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           session=check_user_authorization())


def route_profile():
    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):
        return redirect(url_for('login_username', username=session['username']))

    # иначе показываем форму авторизации
    else:
        return redirect(url_for('login'))


def route_profile_username(username):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_profile_username()

    # если пользователь авторизован
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))

    return render_template('profile.html',
                           title=f'Профиль пользователя "{username}"',
                           menu=menu,
                           user_menu=user_menu,
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
            s = request.form['username']
            session['user_id'] = user_id
            flash(f'Вы успешно вошли как {s}!', category='info')
            return redirect(url_for('weight', username=session['username']))
        else:
            flash(f'Не верный логин или пароль', category='danger')

    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):

        # направляем в профиль
        return redirect(url_for('weight', username=session['username']))

    # иначе показываем форму авторизации
    else:
        menu = modules.menu.menu()
        user_menu = modules.menu.user_menu(check_user_authorization())
        submenu = modules.menu.submenu_login()

        return render_template('login.html',
                               title="Авторизация",
                               menu=menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               session=check_user_authorization())


def rout_logout():
    """Выход пользователя из системы, удаление сессии"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


def rout_registration():
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_registration()
    user_registration.user_registration_and_verification()

    return render_template('registration.html',
                           title='Регистрация',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           session=check_user_authorization())


def rout_pageNoteFound(error):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    return render_template('page_404.html',
                           title='Ошибка 404',
                           menu=menu,
                           user_menu=user_menu,
                           session=check_user_authorization()), 404
