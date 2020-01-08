from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(max=80)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=80)])
    repeat = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

class LogInForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=80)])
    submit = SubmitField('Log In')