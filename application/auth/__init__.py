from flask import Blueprint

auth_blueprint = Blueprint(__name__, 'auth_blueprint')

from . import login, register, user