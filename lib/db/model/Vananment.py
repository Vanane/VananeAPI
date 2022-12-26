from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy import select, insert

from ..DbManager import DbManager


class Vananment(DbManager.Base):
    __tablename__ = "Vananments"

    id = Column(Integer, primary_key=True)
    content = Column(Text)


    def gets():
        query = select(Vananment)
        s = DbManager().getSession()
        ret = s.scalars(query)

        return ret


    def get(id:int):
        query = select(Vananment).where(Vananment.id == id)
        s = DbManager().getSession()
        ret = s.scalar(query)

        return ret


    def add(content):
        s = DbManager().getSession()

        ret = s.add(Vananment(content = content))
        s.commit()

        return ret


    def update(self, **fields):
        s = DbManager().getSession()

        for field in fields:
            value = fields[field]
            setattr(self, field, value)
        s.commit()
        return True


    def delete(self):
        s = DbManager().getSession()

        s.delete(self)
        s.commit()
        return True


    def __repr__(self) -> str:
        return 'Vananment(' +\
                'id=' + str(self.id) +\
                ', content=' + str(self.content) +\
                ')'
