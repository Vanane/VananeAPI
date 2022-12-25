from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy import select

from ..DbManager import DbManager

import hashlib


class User(DbManager.Base):
    __tablename__ = "Users"

    username = Column(Text, primary_key=True)
    password = Column(Text, nullable=False)
    permissions = Column(Text, nullable=False) # JSON array of strings 
    active = Column(Integer, default=0)


    def getUser(username):
        query = select(User).where(User.username == username)
        ret = None
        s = DbManager().getSession()
        ret = s.scalar(query)
        s.commit()
        print(ret)
        return ret


    def createUser(us:str, pa:str, pe:list, ac = 0):
        s = DbManager().getSession()
        pa = User.encryptPassword(pa)
        
        ret = s.add(User(username=us, password = pa, permissions = str(pe), active = ac))
        s.commit()
        return ret


    def checkPassword(username, password:str):
        s = DbManager().getSession()
        user = User.getUser(username)
        if user is None:
            return False
        else:
            return User.encryptPassword(password) == User.getUser(username).password


    def hasPermissions(self, perms:list):
        pass


    def encryptPassword(pwd:str):
        return hashlib.sha512(pwd.encode('utf-8')).hexdigest()


    def __repr__(self) -> str:
        return 'User(' +\
                'username=' + str(self.username) +\
                ', password=' + str(self.password) +\
                ', permissions=' + self.permissions +\
                ', active=' + str(self.active) +\
                ')'



