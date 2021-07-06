from operator import pos
import json
import re
from types import MethodDescriptorType
from web.auth import login
from . import db
from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from flask import Blueprint, render_template, flash, jsonify
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from flask_login import login_required, current_user
from .models import Note, User, Image

views = Blueprint('views', __name__)

@views.route('/home', methods=['POST', 'GET'])
# @login_required
def home():
    users_login = User.query.order_by(User.login).all()
    if request.method == "POST":
        if 'username' in session:
            # username = session['username']
            note_title = request.form.get('title')
            note_data = request.form.get('note')
            note_tag = request.form.get('tag')
            picture = request.files.get('picture')
            if picture:
                filename  = secure_filename(picture.filename)
                mimetype = picture.mimetype
                note_image = Image(
                img = picture.read(),
                mimetype = mimetype,
                name = filename)

                db.session.add(note_image)
                db.session.commit()

            else:

                flash('Picture does not attached ', category='error')

            valid_title = Note.query.filter_by(title = note_title).first()
            valid_tag = Note.query.filter_by(tag = note_tag).first()
            if valid_title:
                flash('Wrong title', category='error')
            elif valid_tag:
                flash('Wrong tag', category='error')
            elif len(note_data) < 1:
                flash('Write something!', category='error')
            else:
                note_entrance = Note(
                    title =  note_title,
                    data = note_data, 
                    user_login = current_user.login, 
                    tag = note_tag)

                db.session.add(note_entrance)
                db.session.commit()

        else:
            flash('Please login first ', category='error')
            return redirect(url_for('auth.login'))
    return render_template('home.html',
    users_login = users_login,
    current_user = current_user)


@views.route('/posts/<name>', methods=['POST', 'GET'])
def post(name):
    article = Note.query.filter_by(title = name).first()    
    return render_template('post.html', 
    article = article)

# @views.route('/image', methods=['POST'])
# def upload():
#     pic = request.files['pic']
#     filename = secure_filename(pic.filename)
#     mimetype = pic.mimetype
#     img = Image(img=pic.read(), name=filename, mimetype=mimetype)
#     db.session.add(img)
#     db.session.commit()
#     return 'pic has been uploaded'


# @views.route('/image/<int:id>')
# def get_img(id):
#     img = Image.query.filter_by(id=id).first()
#     return Response(img.img, mimetype=img.mimetype)


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
