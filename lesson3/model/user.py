class User(object):

    def __init__(self, username="", password="", email=""):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def Admin(cls):
        return cls(username="admin", password="admin")