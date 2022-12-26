from ..util.patterns.Singleton import Singleton

from ..db.model.User import User


class PermManager(Singleton):
    adminPermission = "Admin"


    def hasPermissions(user:User, perms:set):
        """
        """
        # Counting how many permissions the given set and the user's permissions array have in common
        # This way, the array is read only once
        count = len(perms)
        i = 0

        for p in user.permissions:
            print(p)
            if p == PermManager.adminPermission:
                return True
            if perms.__contains__(p):
                i += 1
        return count == i
