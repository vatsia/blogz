import os
import logging

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from http_method_override import HTTPMethodOverrideMiddleware

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from db import db_session, init_db
from models import User
from forms import LoginForm, SigninForm, UpdateUserForm


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    init_db()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Unauthorized request!')
        return redirect(url_for('index'))

    app.config.from_mapping(
        SECRET_KEY='development',
        DATABASE=os.path.join(app.instance_path, 'development.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database initialization
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # index page. 10 newest posts with paging?
    @app.route('/')
    def index():
        return render_template('index.html')

    # show posts on page
    @app.route('/page/<int:page_num>')
    def page(page_num):
        return render_template('index.html')

    # show whole post or page
    @app.route('/post/<string:page_name>')
    def show_post(page_name):
        return render_template('index.html')

    # render post creation page
    @app.route('/post/new')
    def new_post():
        return render_template('index.html')

    # render post editing page
    @app.route('/post/<string:page_name>/edit')
    def edit_post(page_name):
        return render_template('index.html')

    # save created post to database
    @app.route('/post/create', methods=['POST'])
    def create_post():
        if request.method == 'POST':
            return 'creating post'

    # update post to database
    @app.route('/post/<string:page_name>/update', methods=['UPDATE'])
    def update_post(page_name):
        if request.method == 'UPDATE':
            return 'updating post'

    # delete post
    @app.route('/post/<string:page_name>/delete', methods=['DELETE'])
    def delete_post(page_name):
        if request.method == 'DELETE':
            return 'deleting post'

    # AUTHENTICATION
    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user is None or not user.check_password(form.passw.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember.data)
            flash('Welcome, ' + current_user.name)
            return redirect(url_for('index'))
        return render_template('login/login.html', form=form)

    @app.route('/signin', methods=['POST', 'GET'])
    def signin():
        form = SigninForm()
        if form.validate_on_submit():
            if form.passw.data == form.passw_confirmation.data:
                newuser = User(str(form.username.data), str(form.passw.data))
                db_session.add(newuser)
                db_session.commit()
                flash(u'User created succesfully')
            else:
                flash(u'Password and password confirmation mismatch')
        return render_template('login/signin.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        flash('Logged out!')
        logout_user()
        return redirect(url_for('index'))

    @app.route('/users')
    @login_required
    def list_users():
        users = User.query.all()
        return render_template('login/list.html', u=users)

    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_user(user_id):
        u = User.query.get(user_id)

        if u is None:
            flash('User not found!')
            return redirect(url_for('index'))

        form = UpdateUserForm()

        if request.method == 'POST':
            if u.name != form.username.data:
                u.name = form.username.data
            if len(form.passw.data) > 0:
                u.set_password(form.passw.data)
            db_session.commit()
            return redirect(url_for('edit_user', user_id=user_id))
        else:
            form.username.data = u.name
            return render_template('login/edit.html', form=form, u=u)

    @app.route('/users/<int:uid>/delete', methods=['POST', 'DELETE'])
    @login_required
    def delete_user(uid):
        db_session.delete(User.query.get(uid))
        db_session.commit()
        return redirect(url_for('list_users'))

    return app


