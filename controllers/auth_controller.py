import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from helpers.security_helper import authenticate
from models.user_model import User


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field can not be blank.")
    parser.add_argument('password', type=str, required=True, help="This field can not be blank.")

    def post(self):
        data = UserRegisterResource.parser.parse_args()
        username = data['username']
        password = data['password']
        if User.get_by_username(username):
            return {'message': 'User already exists.'}, 400

        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))
        connection.commit()
        connection.close()
        return {"message": "User created."}, 201


class UserLoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field can not be blank.")
    parser.add_argument('password', type=str, required=True, help="This field can not be blank.")

    def post(self):
        """ authenticate your users and return JWTs

        use the create_access_token() to authenticate your users and return JWTs.

        args:
            username (string): user name
            password (string): password

        returns:
            access_token (string): a jwt access token
        """
        data = UserLoginResource.parser.parse_args()
        username = data['username']
        password = data['password']

        user = authenticate(username, password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
