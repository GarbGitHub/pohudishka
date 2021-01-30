def menu():
    """Общее меню"""

    menu = []
    return menu


def user_menu(user):
    """Меню для авторизованных пользователей"""

    if user is not None:
        user_menu = [{"name": "Моя страница", "url": f"/profile/{user}/"},
                     {"name": "Мой вес", "url": f"/profile/{user}/weight/"},
                     {"name": "Добавить вес", "url": "/add/"},
                     {"name": "Добавить цель", "url": "/add_target/"}]
    else:
        user_menu = []

    return user_menu


def submenu_weight():
    """Меню для раздела Мой вес"""

    submenu = [{"name": "Добавить", "url": "/add/"}]
    return submenu


def submenu_add(user):
    """Меню для раздела Добавить новый вес"""
    if user is not None:
        submenu = [{"name": "Мой вес", "url": f"/profile/{user}/weight/"}]
    else:
        submenu = []
    return submenu


def submenu_profile_username(user):
    """Меню для раздела Профиль пользователя"""

    submenu = [{"name": "Редактировать профиль", "url": f"/profile/{user}/edit_profile/"},
               {"name": "Выйти", "url": "/logout"}]
    return submenu


def submenu_login():
    """Меню для страницы Авторизация"""

    submenu = [{"name": "Регистрация", "url": "/registration/"}]
    return submenu


def submenu_registration():
    """Меню для страницы Авторизация"""

    submenu = [{"name": "Войти", "url": "/login"}]
    return submenu
