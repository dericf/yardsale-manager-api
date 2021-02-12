from flask import Blueprint

market_blueprint = Blueprint(__name__, 'market_blueprint')

from . import routes