from app import db


class Users(db.Model):

    db.__tablename__ = 'users'
    id = db.Column(db.BIGINT, primary_key=True, index=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    username = db.Column(db.String)
    password = db.Column(db.String)
    embedding = db.Column(db.ARRAY(db.FLOAT))

    def __init__(self, username, password):
        self.username = username
        self.password = password


def users_get_all():
    return Users.query.all()


def add_user(user):
    db.session.add(user)
    db.session.commit()




