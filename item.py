import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
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

    @jwt_required()  # require Header.Authorization = 'Bearer <access_token>', https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    def get(self, name):
        item = Item.get_by_name(name)
        if not item:
            return {'message': 'item not found'}, 404
        return {'item': item}

    @jwt_required()
    def post(self, name):
        if Item.get_by_name(name):
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400
        data = Item.parser.parse_args()
        Item.insert_item(name, data['price'])
        return {'message': 'item added'}, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        price = data['price']
        item = Item.get_by_name(name)
        if not item:
            Item.insert_item(name, price)
            return {'message': 'item added'}, 201
        else:
            Item.update_item(name, price)
            return {'message': 'item updated'}, 202

    @jwt_required()
    def delete(self, name):
        if not Item.get_by_name(name):
            return {'message': 'item not found'}, 404
        Item.delete_item(name)
        return {'message': 'item deleted'}, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}
