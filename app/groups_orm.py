from app import db


class Groups(db.Model):
    db.__tablename__ = 'groups'
    id = db.Column(db.BIGINT, primary_key=True, index=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    name = db.Column(db.String)
    creator_id = db.Column(db.BIGINT)
    embedding = db.Column(db.ARRAY(db.FLOAT))

    def __init__(self, name, creator_id):
        self.name = name
        self.creator_id = creator_id


def groups_get_all():
    return Groups.query.all()


def add_group(group):
    db.session.add(group)
    db.session.commit()
