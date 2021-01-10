from datetime import datetime
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


class UserWeight(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    real_weight = db.Column(db.Float(10), default=0.0)
    real_progress = db.Column(db.Float(10), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Users %r>' % self.user_id


def add_object_to_base(obj):
    """Добавление в базу новых записей"""
    db.session.add(obj)
    db.session.commit()
