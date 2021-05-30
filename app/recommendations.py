import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity

from app import db
from app.users_orm import Users, users_get_all
from app.groups_orm import Groups, groups_get_all
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup, user_subscriptions_get_all


def get_user_group_recommendations(user_id, topn):
    user = Users.query.filter_by(id=user_id).first()
    groups = groups_get_all()
    group_embeddings = [g.embedding for g in groups]
    similarities = cosine_similarity([np.array(user.embedding)], np.array(group_embeddings))
    recommendations = [(groups[i].id, groups[i].name, similarities[0][i]) for i in range(len(group_embeddings))]

    result = db.session.query(UserSubscribes_toGroup.group_id).filter_by(subscriber_id=user_id).all()
    user_subscriptions_ids = [r[0] for r in result]
    recommendations = [recommendations[i] for i in range(len(recommendations)) if recommendations[i][0] not in user_subscriptions_ids]

    recommendations.sort(key=lambda x: x[2])
    recommendations = recommendations[::-1]

    return recommendations[:topn]