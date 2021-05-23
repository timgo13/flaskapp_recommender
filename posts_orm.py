from sqlalchemy import Column, BIGINT, String, TIMESTAMP
from db import Base, db_instance


class PostsOrm(Base):
    __tablename__ = 'posts'
    id = Column(BIGINT, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    content = Column(String)
    creator_id = Column(BIGINT)
    child_post_id = Column(BIGINT)
    user_feed_id = Column(BIGINT)
    group_feed_id = Column(BIGINT)

    def __init__(self, content, creator_id, group_id):
        self.content = content
        self.creator_id = creator_id
        self.group_feed_id = group_id


def posts_get_all():
    return db_instance.current_session.query(PostsOrm).all()


def add_post(post):
    db_instance.current_session.add(post)
    db_instance.current_session.commit()