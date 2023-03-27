from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class InterfaceForm(FlaskForm):
    action = StringField('Action')
    ipaddress = StringField('IP Address', validators=[IPAddress()])
    netmask = StringField('Netmask', validators=[DataRequired()])
    submit = SubmitField('Save')
