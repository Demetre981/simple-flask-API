from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField

class LoginForm(FlaskForm):
    nickname = StringField("Nickname", [validators.DataRequired()])
    password = PasswordField("password", [validators.DataRequired()])
    email = StringField("email", [validators.DataRequired()])
    submit = SubmitField("Log in")


class SignForm(LoginForm):
    email = StringField("Nickname", [validators.DataRequired()])
    submit = SubmitField("Sign up")