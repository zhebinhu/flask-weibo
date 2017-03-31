#-*-coding:utf-8-*-
from flask import Blueprint, redirect, request, url_for, g

main = Blueprint('main',__name__)

from . import views,errors
from ..models import Permission, Role


@main.before_app_first_request
def before_request():
    from app import db
    db.create_all()
    Role.insert_roles()
    from flask_login import current_user
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@main.before_request
def before_request():
    from app.auth.forms import LoginForm
    g.loginform=LoginForm()
    from app.auth.forms import RegistrationForm
    g.registrationform = RegistrationForm()

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

@main.app_context_processor
def inject_loginform():
    return dict(loginform=g.loginform)

@main.app_context_processor
def inject_registrationform():
    return dict(registrationform=g.registrationform)
