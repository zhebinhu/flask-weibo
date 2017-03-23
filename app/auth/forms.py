# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, ValidationError

from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'电子邮箱',validators=[Required(),Length(1,64),Email()])
    password = PasswordField(u'密码',validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegistrationForm(FlaskForm):
    email = StringField(u'电子邮箱',validators=[Required(),Length(1,64),Email()])
    username = StringField(u'用户名',validators=[Required(),Length(1,64)])
    password = PasswordField(u'密码',validators=[Required(),EqualTo('password2',message=u'两次密码要一致')])
    password2 = PasswordField(u'确认密码',validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被使用')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')

class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱地址')

class PasswordResetForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱地址')

class ChangeEmailForm(FlaskForm):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')