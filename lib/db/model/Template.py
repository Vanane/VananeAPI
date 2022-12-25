from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from ..DbManager import DbManager


class ____(DbManager.Base):
    __tablename__ = ""

    id = Column(__, primary_key=True)
    ____ = Column(____)

    