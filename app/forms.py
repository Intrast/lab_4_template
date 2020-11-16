from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[Length(min=4, max=25,
                            message='Це поле має бути довжиною між 4 та 25 символів'),
                            DataRequired(message='Це поле обовязкове')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                              validators=[Length(min=6,
                              message='Це поле має бути довжиною більше 6 символів'),
                              DataRequired(message='Це поле обовязкове')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
