from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html', name='Інженерія програмного забезпечення',
                           title='PNU')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            username = form.username.data
            email = form.email.data
            password_hash = bcrypt.generate_password_hash(form.password.data)
            user = User(username=username, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', category='success')
            return redirect(url_for('login'))
        else:
            flash(f'Account created for {form.username.data}!', category='warning')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password_true = bcrypt.check_password_hash(user.password,  form.password.data)
        if user and password_true:
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', category='success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', category='warning')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


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
