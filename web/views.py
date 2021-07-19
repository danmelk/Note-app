from logging import log
from operator import attrgetter, imatmul, irshift, pos
import json
import re
from types import MethodDescriptorType
from flask.wrappers import Response
import imghdr
from sqlalchemy import util
from sqlalchemy.orm import undefer
from sqlalchemy.sql.expression import all_
from web.auth import login
from . import create_app, db
from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from flask import Blueprint, config, render_template, flash, jsonify
from flask.globals import current_app, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from flask_login import login_required, current_user
from .models import Note, Tag, User, Image, Draft
import web
import pathlib


views = Blueprint('views', __name__)
home_bp = Blueprint('home_bp', __name__)


@views.route('/home', methods=['POST', 'GET'])
# @login_required
def home():
    users_login = User.query.order_by(User.login).all()
    if request.method == "POST":
        if 'username' in session:
            # username = session['username']
            note_title = request.form.get('title')
            note_data = request.form.get('note')
            unsorter_list_of_tags = request.form.get('tags')
            sorter_list_of_tags = (unsorter_list_of_tags.split(','))
            note_tag = sorter_list_of_tags
            # note_tag = request.form.get('tags')
            # return render_template('index.html', note_tag = note_tag)
            picture = request.files.getlist('picture')

            valid_title = Note.query.filter_by(title = note_title).first()
            if valid_title:
                flash('Wrong title', category='error')
            elif len(note_data) < 1:
                flash('Write something!', category='error')
            else:
                note_entrance = Note(
                title =  note_title,
                data = note_data, 
                user_login = current_user.login)

                db.session.add(note_entrance)
                db.session.commit()

                if picture:
                    for each_picture in picture:
                        filename = secure_filename(each_picture.filename)

                        mimetype = each_picture.mimetype
                        note_image = Image(
                            img = each_picture.read(),
                            mimetype = mimetype,
                            note_image = note_title,
                            name = filename)

                        db.session.add(note_image)
                        db.session.commit()
                
                if note_tag:
                    for each_tag in note_tag:
                        insert_to_db = Tag(
                            tag_name = each_tag,
                            note_tag = note_title)
                        
                        db.session.add(insert_to_db)
                        db.session.commit()


        else:
            flash('Please login first ', category='error')
            return redirect(url_for('auth.login'))

    return render_template('home.html',
    users_login = users_login,
    current_user = current_user)

@views.route('/home/image/<name>')
def get_image(name):
    image = Image.query.filter_by(name = name).first()
    return Response (image.img, mimetype=image.mimetype)

@views.route('/home/<post>')
def post(post):
    global article
    article = Note.query.filter_by(title = post).first()  
    image = Image.query.filter_by(note_image = post).all()
    tags = Tag.query.filter_by(note_tag = post).all()
    if article:
        if len(image) > 0:
            return render_template('post.html', 
            tags = tags,
            image = image,
            article = article)
        elif len(image) < 0:
            return render_template('post.html', 
            tags = tags,
            article = article)


    else:
        return 'this post does not exists'

@views.route('/tags/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(tag_name = tag_name).all()
    title = tag_name
    if tag:
        return render_template('tag.html',
        title = title,
        tag = tag)
    else:
        return 'there is no association with this tag'

@views.route('/user/<login>', methods=['POST', 'GET'])
def user_page(login):
    user_login = User.query.filter_by(login = login).first()
    if user_login:    
        return render_template('user_page.html', 
        user_login = user_login)
    else:
        return 'this user does not exists. '

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
    if valid_draft_title or valid_common_title:
        flash('Wrong title: already used', category='error')
    elif valid_draft_tag or valid_common_tag:
        flash('Wrong tag: already used', category='error')
    else:
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

@views.route('/delete_note/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_note(id):
    # user = User.query.filter_by(login = current_user.login).first()
    note_id = Note.query.filter_by(id = id).first()
    note_image_dependencies = Image.query.filter_by(note_image = note_id.title).all()
    note_tag_dependencies = Tag.query.filter_by(note_tag = note_id.title).all()
    if note_id:
        if note_id.user_login == current_user.login:
            for single_image in note_image_dependencies:
                db.session.delete(single_image)
                db.session.commit()
            for single_tag in note_tag_dependencies:
                db.session.delete(single_tag)
                db.session.commit()
            db.session.delete(note_id)
            db.session.commit()
            return redirect(url_for('views.home'))
        else: 
            flash('you are not author of this note', category='error')
            return redirect(url_for('views.home'))
    else:
        flash('you are not author of this note', category='error')
        return redirect(url_for('views.home'))

@views.route('/update_note/<int:id>', methods=['POST', 'GET'])
@login_required
def update_note(id):
    note_id = Note.query.filter_by(id = id).first()
    if note_id:
        if note_id.user_login == current_user.login:
            filter_by_id = Note.query.filter_by(id = note_id.id).first()
            unedited_note = filter_by_id.data
            edited_note = request.form.get('upd_note')
            unedited_note = edited_note

            if unedited_note == None:
                return render_template('updated_post.html', 
                unedited_note = unedited_note, 
                edited_note = edited_note,
                article = article, 
                filter_by_id = filter_by_id)

            else:
                filter_by_id.data = unedited_note
                db.session.commit()
                flash('changes applied', category='success')
                return redirect(url_for('views.home'))
                # return render_template('updated_post.html', 
                # unedited_note = unedited_note, 
                # edited_note = edited_note,
                # article = article, 
                # filter_by_id = filter_by_id)

        else:
            return 'you are not author for doing this!'
    else:
        flash('you are not author of this note', category='error')
        return redirect(url_for('views.home'))
