#-*-coding:utf-8-*-
from flask import Blueprint, redirect, request, url_for, g

main = Blueprint('main',__name__)

from . import views,errors
from ..models import Permission, Role, User, Post


@main.before_app_first_request
def before_request():
    from app import db
    db.create_all()
    from flask_login import current_user
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

