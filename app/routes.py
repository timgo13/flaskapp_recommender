from flask import Flask, jsonify
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from app.embedding import add_embedding_column
from app.users_orm import users_get_all
from app.reddit_data import insert_test_reddit
from app.embedding import SBert

from app import app


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/usertest', methods=['GET'])
def db_user_test():
    output = False

    try:
        user = users_get_all()
    except MultipleResultsFound as e:
        output = str(e)
    except NoResultFound as e:
        output = str(e)

    return user[0].username


@app.route('/column_test', methods=['GET'])
def col_test():
    add_embedding_column()
    return 'Finished!'


@app.route('/reddit', methods=['GET'])
def reddit_data():
    add_embedding_column()
    insert_test_reddit()
    return 'Finished!'


@app.route('/sbert', methods=['GET'])
def test_sbert():
    sbert = SBert()
    #sbert.calc_all_post_embeddings()
    #sbert.calc_all_group_embeddings()
    sbert.calc_all_user_embeddings()

    return jsonify(sbert.groups[0].embedding)

