# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, ValidationError

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField(u'请输入你的名字', validators=[Required()])
    submit = SubmitField(u'提交')

class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名',validators=[Length(0,64)])
    location = StringField(u'坐标',validators=[Length(0,64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64)])
    confirmed = BooleanField(u'已认证')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'坐标', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用')

class PostForm(FlaskForm):
    body = PageDownField(u"写点什么",validators=[Required()])
    submit = SubmitField(u'提交')