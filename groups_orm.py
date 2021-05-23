from sqlalchemy import Column, BIGINT, String, TIMESTAMP, text
from db import Base, db_instance


class GroupsOrm(Base):
    __tablename__ = 'groups'
    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    name = Column(String)
    creator_id = Column(BIGINT)

    def __init__(self, name, creator_id):
        self.name = name
        self.creator_id = creator_id


def groups_get_all():
    return db_instance.current_session.query(GroupsOrm).all()


def add_group(group):
    db_instance.current_session.add(group)
    db_instance.current_session.commit()
