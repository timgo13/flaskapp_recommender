from sqlalchemy import Column, BIGINT, String, TIMESTAMP
from db import Base, db_instance


class UsersOrm(Base):

    __tablename__ = 'users'
    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password


def users_get_all():
    return db_instance.current_session.query(UsersOrm).all()


def add_user(user):
    db_instance.current_session.add(user)
    db_instance.current_session.commit()




