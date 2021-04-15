import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from werkzeug.security import safe_str_cmp  # a safe string compare to avoid ascii, unicode encoding errors.

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field can not be blank.')

    @jwt_required()  # require Header.Authorization = 'Bearer <access_token>', https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    def get(self, name):
        connection = sqlite3.connect('../data.db')  # pylint: disable=no-member
        connection.row_factory = sqlite3.Row  # pylint: disable=no-member
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, name, price FROM items WHERE name = ?", (name,))
        row = result.fetchone()
        if not row:
            return {'message': 'item not found'}, 404
        return {'item': {'name': row['name'], 'price': row['price']}}, 200

    @jwt_required()
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda item: item['name'] == name, items), None)
        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

    @jwt_required()
    def delete(self, name):
        global items
        items = [item for item in items if not safe_str_cmp(
            item['name'], name)]
        return {'message': 'item deleted'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}
