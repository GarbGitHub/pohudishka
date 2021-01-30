from datetime import date
import model
from modules import query_sql


def profile(user_id):
    # Запрос текущего веса пользователя (c)
    query_real_weight = query_sql.real_weight_user(user_id)
    print(query_real_weight)

    # Запрос данных пользователя
    profile_query = model.Profiles.query.filter_by(user_id=user_id).first()
    print(profile_query)
    return profile_query, query_real_weight


def calculate_age(born):
    """Рассчитывает вес пользователя"""

    today = date.today()
    user_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    age_text = 'лет'

    if 4 < user_age < 21:
        age_text = 'лет'

    elif 1 < user_age % 10 < 5:
        age_text = 'года'

    elif user_age % 10 == 1:
        age_text = 'год'

    return user_age, age_text


def calculate_imt(user_height, real_weight):
    """Рассчитывает ИМТ (индекс массы тела) пользователя"""

    imt_message = (
        'Выраженный дефицит массы тела',
        'Недостаточная (дефицит) массы тела',
        'Норма',
        'Избыточная масса тела (предожирение)',
        'Ожирение первой степени',
        'Ожирение второй степени',
        'Ожирение третьей степени (морбидное)'
    )

    if real_weight is not None:
        if user_height != 0:
            print(real_weight, user_height)
            imt = real_weight / ((user_height / 100) * (user_height / 100))
            print(imt)
        else:
            imt = 0

        if imt == 0:
            mess, bg_color = '', ''
        elif 0 < imt < 15.99:
            mess = imt_message[0]
            bg_color = 'text-danger'
        elif 16 < imt < 18.49:
            mess = imt_message[1]
            bg_color = 'text-primary'
        elif 18.50 < imt < 24.99:
            mess = imt_message[2]
            bg_color = 'text-success'
        elif 25.00 < imt < 29.99:
            mess = imt_message[3]
            bg_color = 'text-primary'
        elif 30.00 < imt < 34.99:
            mess = imt_message[4]
            bg_color = 'text-danger'
        elif 35.00 < imt < 39.99:
            mess = imt_message[5]
            bg_color = 'text-danger'
        else:
            mess = imt_message[6]
            bg_color = 'text-danger'

        result = {'imt': round(imt, 2), 'mess': mess, 'bg_color': bg_color}
        return result
    else:
        return {'imt': round(0), 'mess': '', 'bg_color': ''}
