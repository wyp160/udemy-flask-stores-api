import sqlite3


class User:
    def __init__(self, _id, username, password):    # id is a Python keyword, use _id instead
        self.id = _id
        self.username = username
        self.password = password

    def json(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = \
            "SELECT "\
            "id, username, password "\
            "FROM users WHERE username = ?"
        result = cursor.execute(sql, (username,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)  # argument unpacking

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
        # connection.row_factory = sqlite3.Row   # pylint: disable=no-member
        cursor = connection.cursor()
        sql = \
            "SELECT "\
            "id, username, password "\
            "FROM users WHERE id = ?"
        result = cursor.execute(sql, (_id,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)  # argument unpacking

    def insert(self):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        sql = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(sql, (self.username, self.password))
        connection.commit()
        # get the auto generated id from sqlite3's last_insert_rowid() function
        self.id = cursor.execute("select last_insert_rowid()").fetchone()[0]
        connection.close()
        return self
