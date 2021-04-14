class User:
    def __init__(self, _id, username, password):    # id is a Python keyword, use _id instead
        self.id = _id
        self.username = username
        self.password = password
