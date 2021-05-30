from app import db


class UserSubscribes_toGroup(db.Model):

    db.__tablename__ = 'user_subscribes_to_group'
    id = db.Column(db.BIGINT, primary_key=True, index=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    subscriber_id = db.Column(db.BIGINT)
    group_id = db.Column(db.BIGINT)

    def __init__(self, sub_id, group_id):
        self.subscriber_id = sub_id
        self.group_id = group_id


def user_subscribtions_get_all():
    return UserSubscribes_toGroup.query.all()


def add_user_subscribtions(user_subscribtions):
    db.session.add(user_subscribtions)
    db.session.commit()
