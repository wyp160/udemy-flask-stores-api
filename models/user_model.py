from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):    # id is a Python keyword, use _id instead
        self.id = _id
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # # connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        # cursor = connection.cursor()
        # sql = \
        #     "SELECT "\
        #     "id, username, password "\
        #     "FROM users WHERE username = ?"
        # result = cursor.execute(sql, (username,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row)  # argument unpacking

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
        # # connection.row_factory = sqlite3.Row   # pylint: disable=no-member
        # cursor = connection.cursor()
        # sql = \
        #     "SELECT "\
        #     "id, username, password "\
        #     "FROM users WHERE id = ?"
        # result = cursor.execute(sql, (_id,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row)  # argument unpacking

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def insert(self):
        # connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # cursor = connection.cursor()
        # sql = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(sql, (self.username, self.password))
        # connection.commit()
        # # get the auto generated id from sqlite3's last_insert_rowid() function
        # self.id = cursor.execute("select last_insert_rowid()").fetchone()[0]
        # connection.close()
        # return self
