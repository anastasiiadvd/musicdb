#import the form classes from flask_wtf and wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


#create the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#create the register (sign up) form
class RegistrationForm(FlaskForm):
    #the lengths match the columns in the users table (username 50, email 100)
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(max=100),
                        Regexp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', message='Enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                              EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
