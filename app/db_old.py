from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DB:
    engine = None
    Session = None
    current_session = None

    def connect(self):
        self.engine = create_engine('postgresql://postgres:postgres@localhost:5432/fhsocial')
        self.Session = sessionmaker(bind=self.engine)
        self.current_session = self.Session()


def add_column(table, col_name):
    q = 'ALTER TABLE ' + str(table) + ' ADD column ' + str(col_name) + ' float[];'
    db_instance.engine.execute(q)


def add_embedding_column():
    add_column('users', 'embedding')
    add_column('groups', 'embedding')
    add_column('posts', 'embedding')


Base = declarative_base()
db_instance = DB()
db_instance.connect()

