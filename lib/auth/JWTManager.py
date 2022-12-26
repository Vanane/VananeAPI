from datetime import datetime, timedelta

from ..util.patterns.Singleton import Singleton
from ..db.model.User import User

from config import config

import jwt

class JWTManager(Singleton):
    activeKeys = dict()


    def getJWTForUser(user:User, duration=3600):
        """
        Returns a token for a given username. If a token was generated in the last *duration* seconds, then the cached token is returned instead.
        """
        generateJwt = lambda user, time: jwt.encode({
                    "iss":user.username,
                    "exp":time
                },
                config["Settings"]["JWT_PASSPHRASE"], algorithm="HS512")

        ret = None
        
        offsetTime = datetime.utcnow() + timedelta(seconds=duration)

        userKey = JWTManager.activeKeys.get(user.username, None)

        if userKey is not None:
            if JWTManager.validateAndDecodeJWT(userKey):
                return userKey
        if ret is None:
            ret = generateJwt(user, offsetTime)
            JWTManager.activeKeys[user.username] = ret

        return ret


    def validateAndDecodeJWT(key:str):
        """
        # Checks the validity of a JWT, and returns the decoded JWT if valid, or None otherwise
        """
        try:
            return jwt.decode(key, key=config["Settings"]["JWT_PASSPHRASE"], algorithms=["HS512"], options={'verify_exp':True})
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return None