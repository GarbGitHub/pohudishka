# Профиль пользователя model.Profiles + текущий вес model.UserWeight
import model
from connect_db import db

def profile_user(user_id):
    try:
        profile = f'SELECT p.*, uw.real_weight ' \
                  f'FROM user_weight ' \
                  f'AS uw ' \
                  f'JOIN profiles ' \
                  f'AS p ' \
                  f'ON uw.user_id  = p.user_id ' \
                  f'WHERE uw.user_id = {user_id} ' \
                  f'ORDER BY uw.created_at DESC LIMIT 1'
        return profile
    except:
        print('error')


def count_target(user_id, status='0'):
    """Количество целей: активные (0) или не активные (1)"""

    try:
        count = """SELECT COUNT(*) FROM target WHERE user_id={!r} AND active ={!r}""".format(user_id, status)
        return count
    except:
        print('error')


def user_targets(user_id, active) -> list:
    """Возвращает активные (0) или не активные (1) цели пользователя"""

    target = model.Target.query.filter_by(user_id=user_id, active=active).order_by(
        model.Target.created_at.desc()).all()
    return target


def row_count_table(name_class, user_id: int) -> int:
    """Возвращает количество строк в любой таблице"""

    count = db.session.query(name_class).filter_by(user_id=user_id).count()
    db.session.commit()
    return count


def real_weight_user(user_id):
    """Текущий вес пользователя"""

    real_weight = model.UserWeight.query.with_entities(model.UserWeight.real_weight).filter_by(
        user_id=user_id).order_by(model.UserWeight.created_at.desc()).first_or_404()
    real_weight = real_weight.real_weight if real_weight else 0
    return real_weight
