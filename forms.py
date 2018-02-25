from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email

from models import User

class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class NoteForm(Form):
    text = TextAreaField("Write something down", validators=[DataRequired()])

class PostscriptForm(Form):
    postscript = TextAreaField("Add a postscript", validators=[DataRequired()])