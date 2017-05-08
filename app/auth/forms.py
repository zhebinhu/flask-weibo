# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, ValidationError, DataRequired

from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(message=u'邮箱不能为空'), Length(1, 64), Email(message=u'请输入有效的邮箱地址')],
                        render_kw={'class': 'form-control'})
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空')], render_kw={'class': 'form-control'})
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError(u'邮箱或密码错误')
        elif not user.verify_password(field.data):
            raise ValidationError(u'邮箱或密码错误')


class RegistrationForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(message=u'邮箱不能为空'), Length(1, 64), Email(message=u'请输入有效的邮箱地址')])
    username = StringField(u'用户名', validators=[Required(message=u'用户名不能为空'), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空'), EqualTo('password2', message=u'两次密码要一致')],render_kw={'class': 'form-control'})
    password2 = PasswordField(u'确认密码', validators=[Required(message=u'确认密码不能为空')],render_kw={'class': 'form-control'})
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[Required()],render_kw={'style': 'width:400px'})
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'密码不一致')],render_kw={'style': 'width:400px'})
    password2 = PasswordField(u'确认密码', validators=[Required()],render_kw={'style': 'width:400px'})
    submit = SubmitField(u'提交', render_kw={'class': 'btn btn-primary'})


class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()],render_kw={'style': 'width:400px'})
    submit = SubmitField(u'提交', render_kw={'class': 'btn btn-primary'})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱地址')


class PasswordResetForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()],render_kw={'style': 'width:400px'})
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')],render_kw={'style': 'width:400px'})
    password2 = PasswordField(u'确认密码', validators=[Required()],render_kw={'style': 'width:400px'})
    submit = SubmitField(u'提交', render_kw={'class': 'btn btn-primary'})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知的邮箱地址')


class ChangeEmailForm(FlaskForm):
    email = StringField(u'新邮箱', validators=[Required(), Length(1, 64),
                                            Email()],render_kw={'style': 'width:400px'})
    password = PasswordField(u'密码', validators=[Required()],render_kw={'style': 'width:400px'})
    submit = SubmitField(u'提交', render_kw={'class': 'btn btn-primary'})

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被注册')
