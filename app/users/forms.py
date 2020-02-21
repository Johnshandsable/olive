from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from app.models import UserLogin


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit_registration = SubmitField('Submit')

    def validate_username(self, username):
        user = UserLogin.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit_login = SubmitField("Login")


class UserSearch(FlaskForm):
    family_name = StringField("Family Name", validators=[DataRequired()])
    family_size = IntegerField("Family Size", validators=[DataRequired()])
    search_user = SubmitField("Search")
