from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[Length(min=4, max=25,
                            message='Це поле має бути довжиною між 4 та 25 символів'),
                            DataRequired(message='Це поле обовязкове'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                              validators=[Length(min=6,
                              message='Це поле має бути довжиною більше 6 символів'),
                              DataRequired(message='Це поле обовязкове')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=4, max=25, message='Це поле має бути довжиною між 4 та 25 символів'),
                           DataRequired(message='Це поле обовязкове'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About Me', validators=[Length(min=4, max=250, message='Це поле має бути довжиною між 4 та 250 символів')])
    password = PasswordField('Password',
                             validators=[Length(min=6,
                                                message='Це поле має бути довжиною більше 6 символів'),
                                         DataRequired(message='Це поле обовязкове')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    last_seen = StringField('Last Seen', validators=[Length(min=4, max=60, message='Це поле має бути довжиною між 4 та 60 символів')])
    picture = FileField('update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use')

    def validate_email(self, field):
        if field.data != current_user.username:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already register')

