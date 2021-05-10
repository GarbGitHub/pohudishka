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
        data_list_weight = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
            model.UserWeight.created_at.desc()).all()

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
        if len(weight_users) > 0:
            for el in reversed(data_list_weight):
                date.append(el.created_at)
                y_list.append(el.real_weight)

            # создается график
            modules.graph.create_graph(graph_img_name, date, y_list)

    else:
        return redirect(url_for('login'))

    return render_template('weight_user.html',
                           title='Мой вес',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           graph_img_name=graph_img_name,
                           data_list_weight=data_list_weight,
                           weight_users=weight_users,
                           session=check_user)


def route_weight(page):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_weight()

    if request.method == 'POST':
        id_element = request.form['btn_id']  # del

        # если нажата кнопка удалить
        if id_element.split("_")[1] == 'del':
            model.remove_from_db(model.UserWeight, id_element.split("_")[0], session['user_id'])
            return redirect(url_for('weight', username=session['username']))

    # если пользователь авторизован
    if ('username' in session) and ('user_id' in session):
        check_user = check_user_authorization()
        folder = f'static/users/{check_user.lower()}/graph/'
        graph_img_name = f'static/users/{check_user.lower()}/graph/g-{random.randint(1, 5000)}.png'
        # чистим пользовательскую папку с графиками
        modules.deleting_files.delete(folder)

        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=session['user_id'], active='0')

        weight = modules.query_sql.real_weight_user(session['user_id'])

        # Количество записей для пагинации
        number_lines_user_weight = query_sql.row_count_table(name_class=model.UserWeight, user_id=session['user_id'])
        pagination = None
        if number_lines_user_weight > 0 and number_lines_user_weight % WEIGHT_PAGE != 0:
            pagination = page_pagination.links_pagination_generation(number_lines_user_weight, WEIGHT_PAGE, page)

        # запрос показателей веса пользователя из БД
        data_list_weight = model.UserWeight.query.filter_by(user_id=session['user_id']).order_by(
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
    else:
        return redirect(url_for('login'))

    return render_template('weight_user.html',
                           title='Мой вес',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           graph_img_name=graph_img_name,
                           # data_list_weight=data_list_weight,
                           weight=weight,
                           target=query_target,
                           weight_users=weight_users,
                           pagination=pagination,
                           title_date=title_date,
                           session=check_user)


def route_add():
    """Добавить вес пользователя"""
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_add(check_user_authorization())

    if ('username' in session) and ('user_id' in session):
        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=session['user_id'], active='0')
        print(query_target)
        if request.method == 'POST':
            try:
                real_weight = float((str(request.form['weight'])))
                print(real_weight, type(real_weight))
                # Записываем новый вес пользователя в базу
                obj = model.UserWeight(user_id=session['user_id'],
                                       real_weight=real_weight,
                                       created_at=datetime.now()
                                       )
                model.add_object_to_base(obj)

                # Обновляем статус цели, если она есть и цель достигнута
                if len(query_target) > 0 and real_weight <= query_target[0].user_target_weight:
                    obj_target = model.Target(
                        user_id=session['user_id'],
                        active='1',
                        finish_at=datetime.now()
                    )
                    model.edit_target_status(obj_target)

                flash(f'Запись успешно добавлена', category='success')
                return redirect(url_for('weight', username=session['username']))

            except ValueError:
                flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
            except (TypeError, AttributeError):
                flash(f'В запросе к базе данных произошла ошибка!', category='danger')

        return render_template('add.html',
                               title='Добавить вес',
                               menu=menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               session=check_user_authorization())
    else:
        return redirect(url_for('login'))


