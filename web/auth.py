from . import db
from web.models import User
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.helpers import flash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/')
def redirect_to_login():
    return redirect(url_for('views.home'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        user_login = request.form.get('username')
        user_password = request.form.get('password')
        valid_user = User.query.filter_by(login = user_login).first()
        if valid_user:
            if valid_user.password == user_password:
                flash('Logged in successfully!', category='success')
                login_user(valid_user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Login does not exist.', category='error')
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    if 'username' in session:
        session.pop('username')
        logout_user()
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

        user = User.query.filter_by(login=login_data).first()
        if user:
            flash('Login already exists.', category='error')
        elif len(name_data) < 2:
            flash('please enter your real name :)', category='error')
        elif len(login_data) < 4:
            flash('your login must be greater then 3 characters', category='error')
        elif len(password_data) < 6:
            flash('your password must be greater then 5 characters', category='error')
        else:
            get_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            new_user = User(name = name_data, login = login_data, password = password_data, ip_addr = get_ip)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully, follow to login page to login', category='success')
            return(redirect(url_for('auth.login')))
    return render_template('sign_up.html')