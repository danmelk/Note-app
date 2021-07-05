from operator import pos
import re
from types import MethodDescriptorType
from web.auth import login
from . import db
from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from flask import Blueprint, render_template, flash
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import login_required, current_user
from .models import Note, User

views = Blueprint('views', __name__)

@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == "POST":
        if 'username' in session:
            # username = session['username']
            users_login = User.query.order_by(User.login).all()
            note_title = request.form.get('title')
            note_data = request.form.get('note')
            note_tag = request.form.get('tag')
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

# @views.route('/laboratory/<int:id>', methods=['POST', 'GET'])
# def laboratory(id):
#     # post_title = Note.query.filter_by
#     post_id = id
#     post_data = Note.query.get(post_id)
#     return render_template('post.html', post_data = post_data)
#     # post_title = 
#     # post_data = 
