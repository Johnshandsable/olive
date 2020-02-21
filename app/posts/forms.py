from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

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
