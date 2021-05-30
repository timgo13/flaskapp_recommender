import pandas as pd
from app.users_orm import Users, add_user, users_get_all
from app.posts_orm import Posts, add_post
from app.groups_orm import Groups, add_group
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup, add_user_subscribtions


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

    # User Subscribtions
    for u in top_user:
        user_profile = df[df['author'] == u]
        user_groups = list(user_profile['subreddit'].unique())
        user_id = top_user.index(u) + 1
        for g_name in user_groups:
            user_subscribtion = UserSubscribes_toGroup(user_id, (reddit_groups.index(g_name) + 1))
            add_user_subscribtions(user_subscribtion)


