# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, ValidationError

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField(u'请输入你的名字', validators=[Required()],render_kw={'style': 'width:400px'})
    submit = SubmitField(u'提交')

class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名',validators=[Length(0,64)],render_kw={'style': 'width:400px'})
    location = StringField(u'坐标',validators=[Length(0,64)],render_kw={'style': 'width:400px'})
    about_me = TextAreaField(u'关于我',validators=[Length(0,64)],render_kw={'style': 'width:400px;height:150px;resize:none'})
    submit = SubmitField(u'提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64),
                                             Email()],render_kw={'style': 'width:400px'})
    username = StringField(u'用户名', validators=[Required(), Length(1, 64)],render_kw={'style': 'width:400px'})
    confirmed = BooleanField(u'已认证')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)],render_kw={'style': 'width:400px'})
    location = StringField(u'坐标', validators=[Length(0, 64)],render_kw={'style': 'width:400px'})
    about_me = TextAreaField(u'关于我',validators=[Length(0,64)],render_kw={'style': 'width:400px;height:150px;resize:none'})
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
    body = PageDownField(u"写点什么",validators=[Required(),Length(0,140,message=u'博文不能超过140字')])
    submit = SubmitField(u'提交')

class CommentForm(FlaskForm):
    body = TextAreaField(u'添加你的评论',validators=[Required(message=u'评论不能为空'),Length(0,100,message=u'评论不能超过100字')],render_kw={'style':'height:100px;resize: none;','placeholder':u'评论不能超过100字'})
    submit = SubmitField(u'提交')