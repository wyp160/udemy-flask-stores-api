from datetime import timedelta

from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from auth import UserRegister, UserLogin
from item import Item, ItemList
from simple_page import simple_page

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=60)

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.register_blueprint(simple_page)

if __name__ == '__main__':  # will not run this if this file is imported
    app.run(port=5000)

