from flask import render_template, session, redirect, url_for, request, flash
from datetime import datetime
import model
import modules
from modules import menu, deleting_files, graph, query_sql, profile_user, page_pagination
import user_authorization
import user_registration
import random
from connect_db import db
from config import WEIGHT_PAGE


def check_user_authorization_new():
    if 'username' in session or 'user_id' in session:
        authorization = {'username': session['username'], 'user_id': session['user_id']}
    else:
        authorization = None
    return authorization


def check_user_authorization():
    if 'username' in session:
        user = session['username']
    else:
        user = None
    return user


def route_index():
    authorization = check_user_authorization_new()

    if authorization:
        page_menu = modules.menu.menu()
        submenu = modules.menu.submenu_weight()
        user_menu = modules.menu.user_menu(authorization['username'])
        username = authorization['username']

        if request.method == 'POST':
            id_element = request.form['btn_id']  # del

            # если нажата кнопка удалить
            if id_element.split("_")[1] == 'del':
                model.remove_from_db(model.UserWeight, id_element.split("_")[0], authorization['user_id'])

        folder = f'static/users/{username.lower()}/graph/'
        graph_img_name = f'static/users/{username.lower()}/graph/g-{random.randint(1, 5000)}.png'

        # чистим пользовательскую папку с графиками
        modules.deleting_files.delete(folder)

        # запрос показателей веса пользователя из БД
        data_list_weight = model.UserWeight.query.filter_by(user_id=authorization['user_id']).order_by(
            model.UserWeight.created_at.desc()).all()

        # формируем список показателей веса для итерации в шаблоне
        weight_users, counter = [], 0
        for el in reversed(data_list_weight):
            if len(weight_users) > 0:
                weight_users.insert(0, {'id': el.id,
                                        'real_weight': el.real_weight,
                                        'real_progress': round((el.real_weight - counter), 2),
                                        'created_at': el.created_at.strftime("%d.%m.%Y")})
            else:  # если первая запись в списке - устанавливаем динамике 0
                weight_users.insert(0, {'id': el.id,
                                        'real_weight': el.real_weight,
                                        'real_progress': 0,
                                        'created_at': el.created_at.strftime("%d.%m.%Y")})
            counter = el.real_weight

        date, y_list = [], []
        if len(weight_users) > 0:
            for el in reversed(data_list_weight):
                date.append(el.created_at)
                y_list.append(el.real_weight)

            # создается график
            modules.graph.create_graph(graph_img_name, date, y_list)

        return render_template('weight_user.html',
                               title='Мой вес',
                               menu=page_menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               graph_img_name=graph_img_name,
                               data_list_weight=data_list_weight,
                               weight_users=weight_users,
                               username=username)
    else:
        return redirect(url_for('login'))


def route_weight(page):
    authorization = check_user_authorization_new()

    if authorization:
        page_menu = modules.menu.menu()
        user_menu = modules.menu.user_menu(authorization['username'])
        submenu = modules.menu.submenu_weight()
        username = authorization['username']

        if request.method == 'POST':
            id_element = request.form['btn_id']  # del

            # если нажата кнопка удалить
            if id_element.split("_")[1] == 'del':
                model.remove_from_db(model.UserWeight, id_element.split("_")[0], authorization['user_id'])
                return redirect(url_for('weight', username=authorization['username']))

        folder = f'static/users/{username.lower()}/graph/'
        graph_img_name = f'static/users/{username.lower()}/graph/g-{random.randint(1, 5000)}.png'
        # чистим пользовательскую папку с графиками
        modules.deleting_files.delete(folder)

        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=authorization['user_id'], active='0')

        weight = modules.query_sql.real_weight_user(authorization['user_id'])

        # Количество записей для пагинации
        number_lines_user_weight = query_sql.row_count_table(name_class=model.UserWeight,
                                                             user_id=authorization['user_id'])
        pagination = None
        if number_lines_user_weight > 0 and number_lines_user_weight % WEIGHT_PAGE != 0:
            pagination = page_pagination.links_pagination_generation(number_lines_user_weight, WEIGHT_PAGE, page)

        # запрос показателей веса пользователя из БД
        data_list_weight = model.UserWeight.query.filter_by(user_id=authorization['user_id']).order_by(
            model.UserWeight.created_at.desc()).paginate(page, WEIGHT_PAGE, False).items

        # формируем список показателей веса для итерации в шаблоне
        weight_users, counter = [], 0
        for el in reversed(data_list_weight):
            if len(weight_users) > 0:
                weight_users.insert(0, {'id': el.id,
                                        'real_weight': el.real_weight,
                                        'real_progress': round((el.real_weight - counter), 2),
                                        'created_at': el.created_at.strftime("%d.%m.%Y")})
            else:  # если первая запись в списке устанавливаем динамике 0
                weight_users.insert(0, {'id': el.id,
                                        'real_weight': el.real_weight,
                                        'real_progress': 0,
                                        'created_at': el.created_at.strftime("%d.%m.%Y")})
            counter = el.real_weight

        date, y_list = [], []
        title_date = str(datetime.now().strftime("%d.%m.%Y"))
        if len(weight_users) > 0:
            for el in reversed(data_list_weight):
                date.append(el.created_at)
                y_list.append(el.real_weight)

            # создается график
            title_date = modules.graph.create_graph(graph_img_name, date, y_list)

        return render_template('weight_user.html',
                               title='Мой вес',
                               menu=page_menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               graph_img_name=graph_img_name,
                               # data_list_weight=data_list_weight,
                               weight=weight,
                               target=query_target,
                               weight_users=weight_users,
                               pagination=pagination,
                               title_date=title_date,
                               username=username)

    else:
        return redirect(url_for('login'))


