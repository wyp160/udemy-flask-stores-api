from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404
        
    def post(self, name):
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
