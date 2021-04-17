import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, get_jwt_header
from werkzeug.security import safe_str_cmp  # a safe string compare to avoid ascii, unicode encoding errors.

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field can not be blank.')

    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items WHERE name = ?", (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'id': row['id'], 'name': row['name'], 'price': row['price']}
        else:
            return None

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items VALUES (null, ?, ?)", (name, price))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price = ? where name = ?", (price, name))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items where name = ?", (name,))
        connection.commit()
        connection.close()
        return True

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items")
        rows = result.fetchall()
        connection.close()
        if rows:
            return [{'id': row['id'], 'name': row['name'], 'price': row['price']} for row in rows]
        else:
            return None

    @jwt_required()  # require Header.Authorization = 'Bearer <access_token>', https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    def get(self, name):
        try:
            item = Item.get_by_name(name)
        except sqlite3.Error:  # pylint: disable=no-member
            return {'message': 'An error occured'}, 500
        if not item:
            return {'message': 'item not found'}, 404
        return {'item': item}

    @jwt_required()
    def post(self, name):
        if Item.get_by_name(name):
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400
        data = Item.parser.parse_args()
        try:
            Item.insert_item(name, data['price'])
        except sqlite3.Error:  # pylint: disable=no-member
            return {'message': 'An error occured'}, 500
        return {'message': 'item added'}, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        price = data['price']
        old_item = Item.get_by_name(name)
        if not old_item:
            try:
                Item.insert_item(name, price)
            except sqlite3.Error:  # pylint: disable=no-member
                return {'message': 'An error occured'}, 500
            return {'message': 'item added'}, 201
        else:
            try:
                Item.update_item(name, price)
            except sqlite3.Error:  # pylint: disable=no-member
                return {'message': 'An error occured'}, 500
            return {'message': 'item updated'}, 202

    @jwt_required()
    def delete(self, name):
        if not Item.get_by_name(name):
            return {'message': 'item not found'}, 404
        try:
            Item.delete_item(name)
        except sqlite3.Error:  # pylint: disable=no-member
            return {'message': 'An error occured'}, 500
        return {'message': 'item deleted'}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        try:
            items = Item.get_all()
        except sqlite3.Error:  # pylint: disable=no-member
            return {'message': 'An error occured'}, 500
        # https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/
        claims = get_jwt()
        identity = get_jwt_identity()
        jwt_header = get_jwt_header()
        return {
            'items': items,
            "additional_claims": claims["note"],
            'identity': identity,
            'jwt_header': jwt_header
        }