def route_add():
    """Добавить вес пользователя"""
    authorization = check_user_authorization_new()

    if authorization:
        page_menu = modules.menu.menu()
        user_menu = modules.menu.user_menu(authorization['username'])
        submenu = modules.menu.submenu_add(authorization['username'])
        username = authorization['username']

        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=authorization['user_id'], active='0')

        if request.method == 'POST':
            try:
                real_weight = float((str(request.form['weight'])))

                # Записываем новый вес пользователя в базу
                obj = model.UserWeight(user_id=authorization['user_id'],
                                       real_weight=real_weight,
                                       created_at=datetime.now()
                                       )
                model.add_object_to_base(obj)

                # Обновляем статус цели, если она есть и цель достигнута
                if len(query_target) > 0 and real_weight <= query_target[0].user_target_weight:
                    obj_target = model.Target(
                        user_id=authorization['user_id'],
                        active='1',
                        finish_at=datetime.now()
                    )
                    model.edit_target_status(obj_target)

                flash(f'Запись успешно добавлена', category='success')
                return redirect(url_for('weight', username=authorization['username']))

            except ValueError:
                flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
            except (TypeError, AttributeError):
                flash(f'В запросе к базе данных произошла ошибка!', category='danger')

        return render_template('add.html',
                               title='Добавить вес',
                               menu=page_menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               username=username)
    else:
        return redirect(url_for('login'))


def route_add_target():
    authorization = check_user_authorization_new()

    if authorization:
        page_menu = modules.menu.menu()
        user_menu = modules.menu.user_menu(authorization['username'])
        submenu = modules.menu.submenu_add(authorization['username'])
        username = authorization['username']
        query_real_weight = modules.query_sql.real_weight_user(authorization['user_id'])
        query_target = None

        # Узнаем, есть ли активные цели status='0'
        count_target = db.session.execute(query_sql.count_target(user_id=authorization['user_id'],
                                                                 status='0')).fetchone()['count']

        # Если есть цели получим о них данные
        if count_target > 0:
            # Запрос активной цели пользователя
            query_target = query_sql.user_targets(user_id=authorization['user_id'], active='0')

        if request.method == 'POST':
            id_element = request.form['btn_id']  # del

            # если нажата кнопка удалить
            if id_element.split("_")[1] == 'del':
                model.remove_from_db(model.Target, id_element.split("_")[0], authorization['user_id'])
                return redirect(url_for('add_target', username=authorization['username']))
            elif id_element.split("_")[1] == 'leave':
                return redirect(url_for('login_username', username=authorization['username']))
            else:
                try:
                    target = float((str(request.form['weight'])))
                    if query_real_weight == 0:
                        flash(f'Чтобы установить цель, сначала добавьте свой вес', category='danger')
                        return redirect(url_for('add'))
                    elif query_real_weight is not None and query_real_weight > target:
                        obj = model.Target(user_id=authorization['user_id'],
                                           user_target_weight=target,
                                           start_weight=query_real_weight,
                                           created_at=datetime.now()
                                           )
                        model.add_object_to_base(obj)
                        flash(f'Запись успешно добавлена', category='success')
                        return redirect(url_for('login_username', username=authorization['username']))
                    else:
                        flash(f'Цель должна быть меньше вашего текущего веса!', category='danger')
                except ValueError:
                    flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
                except (TypeError, AttributeError):
                    flash(f'В запросе к базе данных произошла ошибка!', category='danger')

        return render_template('target.html',
                               title='Добавить цель',
                               menu=page_menu,
                               count_target=count_target,
                               user_menu=user_menu,
                               start_weight=query_real_weight,
                               target=query_target,
                               submenu=submenu,
                               username=username)
    else:
        return redirect(url_for('login'))


def route_profile():
    authorization = check_user_authorization_new()
    # если пользователь авторизован
    if authorization:
        return redirect(url_for('login_username', username=authorization['username']))

    # иначе показываем форму авторизации
    else:
        return redirect(url_for('login'))


