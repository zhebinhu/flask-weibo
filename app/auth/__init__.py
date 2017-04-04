from flask import Blueprint, g

auth = Blueprint('auth',__name__)

from . import views