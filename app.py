from datetime import timedelta

from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from controllers.auth_controller import UserRegisterResource, UserLoginResource
from controllers.auth_with_refresh_controller import auth_with_refresh_bp
from resources.item_resource import ItemResource, ItemListResource
from resources.store_resource import StoreResource, StoreListResource


app = Flask(__name__)

# jwt
app.config["JWT_COOKIE_SECURE"] = False  # In production, this should always be set to True
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # disable for development, enable for production. Disabled will allow you to use cookies being severed from the same domain
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # 'cookies' for using cookie, 'headers' for use header with {'Authorization': 'Bearer {{access_token}}'}
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)  # suggest value: seconds=3600 for JWT to expire within an hour
app.config['PROPAGATE_EXCEPTIONS'] = True  # Exceptions are re-raised rather than being handled by the app’s error handlers, Flask-JwT-extended error handling, see https://github.com/vimalloc/flask-jwt-extended/issues/20
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'database/data.db'  # + '../data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True, Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None, which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed.

# jwt
jwt = JWTManager(app)


# flask-restful routes
# api_bp = Blueprint('api', __name__)  # set a route segment for api
api = Api(app)
api.add_resource(UserRegisterResource, '/register')  # http://ssfd.com/register
api.add_resource(UserLoginResource, '/login')
api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(StoreListResource, '/stores')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemListResource, '/items')

# flask-routes
app.register_blueprint(auth_with_refresh_bp, url_prefix='/auth')

if __name__ == '__main__':  # will not run this if this file is imported.
    # database
    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    app.run(port=5000)
