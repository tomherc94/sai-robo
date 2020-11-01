from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

#-----------Users----------------

class RegisterForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("password", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class DeleteForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])

class ReadForm(FlaskForm):
    username = StringField("username")

class UpdateForm(FlaskForm):
    #username = StringField("username", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("password", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

#-----------Released----------------

class RegisterFormReleased(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired()])

