from logging import log
from re import L
from . import db
import re
from web.models import User
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.helpers import flash
from werkzeug.datastructures import cache_property

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('views.home'))
    else:
        return render_template('login.html')

@auth.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('You are logged out!', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('You are not logged in', category='error')
        return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        name_data = request.form.get('name')
        login_data = request.form.get('login')
        password_data = request.form.get('password')
        if len(name_data) < 2:
            flash('please enter your real name :)', category='error')
        elif len(login_data) < 4:
            flash('your login must be greater then 3 characters', category='error')
        elif len(password_data) < 6:
            flash('your password must be greater then 5 characters', category='error')
        else:
            new_user = User(name = name_data, login = login_data, password = password_data)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully, follow to login page to login', category='success')
            return(redirect(url_for('auth.login')))
    return render_template('sign_up.html')