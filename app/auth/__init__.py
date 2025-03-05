from flask import Blueprint
from app.auth import routes

auth_bp = Blueprint('auth', __name__)

from . import routes