from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from db import db_instance
from users_orm import UsersOrm, users_get_all
from reddit_data import insert_test_reddit

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dbtest', methods=['GET'])
def db_test():
    output = 'database connection is ok'

    try:
        db_instance.connect()
        db_instance.current_session.execute('SELECT 1')
    except Exception as e:
        output = str(e)

    return output


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


@app.route('/reddit', methods=['GET'])
def reddit_data():
    insert_test_reddit()
    return 'Finished!'


if __name__ == '__main__':
    app.run()
