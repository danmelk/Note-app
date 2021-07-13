from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key = True)

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('note.id'), primary_key=True))

class Draft(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    data = db.Column(db.String(5000))
    tag = db.Column(db.String(100), unique = True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_login = db.Column(db.String, db.ForeignKey('user.login'))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.LargeBinary, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    data = db.Column(db.String(5000))
    tag = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_login = db.Column(db.String, db.ForeignKey('user.login'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    notes = db.relationship('Note')
    drafts = db.relationship('Draft')