from operator import irshift, pos
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
from .models import Note, User, Image, Draft

views = Blueprint('views', __name__)

@views.route('/home', methods=['POST', 'GET'])
# @login_required
def home():
    users_login = User.query.order_by(User.login).all()
    if request.method == "POST":
        if 'username' in session:
            # username = session['username']
            all_users_draft = Draft.query.order_by(Draft.title).all()
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


@views.route('/post/<name>', methods=['POST', 'GET'])
def post(name):
    article = Note.query.filter_by(title = name).first()    
    return render_template('post.html', 
    article = article)

@views.route('/user/<login>', methods=['POST', 'GET'])
def user_page(login):
    user_login = User.query.filter_by(login = login).first()    
    return render_template('user_page.html', 
    user_login = user_login)

@views.route('<login>/draft', methods=['POST', 'GET'])
@login_required
def user_draft(login):
    draft_author = User.query.filter_by(login = login).first()
    # post_draft_title = Draft.query.filter_by(title = title).first()
    draft_title = request.form.get('title')
    draft_data = request.form.get('note')
    draft_tag = request.form.get('tag')
    valid_common_title = Note.query.filter_by(title = draft_title).first()
    valid_common_tag = Note.query.filter_by(tag = draft_title).first()
    valid_draft_title = Draft.query.filter_by(title = draft_title).first()
    valid_draft_tag = Draft.query.filter_by(tag = draft_tag).first()
    # if valid_draft_title or valid_common_title:
    #     flash('Wrong title', category='error')
    # elif valid_draft_tag or valid_common_tag:
    #     flash('Wrong tag', category='error')
    # else:
    draft_post = Draft(
        title = draft_title,
        data = draft_data,
        tag = draft_tag,
        user_login = current_user.login)
    db.session.add(draft_post)
    db.session.commit()
    return render_template('draft.html',
    draft_author = draft_author,
    current_user = current_user)

@views.route('/delete_note', methods=['POST', 'GET'])
def delete_note():
    # user = User.query.filter_by(login = current_user.login).first()
    note = Note.query.filter_by(user_login = current_user.login).first()
    if note:
        if note.user_login == current_user.login:
            db.session.delete(note)
            db.session.commit()
            return redirect(url_for('views.home'))
    else:
        flash('you are not author of this note', category='error')
        return redirect(url_for('views.home'))

