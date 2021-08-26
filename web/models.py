from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))
    note_tag = db.Column(db.String, db.ForeignKey('note.title'))
    note_tag_url = db.Column(db.String, db.ForeignKey('note.note_url'))
    
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    data = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_login = db.Column(db.String, db.ForeignKey('user.login'))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.LargeBinary)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    note_image = db.Column(db.String, db.ForeignKey('note.title'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)
    data = db.Column(db.String(5000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    note_url = db.Column(db.String(200), unique = True)
    user_login = db.Column(db.String, db.ForeignKey('user.login'))
    images = db.relationship('Image')
    tags = db.relationship('Tag', foreign_keys = [Tag.note_tag])
    tags_url = db.relationship('Tag', foreign_keys = [Tag.note_tag_url])

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    ip_addr = db.Column(db.String(100))
    notes = db.relationship('Note')
    drafts = db.relationship('Draft')