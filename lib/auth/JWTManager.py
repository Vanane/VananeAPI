from datetime import datetime, timedelta

from ..util.patterns.Singleton import Singleton
from ..db.model.User import User

from config import config

import jwt

class JWTManager(Singleton):
    activeKeys = dict()


    def getJWTForUser(user:User, duration=3600):

        generateJwt = lambda user, time: jwt.encode({
                    "iss":user.username,
                    "exp":time
                },
                config["Settings"]["JWT_PASSPHRASE"], algorithm="HS512")

        ret = None
        
        offsetTime = datetime.utcnow() + timedelta(seconds=duration)

        userKey = JWTManager.activeKeys.get(user.username, None)

        if userKey is not None:
            if JWTManager.checkJWT(userKey):
                ret = userKey
        if ret is None:
            ret = generateJwt(user, offsetTime)
            JWTManager.activeKeys[user.username] = ret

        return ret


    def checkJWT(key:str):
        try:
            jwt.decode(key, key=config["Settings"]["JWT_PASSPHRASE"], algorithms=["HS512"], options={'verify_exp':True})
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return False
        return True