def route_add_target():
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_add(check_user_authorization())
    if ('username' in session) and ('user_id' in session):
        query_real_weight = modules.query_sql.real_weight_user(session['user_id'])
        query_target = None

        # Узнаем, есть ли активные цели status='0'
        count_target = db.session.execute(query_sql.count_target(user_id=session['user_id'], status='0')).fetchone()[
            'count']

        # Если есть цели получим о них данные
        if count_target > 0:
            # Запрос активной цели пользователя
            query_target = query_sql.user_targets(user_id=session['user_id'], active='0')

        if request.method == 'POST':
            id_element = request.form['btn_id']  # del

            # если нажата кнопка удалить
            if id_element.split("_")[1] == 'del':
                model.remove_from_db(model.Target, id_element.split("_")[0], session['user_id'])
                return redirect(url_for('add_target', username=session['username']))
            elif id_element.split("_")[1] == 'leave':
                return redirect(url_for('login_username', username=session['username']))
            else:
                try:
                    target = float((str(request.form['weight'])))
                    if query_real_weight == 0:
                        flash(f'Чтобы установить цель, сначала добавьте свой вес', category='danger')
                        return redirect(url_for('add'))
                    elif query_real_weight is not None and query_real_weight > target:
                        obj = model.Target(user_id=session['user_id'],
                                           user_target_weight=target,
                                           start_weight=query_real_weight,
                                           created_at=datetime.now()
                                           )
                        model.add_object_to_base(obj)
                        flash(f'Запись успешно добавлена', category='success')
                        return redirect(url_for('login_username', username=session['username']))
                    else:
                        flash(f'Цель должна быть меньше вашего текущего веса!', category='danger')
                except ValueError:
                    flash(f'Ошибка ввода! Недопустимый тип введенных данных', category='danger')
                except (TypeError, AttributeError):
                    flash(f'В запросе к базе данных произошла ошибка!', category='danger')

        return render_template('target.html',
                               title='Добавить цель',
                               menu=menu,
                               count_target=count_target,
                               user_menu=user_menu,
                               start_weight=query_real_weight,
                               target=query_target,
                               submenu=submenu,
                               session=check_user_authorization())
    else:
        return redirect(url_for('login'))


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
    submenu = modules.menu.submenu_profile_username(check_user_authorization())

    # если пользователь не авторизован
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    else:
        # Профиль и текущий вес пользователя
        profile_query, query_real_weight = modules.profile_user.profile(session['user_id'])

        # Запрос активной ('0') цели пользователя
        query_target = query_sql.user_targets(user_id=session['user_id'], active='0')

        # Индекс массы тела
        imt = modules.profile_user.calculate_imt(profile_query.user_height, query_real_weight)

        born = None
        age_text = None
        if profile_query.birthday is not None:
            born, age_text = modules.profile_user.calculate_age(profile_query.birthday)

        return render_template('profile.html',
                               title=f'Профиль пользователя "{username}"',
                               menu=menu,
                               user_menu=user_menu,
                               submenu=submenu,
                               profile=profile_query,
                               username=username,
                               weight=query_real_weight,
                               imt=imt,
                               born=born,
                               age_text=age_text,
                               target=query_target,
                               session=check_user_authorization())


def edit_profile(username):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    submenu = modules.menu.submenu_profile_username(check_user_authorization())

    # если пользователь авторизован
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))

    # Профиль и текущий вес пользователя
    profile_query, query_real_weight = modules.profile_user.profile(session['user_id'])

    if request.method == 'POST':
        gender = int(str(request.form['gender']))
        if gender == 0:
            photo_user = f'/static/images/users/avatars/v-{random.randint(1, 8)}.jpg'
        elif gender == 1:
            photo_user = f'/static/images/users/avatars/m-{random.randint(1, 8)}.jpg'
        else:
            photo_user = '/static/images/users/avatars/no_photo.jpg'

        obj_profile = model.Profiles(user_id=session['user_id'],
                                     name=str(request.form['name']),
                                     surname=str(request.form['surname']),
                                     birthday=request.form['birthday'],
                                     user_height=int(str(request.form['user_height'])),
                                     gender=gender,
                                     hometown=str(request.form['hometown']),
                                     photo_user=photo_user
                                     )
        model.edit_object_to_base(obj_profile)

    return render_template('edit_profile.html',
                           title=f'Редактировать профиль - "{username}"',
                           menu=menu,
                           user_menu=user_menu,
                           submenu=submenu,
                           username=username,
                           profile=profile_query,
                           weight=query_real_weight,
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

            menu = modules.menu.menu()
            user_menu = modules.menu.user_menu(check_user_authorization())
            return render_template('admin.html',
                                   title='Панель управления',
                                   menu=menu,
                                   user_menu=user_menu,
                                   session=check_user_authorization())
    else:
        return redirect(url_for('index'))


def rout_pageNoteFound(error):
    menu = modules.menu.menu()
    user_menu = modules.menu.user_menu(check_user_authorization())
    return render_template('page_404.html',
                           title='Ошибка 404',
                           menu=menu,
                           user_menu=user_menu,
                           session=check_user_authorization()), 404
