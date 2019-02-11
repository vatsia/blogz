import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import LoginManager, current_user, login_user

from db import db_session, init_db
from models import User
from loginform import LoginForm

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    init_db()

    login_manager = LoginManager()
    login_manager.init_app(app)

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
        if request.method == 'POST': #TODO validate form
            user = User.query.filter_by(name=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        return render_template('login/login.html', form=form)

    return app

