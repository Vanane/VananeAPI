from ..util.patterns.Singleton import Singleton

from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session 

from config import config


class DbManager(Singleton):
    engine = None
    
    session = None

    Base = declarative_base()

    """
    Lambda function to convert any ORM object to a JSON-convertible dictionary
    """
    Base.toDict = lambda object:dict((col, getattr(object, col)) for col in object.__table__.columns.keys())
    

    def __init__(self):
        if self.engine is None:
            path = "sqlite:///" + config["Database"]["DB_PATH"]
            self.engine = create_engine(path, echo=True)
            self.Base.metadata.create_all(bind=self.engine)

        
    def getSession(self):
        if self.session is None:
            self.session = Session(self.engine)
        return self.session
