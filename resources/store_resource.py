from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from models.store_model import Store


class StoreResource(Resource):
    @jwt_required()
    def get(self, name):
        try:
            store = Store.get_by_name(name)
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        if not store:
            return {'message': 'store not found'}, 404
        return store.json()

    @jwt_required()
    def post(self, name):
        if Store.get_by_name(name):
            return {'message': 'An store with the name \'{}\' already exist.'.format(name)}, 400
        store = Store(None, name)
        try:
            store.save_to_db()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = Store.get_by_name(name)
        if not store:
            return {'message': 'store not found'}, 404
        try:
            store.delete_from_db()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return {'message': 'store deleted'}, 200


class StoreListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            stores = Store.get_all()
        except SQLAlchemyError as e:
            return {'message': 'An error occured.({})'.format(e.__dict__)}, 500
        return {
            'stores': [store.json() for store in stores]
        }
