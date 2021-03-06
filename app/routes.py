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
from app import db, scheduler

sbert = SBert()

# Deactivate Update Embeddings for Debugging
# scheduler.add_job(id='Update Task', func=sbert.update_all_embeddings(), trigger='interval', hours=24)


@app.route('/usertest', methods=['GET'])
def db_user_test():
    r"""
    Test to check the database connection
    :return: json
    """
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
    r"""
    Adds embedding column to the tables
    :return: json, finished or error
    """
    result = add_embedding_column()
    return jsonify(result)


@app.route('/insert_test_reddit', methods=['GET'])
def reddit_data():
    r"""
    Inserts the reddit test data in the db
    :return: json, finished or error
    """
    try:
        add_embedding_column()
        insert_test_reddit()
        return jsonify('Finished!')
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/test_user', methods=['GET'])
def test_user():
    r"""
    Inserts test users into db
    :return: json, { user_names, user_ids }
    """
    insert_test_user()
    user_names = ['test_user1', 'test_user2']
    result = db.session.query(Users.id).filter(Users.username.in_(user_names)).all()
    test_user_ids = [r[0] for r in result]
    return jsonify(user_names, test_user_ids)


@app.route('/sbert/<text>', methods=['GET'])
def test_sbert(text):
    r"""
    For testing the sbert model, encodes given text to embedding
    :param text: string, input text
    :return: json, embedding vector/ array
    """
    embedding = sbert.encode(text)

    return jsonify(embedding)


@app.route('/api/recommendations/user_group_recommendations/<user_id>', methods=['GET'])
def user_group_recommendations(user_id):
    r"""
    Returns group recommendations for a given user
    :param user_id: int
    :return: json, recommendations { userid, username, sub_count, list_group_ids, list_group_names }
    """
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
    r"""
    Return group recommendations for a given text/ post, (in connection with given main group)
    :param json_post: { post, group }
    :return: json, recommendations { list_group_ids, list_group_names }
    """
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

