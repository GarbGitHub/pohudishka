from datetime import timedelta

from app_init import app
from flask_sqlalchemy import SQLAlchemy

app.permanent_session_lifetime = timedelta(days=10)
app.config.from_object('config')
db = SQLAlchemy(app)

