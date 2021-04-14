from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        # item = next(enumerate([item for item in items if item['name'] == name]), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400  # bad request
        request_data = request.get_json()  # use force=True to avoid contentType; use silent=True to avoid error and return none
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        return {'name': name}
        
    def delete(self, name):
        return {'name': name}


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
