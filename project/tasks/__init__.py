from flask import Blueprint

tasks_blueprint = Blueprint('tasks', __name__, template_folder='templates')

from . import routes