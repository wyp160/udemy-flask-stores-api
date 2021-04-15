import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):    # id is a Python keyword, use _id instead
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member, https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
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
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member, https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, username, password FROM users WHERE id = ?", (_id,))
        row = result.fetchone()
        if row:
            user = cls(row['id'], row['username'], row['password'])
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field can not be blank.")
    parser.add_argument('password', type=str, required=True, help="This field can not be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": "User created."}, 201
