from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from auth import UserRegister, UserLogin
from item import Item, ItemList

app = Flask(__name__)

app.secret_key = 'test-secret-key'  # need to passin by env variable
jwt = JWTManager(app)

api = Api(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/auth')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':  # will not run this if this file is imported
    app.run(port=5000)

