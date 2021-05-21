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


Base = declarative_base()
db_instance = DB()
db_instance.connect()

