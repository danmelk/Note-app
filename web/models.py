from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# class Tag(db.Model):
#     tag_name = db.Column(db.String(100), primary_key = True)
#     note_relation = db.relationship('Note')

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.LargeBinary, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    data = db.Column(db.String(5000))
    tag = db.Column(db.String(100), unique = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_login = db.Column(db.String, db.ForeignKey('user.login'))
    # tag_name = db.Column(db.String(100), db.ForeignKey('tag.tag_name'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    notes = db.relationship('Note')