from datetime import datetime

from flask import flash

from connect_db import db


class Users(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(360), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    is_deleted = db.Column(db.SmallInteger, default=0)
    rang = db.Column(db.SmallInteger, default=0)

    def __repr__(self):
        return '<Users %r>' % self.id


class Profiles(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    name = db.Column(db.String(30), nullable=False, default='')  # Имя
    surname = db.Column(db.String(40), nullable=False, default='')  # Фамилия
    gender = db.Column(db.SmallInteger, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    hometown = db.Column(db.String(40), nullable=False, default='')
    user_height = db.Column(db.Integer, default=0)  # Рос
    photo_user = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return "[{name: '%s'}, {surname: '%s'}, {user_height: %r}, {gender: %r}, {birthday: '%s'}, {hometown: '%s'}, " \
               "{photo_user: '%s'}]" % (self.name, self.surname, self.user_height, self.gender,
                                        self.birthday, self.hometown, self.photo_user)


class UserWeight(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    real_weight = db.Column(db.Float(10), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "'id': %r, 'user_id': %r, 'real_weight': %r, 'created_at': %s" % (
            self.id, self.user_id, self.real_weight, self.created_at)


class Target(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    active = db.Column(db.CHAR, nullable=False, default=0)
    start_weight = db.Column(db.Float(10), default=0.0)
    user_target_weight = db.Column(db.Float(10), nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    finish_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "'id': %r, 'user_id': %r, 'active': %r, 'start_weight': %r, 'user_target_weight': %r, 'created_at': " \
               "%s, 'finish_at': %s" % (
                   self.id, self.user_id, self.active, self.start_weight, self.user_target_weight, self.created_at,
                   self.finish_at)


def add_object_to_base(obj):
    """Добавление в базу новых записей"""
    db.session.add(obj)
    db.session.commit()


def edit_object_to_base(obj_profile):
    """Редактирование профиля"""
    print(obj_profile)
    try:
        profile = db.session.query(Profiles).filter(Profiles.user_id == obj_profile.user_id).first()
        profile.name = obj_profile.name
        profile.surname = obj_profile.surname
        profile.gender = obj_profile.gender
        profile.birthday = obj_profile.birthday
        profile.hometown = obj_profile.hometown
        profile.user_height = obj_profile.user_height
        profile.photo_user = obj_profile.photo_user
        db.session.commit()
        flash(f'Профиль успешно обновлен!', category='success')
    except:
        flash(f'Произошла ошибка! Error in def update_state', category='danger')


def edit_target_status(obj_target):
    """Редактирование статусов целей пользователя"""
    print('obj_target', obj_target)
    try:
        target = db.session.query(Target).filter(Target.user_id == obj_target.user_id, Target.active == '0').first()
        target.active = obj_target.active
        target.finish_at = obj_target.finish_at
        db.session.commit()
        return flash(f'Поздравляем! Вы достигли поставленной цели. Так держать!', category='success')
    except:
        return flash(f'При обновлении статуса цели произошла ошибка', category='danger')


def remove_from_db(name_class, id_element, user_id):
    """Удаление из базы"""
    try:
        db.session.query(name_class).filter_by(id=id_element, user_id=user_id).delete()
        db.session.commit()
        flash(f'Успешно удалено из базы!', category='success')
    except ValueError:
        flash(f'Произошла ошибка!', category='success')
