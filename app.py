from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
# a safe string compare to avoid ascii, unicode encoding errors.
from werkzeug.security import safe_str_cmp

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'test-secret-key'
jwt = JWTManager(app)

api = Api(app)

items = []


@app.route("/auth", methods=["POST"])
def auth():
    """ authenticate your users and return JWTs

    use the create_access_token() to authenticate your users and return JWTs.

    args:
        username (string): user name
        password (string): password

    returns:
        access_token (string): a jwt access token
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


class Item(Resource):
    @jwt_required()  # require Header.Authorization = 'Bearer <access_token>'
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        # item = next(enumerate([item for item in items if item['name'] == name]), None)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            # bad request
            return {'message': 'An item with the name \'{}\' already exist.'.format(name)}, 400
        # use force=True to avoid contentType; use silent=True to avoid error and return none
        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def put(self, name):
        price = request.json.get("price", None)
        item = next(filter(lambda item: item['name'] == name, items), None)
        if not item:
            item = {'name': name, 'price': price}
            items.append(item)
        else:
            item.update({'price': price})
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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
