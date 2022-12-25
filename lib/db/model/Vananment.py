from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ____(Base):
    __tablename__ = "Vananments"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
