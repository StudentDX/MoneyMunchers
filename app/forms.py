from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo

#class ButtonField(SubmitField):


class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(max=80)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=80)])
    repeat = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

class LogInForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=80)])
    submit = SubmitField('Log In')

class BudgetForm(FlaskForm):
    amount = DecimalField('Amount',validators=[DataRequired()])
    
    def __init__(self,submit):
        super().__init__()
        self.submit = SubmitField(_form=self,_name=submit)