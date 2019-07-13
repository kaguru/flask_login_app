import os
from flask import Flask, request, redirect, url_for
from flask_login import LoginManager
from .forms import LoginForm, RegisterForm
from .models import UserActive


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserActive(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login', next=request.path))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'strong-secret-key'
    app.config['DATABASE'] = f"sqlite:///{os.path.dirname(__file__)}/db_login_app.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        from . import models
        from . import db
        from . import auth
        from . import members
        from . import public

        # Register Blueprints
        app.register_blueprint(members.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(public.bp)
        app.add_url_rule('/', methods=['GET', 'POST'], endpoint='public.index')
        # Initialize Login Manager
        login_manager.init_app(app)

        # Create Tables
        @app.before_first_request
        def create_tables():
            models.create_tables(db.get_engine())
    return app


if __name__ == '__main__':
    # Run Application
    create_app()

