# ~*~ encoding: utf-8 ~*~
from flask import Blueprint

main = Blueprint('user', __name__)

from . import views