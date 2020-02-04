from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, PasswordField, BooleanField
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


class NewForm(FlaskForm):
    family_name = StringField("Family Name", validators=[DataRequired()])
    family_size = IntegerField("Family Size", validators=[DataRequired()])
    submit_new = SubmitField("Submit")


class ExistingForm(FlaskForm):
    client_id = IntegerField("Client ID", validators=[DataRequired()])
    organization = SelectField('Organization', [DataRequired()],
                               choices=[('Global FC', 'Global FC'),
                                        ('Happy Bottoms', 'Happy Bottoms'),
                                        ('Literacy KC', 'Literacy KC'),
                                        ('Mattie Rhodes', 'Mattie Rhodes'),
                                        ('Start at Zero', 'Start at Zero')])
    submit_existing = SubmitField("Submit")


class Report(FlaskForm):
    month = SelectField('Month', [DataRequired()],
                        choices=[('0', 'All'),
                                 ('1', 'January'),
                                 ('2', 'February'),
                                 ('3', 'March'),
                                 ('4', 'April'),
                                 ('5', 'May'),
                                 ('6', 'June'),
                                 ('7', 'July'),
                                 ('8', 'August'),
                                 ('9', 'September'),
                                 ('10', 'October'),
                                 ('11', 'November'),
                                 ('12', 'December')])

    year = SelectField('Year', [DataRequired()],
                       choices=[('2020', '2020'),
                                ('2021', '2021'),
                                ('2022', '2022'),
                                ('2023', '2023'),
                                ('2024', '2024'),
                                ('2025', '2025'),
                                ('2026', '2026')])

    organization = SelectField('Organization', [DataRequired()],
                               choices=[('Global FC', 'Global FC'),
                                        ('Happy Bottoms', 'Happy Bottoms'),
                                        ('Literacy KC', 'Literacy KC'),
                                        ('Mattie Rhodes', 'Mattie Rhodes'),
                                        ('Start at Zero', 'Start at Zero'),
                                        ('Master', 'Master')])

    submit_report = SubmitField("Submit")


class Download(FlaskForm):
    month = SelectField('Month', [DataRequired()],
                        choices=[('0', 'All'),
                                 ('1', 'January'),
                                 ('2', 'February'),
                                 ('3', 'March'),
                                 ('4', 'April'),
                                 ('5', 'May'),
                                 ('6', 'June'),
                                 ('7', 'July'),
                                 ('8', 'August'),
                                 ('9', 'September'),
                                 ('10', 'October'),
                                 ('11', 'November'),
                                 ('12', 'December')])

    year = SelectField('Year', [DataRequired()],
                       choices=[('2020', '2020'),
                                ('2021', '2021'),
                                ('2022', '2022'),
                                ('2023', '2023'),
                                ('2024', '2024'),
                                ('2025', '2025'),
                                ('2026', '2026')])

    organization = SelectField('Organization', [DataRequired()],
                               choices=[('Global FC', 'Global FC'),
                                        ('Happy Bottoms', 'Happy Bottoms'),
                                        ('Literacy KC', 'Literacy KC'),
                                        ('Mattie Rhodes', 'Mattie Rhodes'),
                                        ('Start at Zero', 'Start at Zero'),
                                        ('Master', 'Master')])

    submit_download = SubmitField("Get Report")
