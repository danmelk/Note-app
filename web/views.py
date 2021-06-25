import re
from types import MethodDescriptorType
from web.auth import login
from flask import Blueprint, render_template, flash
from flask.globals import request, session
from flask.helpers import url_for
from werkzeug.utils import redirect

views = Blueprint('views', __name__)

@views.route('/home', methods=['POST', 'GET'])
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username = username)
    else:
        flash('Please login first ', category='error')

        return redirect(url_for('auth.login'))


