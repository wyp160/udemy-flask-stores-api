from datetime import timedelta

from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from auth import UserRegister, UserLogin
from item import Item, ItemList
from auth_with_refresh import auth_with_refresh


app = Flask(__name__)

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # disable for development, enable for production. Disabled will allow you to use cookies being severed from the same domain
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # 'cookies' for using cookie, 'headers' for use header with {'Authorization': 'Bearer {{access_token}}'}
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)  # suggest value: seconds=3600 for JWT to expire within an hour
app.config['PROPAGATE_EXCEPTIONS'] = True  # Exceptions are re-raised rather than being handled by the app’s error handlers, Flask-JwT-extended error handling, see https://github.com/vimalloc/flask-jwt-extended/issues/20

jwt = JWTManager(app)

# api_bp = Blueprint('api', __name__)  # set a route segment for api
api = Api(app)


api.add_resource(UserRegister, '/register')  # http://ssfd.com/register
api.add_resource(UserLogin, '/login')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.register_blueprint(auth_with_refresh)

if __name__ == '__main__':  # will not run this if this file is imported
    app.run(port=5000)
