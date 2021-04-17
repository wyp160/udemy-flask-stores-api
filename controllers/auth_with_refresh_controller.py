""" auth_with_refresh.py

auth with after_request refresh of JWT, for api design for website.
"""
# 搞懂Flask-JWT-Extended, see https://ithelp.ithome.com.tw/articles/10206407
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import jsonify, request
from flask import Blueprint, after_this_request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

from helpers.security_helper import authenticate
from models.user_model import User

auth_with_refresh_bp = Blueprint('auth_with_refresh', __name__)


# Using an `after_app_request` callback to refresh the access token
# that is within the timedelta valuse set below (suggest is 1800 seconds or 30 min)
# the timedelta value should be less then the app.config['JWT_ACCESS_TOKEN_EXPIRES'] value
# after_app_request like Flask.after_request() but for a blueprint.
# Such a function is executed after each request, even if outside of the blueprint.
# see https://tedboy.github.io/flask/generated/generated/flask.Blueprint.after_app_request.html
@auth_with_refresh_bp.after_app_request
def refresh_expiring_jwts(response):
    """ after a request, refresh the JWT access cookie if it is within 30 minutes of expiring
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(seconds=1800))  # suggest value: seconds=1800 for refresh any token that is within 30 minues
        if target_timestamp > exp_timestamp:
            additional_claims = {"note": "access_token from after_app_request"}
            access_token = create_access_token(identity=get_jwt_identity(), additional_claims=additional_claims)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@auth_with_refresh_bp.route("/login-with-refresh", methods=["POST"])
def login():
    """ login user and set an JWT access cookie
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = authenticate(username, password)
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # add additional info to claim, see https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    additional_claims = {"note": "access_token from user login"}
    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    response = jsonify({
        "msg": "login successful",
        "access_token": access_token,
        "additional_claims": additional_claims
    })
    set_access_cookies(response, access_token)
    return response


@auth_with_refresh_bp.route("/logout-with-refresh", methods=["POST"])
def logout():
    """ logout user by unset the JWT access cookie
    """
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@auth_with_refresh_bp.route("/register-with-refresh", methods=['POST'])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if User.find_by_username(username):
        return {'message': 'User already exists.'}, 400
    user = User(None, username, password).insert()
    return {"message": "User created."}, 201
