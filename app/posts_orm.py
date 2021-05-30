from app import db


class Posts(db.Model):
    db.__tablename__ = 'posts'
    id = db.Column(db.BIGINT, primary_key=True, index=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    content = db.Column(db.String)
    creator_id = db.Column(db.BIGINT)
    child_post_id = db.Column(db.BIGINT)
    user_feed_id = db.Column(db.BIGINT)
    group_feed_id = db.Column(db.BIGINT)
    embedding = db.Column(db.ARRAY(db.FLOAT))

    def __init__(self, content, creator_id, group_id):
        self.content = content
        self.creator_id = creator_id
        self.group_feed_id = group_id


def posts_get_all():
    return Posts.query.all()


def posts_get_first():
    return Posts.query.first()


def add_post(post):
    db.session.add(post)
    db.session.commit()
