from werkzeug.security import safe_str_cmp      # a safe string compare to avoid ascii, unicode encoding errors.
from models.user_model import User


def authenticate(username, password):
    user = User.get_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# def identity(payload):
#     user_id = payload['identity']
#     return User.find_by_id(user_id)
