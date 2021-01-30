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


def real_weight_user(user_id):
    """Текущий вес пользователя"""

    real_weight = model.UserWeight.query.with_entities(model.UserWeight.real_weight).filter_by(
        user_id=user_id).order_by(model.UserWeight.created_at.desc()).first()
    real_weight = real_weight.real_weight if real_weight else 0
    return real_weight
