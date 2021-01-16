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
    name = db.Column(db.String(30), nullable=True)  # Имя
    lastname = db.Column(db.String(40), nullable=True)  # Отчество
    surname = db.Column(db.String(40), nullable=True)  # Фамилия
    gender = db.Column(db.SmallInteger, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    hometown = db.Column(db.String(40), nullable=True)
    user_height = db.Column(db.Float(10), default=0)
    photo_user = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<Profiles %r>' % self.user_id


class UserWeight(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    real_weight = db.Column(db.Float(10), default=0.0)
    real_progress = db.Column(db.Float(10), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return str(self.id)


def add_object_to_base(obj):
    """Добавление в базу новых записей"""
    db.session.add(obj)
    db.session.commit()


def remove_from_db(name_class, id_element, user_id):
    """Удаление из базы стен и блоков пользователем"""
    try:
        db.session.query(name_class).filter_by(id=id_element, user_id=user_id).delete()
        db.session.commit()
        flash(f'Успешно удалено из базы!', category='success')
    except ValueError:
        flash(f'Произошла ошибка!', category='success')
