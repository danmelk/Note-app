from flask import Flask
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from sqlalchemy.orm import query

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your secret key ;)'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dan:dan_melk_postgres@localhost/webexam'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db.create_all(app=app)


