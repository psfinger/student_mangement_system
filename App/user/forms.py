from time import sleep

from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from App.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    # submit = SubmitField('Register')

    def validate_username(self, username):
        print("check username")
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash("用户名已存在")
            raise ValidationError('用户名已存在')
