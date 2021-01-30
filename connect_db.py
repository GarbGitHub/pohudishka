from datetime import timedelta
import os
from app_init import app
from flask_sqlalchemy import SQLAlchemy

app.permanent_session_lifetime = timedelta(days=10)
app.config.from_object('config_example')
# app.config.from_object('config')
db = SQLAlchemy(app)

