from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

app = Flask(__name__)
db = SQLAlchemy()
scheduler = APScheduler()
app.config.from_object(Config)
db.app = app
db.init_app(app)

from app import routes, groups_orm, users_orm, posts_orm, embedding


def create_app():
    app.config.from_object(Config)
    db.app = app
    db.init_app(app)

    return app