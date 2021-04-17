from sqlalchemy.exc import SQLAlchemyError

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, get_jwt_header
from werkzeug.security import safe_str_cmp  # a safe string compare to avoid ascii, unicode encoding errors.

from models.item_model import Item


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field can not be blank.')

    @jwt_required()
    def get(self, name):
        try:
            item = Item.get_by_name(name)
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        if not item:
            return {'message': 'item not found'}, 404
        return item.json()

    @jwt_required()
    def post(self, name):
        if Item.get_by_name(name):
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400
        data = ItemResource.parser.parse_args()
        item = Item(None, name, data['price'])
        try:
            item.save_to_db()  # item.insert()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = ItemResource.parser.parse_args()
        price = data['price']
        item = Item.get_by_name(name)
        is_new = item is None
        if is_new:
            item = Item(None, name, price)
        else:
            item.price = price
        try:
            item.save_to_db()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return item.json(), 201 if is_new else 202

        # if item:
        #     item.price = price
        #     try:
        #         item.save_to_db()  # old_item.update()
        #         # Item.update_item(name, price)
        #     except sqlite3.Error:  # pylint: disable=no-member
        #         return {'message': 'An error occured'}, 500
        #     return item.json(), 202
        # else:
        #     item = Item(None, name, price)
        #     try:
        #         item.save_to_db()  # item.insert()
        #     except sqlite3.Error:  # pylint: disable=no-member
        #         return {'message': 'An error occured'}, 500
        #     return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = Item.get_by_name(name)
        if not item:
            return {'message': 'item not found'}, 404
        try:
            item.delete_from_db()  # item.delete()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return {'message': 'item deleted'}, 200


class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            items = Item.get_all()  # items = Item.get_all()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        # https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/
        claims = get_jwt()
        identity = get_jwt_identity()
        jwt_header = get_jwt_header()
        return {
            'items': [item.json() for item in items],
            "additional_claims": claims["note"],
            'identity': identity,
            'jwt_header': jwt_header
        }
