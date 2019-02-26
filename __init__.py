import os
import logging

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort

from urllib.parse import quote_plus

import bbcode

from http_method_override import HTTPMethodOverrideMiddleware

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from db import db_session
from models import User, Post
from forms import LoginForm, SigninForm, UpdateUserForm, CreatePostForm


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    sqlite_db_path = os.path.join(app.instance_path, 'development.sqlite')
    app.config.from_mapping(
        SECRET_KEY='development',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + sqlite_db_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        POSTS_PER_PAGE=5,
    )

    db_session.init_app(app)

    # if database file not exists, create it and create root user
    if User.count() == 0 or User.count() is None:
        db_session.create_all(app=app)
        u = User(name='root', password='root123')
        db_session.add(u)
        db_session.commit()
        print('Created root user')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Unauthorized request!')
        return redirect(url_for('index'))

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # index page. 10 newest posts with paging?
    @app.route('/')
    def index():
        return render_template('index.html')

    # show posts on page
    @app.route('/page')
    @app.route('/page/<int:page_num>')
    def page(page_num=1):
        posts = Post.query.paginate(page_num, app.config['POSTS_PER_PAGE'], True)
        return render_template('index.html', posts=posts)

    # show whole post or page
    @app.route('/post/<string:page_name>')
    def show_post(page_name):
        p = Post.query.filter_by(link_address=page_name).first()
        if p is None:
            abort(404)
        if p.is_draft and current_user.is_authenticated is False:
            abort(403)

        parser = bbcode.Parser()
        parser.add_simple_formatter(
            'video',
            '<iframe width="420" height="315" src="https://www.youtube.com/embed/%(value)s"></iframe>',
            standalone=False
        )
        #p.content = bbcode.render_html(p.content)
        p.content = parser.format(p.content)

        return render_template('posts/view_post.html', p=p)

    # render post creation page
    @app.route('/post/new', methods=['GET', 'POST'])
    def new_post():
        form = CreatePostForm()
        if form.validate_on_submit():
            p = Post(
                quote_plus(form.header.data),
                form.header.data,
                form.lead_paragraph.data,
                form.content.data,
                current_user.id,
                form.is_draft.data
            )
            db_session.add(p)
            db_session.commit()
            flash('Post created succesfully!')
            return redirect(url_for('show_post', page_name=p.link_address))
        return render_template('posts/new.html', form=form)

    # render post editing page
    @app.route('/post/<string:page_name>/edit')
    def edit_post(page_name):
        return render_template('index.html')

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


