from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

from App.main import routes
from App.main.grade import routes
from App.main.permission import routes
from App.main.role import routes
from App.main.student import routes
