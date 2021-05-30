import numpy as np
import torch
from sentence_transformers import SentenceTransformer, models, util
from app.posts_orm import Posts, posts_get_all, add_post, posts_get_first
from app.groups_orm import Groups, groups_get_all
from app.users_orm import Users, users_get_all
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup, user_subscribtions_get_all
from app import db
from sqlalchemy.exc import ProgrammingError

model_name = 'paraphrase-xlm-r-multilingual-v1'


class SBert:
    model = None
    gpu = False
    posts = None
    groups = None
    users = None
    user_subscribtions = None

    def __init__(self):
        if torch.cuda.is_available():
            self.model = SentenceTransformer(model_name, device='cuda')
            self.gpu = True
        else:
            self.model = SentenceTransformer(model_name)

    def calc_all_post_embeddings(self):
        self.posts = posts_get_all()
        posts_content = [self.posts[i].content for i in range(len(self.posts))]
        post_embeddings = self.model.encode(posts_content, convert_to_numpy=True, normalize_embeddings=True)
        for i in range(len(self.posts)):
            self.posts[i].embedding = list(map(float, list(post_embeddings[i])))

        db.session.commit()

    def test_calc_post_embeddings(self):
        self.posts = posts_get_first()
        posts_content = self.posts.content
        post_embeddings = self.model.encode(posts_content, convert_to_numpy=True, normalize_embeddings=True)
        self.posts.embedding = list(map(float, list(post_embeddings)))

        db.session.commit()

    def calc_all_group_embeddings(self):
        self.posts = posts_get_all()
        self.groups = groups_get_all()
        for g in self.groups:
            group_profile = Posts.query.filter_by(group_feed_id=g.id).all()
            group_profile_embeddings = [group_profile[i].embedding for i in range(len(group_profile))]
            group_profile_embeddings_array = np.array(group_profile_embeddings)
            group_embedding = np.mean(group_profile_embeddings_array, axis=0)
            g.embedding = list(map(float, list(group_embedding)))

        db.session.commit()

    def calc_all_user_embeddings(self):
        self.users = users_get_all()
        self.groups = groups_get_all()
        self.user_subscribtions = user_subscribtions_get_all()

        for u in self.users:
            user_group_subs = UserSubscribes_toGroup.query.filter_by(subscriber_id=u.id).all()
            user_groups_subs_list = [user_group_subs[i].group_id for i in range(len(user_group_subs))]
            user_groups = db.session.query(Groups).filter(Groups.id.in_(user_groups_subs_list)).all()
            user_group_embeddings = [user_groups[i].embedding for i in range(len(user_groups))]
            user_group_embeddings = np.array(user_group_embeddings)
            user_embedding = np.mean(user_group_embeddings, axis=0)
            u.embedding = list(map(float, list(user_embedding)))

        db.session.commit()


def add_column(table, col_name):
    try:
        q = 'ALTER TABLE ' + str(table) + ' ADD column ' + str(col_name) + ' float[];'
        db.engine.execute(q)
    except ProgrammingError:
        db.session.rollback()


def add_embedding_column():
    add_column('users', 'embedding')
    add_column('groups', 'embedding')
    add_column('posts', 'embedding')
