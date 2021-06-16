import numpy as np
import torch
from sentence_transformers import SentenceTransformer, models, util
from app.posts_orm import Posts, posts_get_all, add_post, posts_get_first
from app.groups_orm import Groups, groups_get_all
from app.users_orm import Users, users_get_all
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup, user_subscriptions_get_all
from app import db
from sqlalchemy.exc import ProgrammingError
from datetime import datetime

model_name = 'paraphrase-xlm-r-multilingual-v1'


class SBert:
    model = None
    gpu = False
    posts = None
    groups = None
    users = None
    user_subscriptions = None
    last_update_user = datetime.utcnow()

    def __init__(self):
        if torch.cuda.is_available():
            self.model = SentenceTransformer(model_name, device='cuda')
            self.gpu = True
        else:
            self.model = SentenceTransformer(model_name)

    def encode(self, text):
        return self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    def calc_all_post_embeddings(self):
        self.posts = posts_get_all()

        posts_content = [self.posts[i].content for i in range(len(self.posts))]
        post_embeddings = self.model.encode(posts_content, convert_to_numpy=True, normalize_embeddings=True)
        for i in range(len(self.posts)):
            self.posts[i].embedding = list(map(float, list(post_embeddings[i])))

        db.session.commit()

    def update_post_embeddings(self):
        self.posts = posts_get_all()
        new_posts = db.session.query(Posts).filter(Posts.embedding.is_(None)).all()
        posts_content = [p.content for p in new_posts]
        post_embeddings = self.model.encode(posts_content, convert_to_numpy=True, normalize_embeddings=True)
        for i in range(len(new_posts)):
            self.posts[new_posts[i].id].embedding = list(map(float, list(post_embeddings[i])))

        db.session.commit()

    def calc_all_group_embeddings(self):
        self.posts = posts_get_all()
        self.groups = groups_get_all()

        for g in self.groups:
            group_profile = Posts.query.filter_by(group_feed_id=g.id).all()
            group_profile_embeddings = [group_profile[i].embedding for i in range(len(group_profile))]
            group_embedding = np.mean(np.array(group_profile_embeddings), axis=0)
            g.embedding = list(map(float, list(group_embedding)))

        db.session.commit()

    def update_group_embeddings(self):
        self.posts = posts_get_all()
        self.groups = groups_get_all()

        for g in self.groups:
            new_group_profile = db.session.query(Posts).filter(Posts.id.is_(g.id), Posts.embedding.is_(None))
            new_group_profile_embeddings = [gp.embedding for gp in new_group_profile]
            group_embedding = np.mean(np.array(new_group_profile_embeddings.append(g.embedding)), axis=0)
            g.embedding = list(map(float, list(group_embedding)))

        db.session.commit()

    def calc_all_user_embeddings(self):
        self.users = users_get_all()
        self.groups = groups_get_all()
        self.user_subscriptions = user_subscriptions_get_all()

        for u in self.users:
            user_group_subs = UserSubscribes_toGroup.query.filter_by(subscriber_id=u.id).all()
            user_groups_subs_list = [user_group_subs[i].group_id for i in range(len(user_group_subs))]
            user_groups = db.session.query(Groups).filter(Groups.id.in_(user_groups_subs_list)).all()
            user_group_embeddings = [user_groups[i].embedding for i in range(len(user_groups))]
            user_embedding = np.mean(np.array(user_group_embeddings), axis=0)
            u.embedding = list(map(float, list(user_embedding)))

        db.session.commit()

    def update_all_embeddings(self):
        self.update_post_embeddings()
        self.update_group_embeddings()
        self.calc_all_user_embeddings()


def add_column(table, col_name):
    try:
        q = 'ALTER TABLE ' + str(table) + ' ADD column ' + str(col_name) + ' float[];'
        db.engine.execute(q)
        return 'Finished Successfully!'
    except ProgrammingError:
        db.session.rollback()
        return 'Add Column failed! (possible already existed)'


def add_embedding_column():
    r1 = add_column('users', 'embedding')
    r2 = add_column('groups', 'embedding')
    r3 = add_column('posts', 'embedding')
    return {"users": r1, "groups": r2, "posts": r3}




