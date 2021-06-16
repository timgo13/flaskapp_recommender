from flask import Flask, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from app.embedding import add_embedding_column
from app.users_orm import Users, users_get_all
from app.reddit_data import insert_test_reddit, insert_test_user
from app.embedding import SBert
from app.recommendations import get_user_group_recommendations, get_post_group_recommendations
from app.user_subscribes_to_group_orm import UserSubscribes_toGroup

from app import app
from app import db

sbert = SBert()


@app.route('/usertest', methods=['GET'])
def db_user_test():
    error_output = False
    try:
        user = users_get_all()
    except MultipleResultsFound as e:
        error_output = str(e)
    except NoResultFound as e:
        error_output = str(e)

    return jsonify({"first_user_name": user[0].username, "error": error_output})


@app.route('/add_embedding_column', methods=['GET'])
def col_test():
    result = add_embedding_column()
    return jsonify(result)


@app.route('/insert_test_reddit', methods=['GET'])
def reddit_data():
    try:
        add_embedding_column()
        insert_test_reddit()
        return jsonify('Finished!')
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/test_user', methods=['GET'])
def test_user():
    insert_test_user()
    user_names = ['test_user1', 'test_user2']
    result = db.session.query(Users.id).filter(Users.username.in_(user_names)).all()
    test_user_ids = [r[0] for r in result]
    return jsonify(user_names, test_user_ids)

@app.route('/sbert', methods=['GET'])
def test_sbert():
    # sbert.calc_all_post_embeddings()
    # sbert.calc_all_group_embeddings()
    #sbert.calc_all_user_embeddings()
    sbert.update_all_embeddings()

    return jsonify(sbert.groups[0].embedding)


@app.route('/api/recommendations/user_group_recommendations/<user_id>', methods=['GET'])
def user_group_recommendations(user_id):
    user = Users.query.filter_by(id=user_id).first()
    count_subscriptions = UserSubscribes_toGroup.query.filter_by(subscriber_id=user_id).count()
    recommendations = get_user_group_recommendations(user_id, 5)
    recommendations_ids = [r[0] for r in recommendations]
    recommendations_names = [r[1] for r in recommendations]

    result = {'user_id': user_id, 'user_name': user.username, 'count_subscriptions': count_subscriptions,
              'group_id_recommendations': recommendations_ids,'group_recommendations': recommendations_names}

    response = jsonify(result)
    return response


@app.route('/api/recommendations/post_group_recommendations', methods=['POST'])
def get_post_recommendations():

    content = request.json
    post = content['post']
    group = content['group']
    recommendations = get_post_group_recommendations(sbert, post, group, 5)
    recommendation_names = [r[1] for r in recommendations]
    recommendation_ids = [r[0] for r in recommendations]

    return jsonify(recommendation_ids, recommendation_names)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

