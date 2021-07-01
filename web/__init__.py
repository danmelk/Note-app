from flask import Flask
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

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

    from .models import User

    create_database(app)

    return app

def create_database(app):
    db.create_all(app=app)


