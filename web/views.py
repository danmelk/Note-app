import re
from types import MethodDescriptorType
from . import db
from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from flask import Blueprint, render_template, flash
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import login_required, current_user
from .models import Note


views = Blueprint('views', __name__)



@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == "POST":
        if 'username' in session:
            # username = session['username']
            note_data = request.form.get('note')
            note_entrance = Note(data = note_data, user_id = current_user.id)
            db.session.add(note_entrance)
            db.session.commit()
            return render_template('home.html', user = current_user)
        else:
            flash('Please login first ', category='error')
            return redirect(url_for('auth.login'))
    else:
        return render_template('home.html', user=current_user)