from ..util.patterns.Singleton import Singleton

from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session 

from config import config


class DbManager(Singleton):
    engine = None
    
    session = None

    Base = declarative_base()
    Base.to_dict = lambda a:dict((col, getattr(a, col)) for col in a.__table__.columns.keys()) # Lambda function to convert any ORM object to a JSON-convertible dictionary


    def __init__(self):
        if self.engine is None:
            path = "sqlite:///" + config["Database"]["DB_PATH"]
            self.engine = create_engine(path, echo=True)
            self.Base.metadata.create_all(bind=self.engine)

        
    def getSession(self):
        if self.session is None:
            self.session = Session(self.engine)
        return self.session
