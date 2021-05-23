import pandas as pd
from users_orm import UsersOrm, add_user, users_get_all
from posts_orm import PostsOrm, add_post
from groups_orm import GroupsOrm, add_group


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
        user = UsersOrm(u, '123')
        add_user(user)

    # Groups
    count_reddits = df['subreddit'].value_counts()
    reddit_groups = list(count_reddits.index)
    for g in reddit_groups:
        group = GroupsOrm(g, 1)
        add_group(group)

    # Posts
    for i, row in df.iterrows():
        text = str(row['title']) + ' ' + str(row['selftext'])
        post = PostsOrm(text,
                        (top_user.index(str(row['author'])) + 1),
                        (reddit_groups.index(str(row['subreddit'])) + 1))
        add_post(post)

