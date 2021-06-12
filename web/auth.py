from flask import Blueprint, render_template, request
from flask.helpers import flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return 'logout'

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        name_data = request.form.get('name')
        login_data = request.form.get('login')
        password_data = request.form.get('password')
        if len(login_data) < 4:
            flash('your login must be greater then 3 characters', category='error')
        elif len(password_data) < 6:
            flash('your password must be greater then 5 characters', category='error')
        else:
            flash('Account created successfully', category='success')
    return render_template('sign_up.html')