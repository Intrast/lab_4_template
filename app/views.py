from flask import render_template, url_for, flash, redirect, request
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


@app.route('/')
def index():
    return render_template('index.html', name='Інженерія програмного забезпечення',
                           title='PNU')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@gmail.com' and form.password.data == '1111':
            flash('You have been logged in!', category='success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', category='warning')
    return render_template('login.html', form=form, title='Login')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user = {'nickname': 'Miguel'}  # видуманий користувач
    posts = [  # список видуманих постів
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("posts.html",
                           title='Home',
                           user=user,
                           posts=posts)
