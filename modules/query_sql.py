# Профиль пользователя model.Profiles + текущий вес model.UserWeight
import model


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


def count_target(user_id):
    """Количество целей"""

    try:
        count = "SELECT COUNT(*) FROM target WHERE user_id=%r" % user_id
        return count
    except:
        print('error')


def user_targets(user_id, active) -> list:
    """Возвращает активные (0) или не активные (1) цели пользователя"""

    status = active if active == '0' else '1'
    target = model.Target.query.filter_by(user_id=user_id, active=status).order_by(
        model.Target.created_at.desc()).all()
    return target


def real_weight_user(user_id):
    """Текущий вес пользователя"""

    real_weight = model.UserWeight.query.with_entities(model.UserWeight.real_weight).filter_by(
        user_id=user_id).order_by(model.UserWeight.created_at.desc()).first()
    real_weight = real_weight.real_weight if real_weight else 0
    return real_weight
