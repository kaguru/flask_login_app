from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import or_, and_

from .db import get_engine, get_session
from .models import User, UserActive

from .forms import LoginForm, RegisterForm
from . import helpers

db_engine = get_engine()
db_session = get_session()
login_manager = LoginManager()

bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    user = db_session.query(User).filter(and_(User.username == username_input, User.password == password_input)).first()
    return User(user.id)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    success_msg = None
    if form.validate_on_submit():
        username_input = request.form.get('username')
        password_input = request.form.get('password')
        if username_input and password_input:
            user = db_session.query(User).filter(and_(User.username == username_input)).first()
            db_session.commit()
            if user and check_password_hash(user.password, password_input):
                login_user(UserActive(user.id))
                session['username'] = user.username
                success_msg = 'Login Successful'
                next = request.args.get('next')
                if not helpers.is_safe_url(next):
                    return abort(400)
                flash(success_msg)
                return redirect(next or url_for('members.index'))
            else:
                error = f"Wrong Credentials <a href={url_for('auth.register')}> Register </a>"
        else:
            error = 'Please Fill in All Fields!'
        if error:
            flash(error)
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username_input = request.form.get('username')
        email_input = request.form.get('email')
        password_input = request.form.get('password')

        if username_input and email_input and password_input:
            if db_session.query(User).filter(or_(User.username == username_input, User.email == email_input)).first():
                error = f"Account Exists <a href={url_for('auth.login')}> Login </a>"
            else:
                user_reg = User(username=username_input, email=email_input, password=generate_password_hash(password_input))
                db_session.add(user_reg)
                db_session.commit()
                flash('Registration Successful')
                return redirect(url_for('auth.login'))
        else:
            error = 'Please Fill in All Fields!'
        flash(error)
    return render_template('register.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Successfully Logged Out')
    return redirect(url_for('auth.index'))

