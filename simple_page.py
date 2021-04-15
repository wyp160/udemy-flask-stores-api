from flask import Blueprint

simple_page = Blueprint('simple_page', __name__)


@simple_page.route('/simple_page')
def show():
    return 'simple page'
