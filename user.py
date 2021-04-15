import sqlite3


class User:
    def __init__(self, _id, username, password):    # id is a Python keyword, use _id instead
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, username, password FROM USERS WHERE username = ?", (username,))
        row = result.fetchone()
        if row:
            user = cls(row['id'], row['username'], row['password'])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
        connection.row_factory = sqlite3.Row   # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, username, password FROM users WHERE id = ?", (_id,))
        row = result.fetchone()
        if row:
            user = cls(row['id'], row['username'], row['password'])
        else:
            user = None
        connection.close()
        return user
