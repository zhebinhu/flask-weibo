# -*-coding:utf-8-*-
from functools import wraps
from flask import abort, redirect, request, url_for, flash
from flask_login import current_user, login_user

from .models import Permission, User


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

def login_btn(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app.auth.forms import LoginForm
        loginform = LoginForm()
        if loginform.validate_on_submit():
            user = User.query.filter_by(email=loginform.email.data).first()
            if user is not None and user.verify_password(loginform.password.data):
                login_user(user, loginform.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
            flash(u'无效的用户名或密码')
        return f(loginform=loginform, *args, **kwargs)
    return decorated_function