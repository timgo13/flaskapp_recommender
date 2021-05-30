import pandas as pd
import numpy as np
from app.users_orm import Users, add_user, users_get_all
from app.posts_orm import Posts, add_post
from app.groups_orm import Groups, add_group, groups_get_all
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup, add_user_subscriptions
from app import db
from sqlalchemy.exc import IntegrityError


file_name = '/home/ubuntu/Documents/Praxisprojekt/german_reddit_submissions_20k.pickle'
top_n_user = 1000


def insert_test_reddit():
    df = pd.read_pickle(file_name)

    # User
    df = df[df['author'] != '[deleted]']
    count_sub = df['author'].value_counts()
    top_user = list(count_sub.index[:top_n_user])
    df = df[df['author'].isin(top_user)]
    for u in top_user:
        user = Users(u, '123')
        add_user(user)

    # Groups
    count_reddits = df['subreddit'].value_counts()
    reddit_groups = list(count_reddits.index)
    for g in reddit_groups:
        group = Groups(g, 1)
        add_group(group)

    # Posts
    for i, row in df.iterrows():
        text = str(row['title']) + ' ' + str(row['selftext'])
        post = Posts(text,
                     (top_user.index(str(row['author'])) + 1),
                     (reddit_groups.index(str(row['subreddit'])) + 1))
        add_post(post)

    # User Subscriptions
    for u in top_user:
        user_profile = df[df['author'] == u]
        user_groups = list(user_profile['subreddit'].unique())
        user_id = top_user.index(u) + 1
        for g_name in user_groups:
            user_subscription = UserSubscribes_toGroup(user_id, (reddit_groups.index(g_name) + 1))
            add_user_subscriptions(user_subscription)


def insert_test_user():
    # Youtube/ Influencer User
    groups = [Groups.query.filter_by(name='Papaplatte').first(), Groups.query.filter_by(name='PietSmiet').first(),
              Groups.query.filter_by(name='Klengan').first()]
    group_embeddings = [g.embedding for g in groups]
    new_user = Users('test_user1', '123')
    new_user.embedding = list(map(float, list(np.mean(np.array(group_embeddings), axis=0))))
    try:
        add_user(new_user)
    except IntegrityError:
        db.session.rollback()
        pass

    user = Users.query.filter_by(username=new_user.username).first()
    for g in groups:
        try:
            new_user_sub = UserSubscribes_toGroup(user.id, g.id)
            add_user_subscriptions(new_user_sub)
        except IntegrityError:
            db.session.rollback()
            pass


    # Alt. Fakten/ AFD
    groups = [Groups.query.filter_by(name='AFD').first(), Groups.query.filter_by(name='Volksverpetzer').first(),
              Groups.query.filter_by(name='alt_fakten').first()]
    group_embeddings = [g.embedding for g in groups]
    new_user = Users('test_user2', '123')
    new_user.embedding = list(map(float, list(np.mean(np.array(group_embeddings), axis=0))))
    try:
        add_user(new_user)
    except IntegrityError:
        db.session.rollback()
        pass

    user = Users.query.filter_by(username=new_user.username).first()
    for g in groups:
        try:
            new_user_sub = UserSubscribes_toGroup(user.id, g.id)
            add_user_subscriptions(new_user_sub)
        except IntegrityError:
            db.session.rollback()
            pass




