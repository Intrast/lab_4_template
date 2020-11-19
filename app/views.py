from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreatePostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html', name='Інженерія програмного забезпечення',
                           title='PNU')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen_user = datetime.utcnow()
        db.session.commit()


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


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = bcrypt.generate_password_hash(form.password.data)
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='image/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    return render_template("posts.html",
                           title='Posts',
                           posts=posts)


@app.route('/posts/<int:id>', methods=['GET', 'POST'])
def post_details(id):
    post = Post.query.get(id)
    return render_template("post_detail.html",
                           title='Posts Detail',
                           post=post)


@app.route('/posts/<int:id>/delete', methods=['GET', 'POST'])
def post_delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))


@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def post_edit(id):
    post = Post.query.get(id)
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.date_posted = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('post_details', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_edit.html', title='Post Edit', form=form)


@app.route('/post/new', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template("create-post.html", title='Create Post', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/image', picture_fn)
    # form_picture.save(picture_path)
    # return picture_fn

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