def route_profile_username(user):
    """Данные в профиле привязать к id пользователя так как это профиль могут просматривать другие пользователи"""
    authorization = check_user_authorization_new()

    # если пользователь не авторизован или это не его профиль
    if authorization is None or authorization['username'] != user:
        return redirect(url_for('login'))

    else:
        page_menu = modules.menu.menu()
        user_menu = modules.menu.user_menu(authorization['username'])
        submenu = modules.menu.submenu_profile_username(authorization['username'])
        # username = authorization['username']

        # Профиль и текущий вес пользователя
        profile_query, query_real_weight = modules.profile_user.profile(authorization['user_id'])  # !

        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=authorization['user_id'], active='0')  # !

        # Индекс массы тела
        imt = modules.profile_user.calculate_imt(profile_query.user_height, query_real_weight)

        born = None
        age_text = None
        if profile_query.birthday is not None:
            born, age_text = modules.profile_user.calculate_age(profile_query.birthday)

        return render_template('profile.html',
                               title=f'Профиль пользователя "{user}"',
                               menu=page_menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               profile=profile_query,
                               username=user,
                               weight=query_real_weight,
                               imt=imt,
                               born=born,
                               age_text=age_text,
                               target=query_target)


def edit_profile(user):
    authorization = check_user_authorization_new()

    # если пользователь не авторизован или это не его профиль
    if authorization is None or authorization['username'] != user:
        return redirect(url_for('login'))

    page_menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(authorization['username'])
    submenu = modules.menu.submenu_profile_username(authorization['username'])
    username = authorization['username']

    # Профиль и текущий вес пользователя
    profile_query, query_real_weight = modules.profile_user.profile(session['user_id'])

    if request.method == 'POST':
        gender = int(str(request.form['gender']))
        if gender == 0:
            photo_user = f'/static/images/users/avatars/v-{random.randint(1, 11)}.jpg'
        elif gender == 1:
            photo_user = f'/static/images/users/avatars/m-{random.randint(1, 11)}.jpg'
        else:
            photo_user = '/static/images/users/avatars/no_photo.jpg'

        obj_profile = model.Profiles(user_id=authorization['user_id'],
                                     name=str(request.form['name']),
                                     surname=str(request.form['surname']),
                                     birthday=request.form['birthday'],
                                     user_height=int(str(request.form['user_height'])),
                                     gender=gender,
                                     hometown=str(request.form['hometown']),
                                     photo_user=photo_user)
        model.edit_object_to_base(obj_profile)

    return render_template('edit_profile.html',
                           title=f'Редактировать профиль - "{username}"',
                           menu=page_menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           username=username,
                           profile=profile_query,
                           weight=query_real_weight)


def route_login():
    authorization = check_user_authorization_new()

    if authorization:
        return redirect(url_for('weight', username=session['username']))

    else:
        page_menu = modules.menu.menu()
        submenu = modules.menu.submenu_login()

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
                flash(f'Вы успешно вошли как {username}!!', category='info')
                return redirect(url_for('weight', username=session['username']))
            else:
                flash(f'Не верный логин или пароль', category='danger')

        return render_template('login.html',
                               title="Авторизация",
                               menu=page_menu,
                               submenu=submenu)


def rout_logout():
    """Выход пользователя из системы, удаление сессии"""

    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


def rout_registration():
    authorization = check_user_authorization_new()
    if authorization:
        return redirect(url_for('profile'))

    page_menu = modules.menu.menu()
    submenu = modules.menu.submenu_registration()
    result = user_registration.user_registration_and_verification()
    if result:
        return redirect(url_for('login'))
    return render_template('registration.html',
                           menu=page_menu,
                           submenu=submenu,
                           title='Регистрация')


def rout_admin():
    # если пользователь авторизован

    if ('username' in session) and ('user_id' in session):
        rang = model.Users.query.with_entities(model.Users.rang).filter_by(id=session['user_id']).first_or_404()
        if rang[0] != 1:
            return redirect(url_for('profile', username=session['username']))

        else:
            if request.method == 'POST':
                pass
                # start_app_ping = request.form['btn_start_ping']  # del
                # # если нажата кнопка удалить
                # if start_app_ping == 'start_ping':
                #     modules.server_ping.app_ping()

            page_menu = modules.menu.menu()
            user_menu = modules.menu.user_menu(check_user_authorization())
            return render_template('admin.html',
                                   title='Панель управления',
                                   menu=page_menu,
                                   user_menu=user_menu,
                                   session=check_user_authorization())
    else:
        return redirect(url_for('index'))


def page_note_found(error):
    page_menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    return render_template('page_404.html',
                           title='Ошибка 404',
                           menu=page_menu,
                           user_menu=user_menu,
                           session=check_user_authorization()), 404
