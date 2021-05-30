from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


from app import routes, groups_orm, users_orm, posts_orm


def create_app():
    app.config.from_object(Config)
    db.app = app
    db.init_app(app)

    return app