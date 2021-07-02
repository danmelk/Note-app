# from flask import Flask, session, redirect, url_for, render_template, request
# app = Flask(__name__)
# app.secret_key = 'your secret key'

# @app.route("/", methods=['POST', 'GET'])
# def index():
#     if 'login' in session:
#         login = session.get('login')
#         return render_template('index.html', login = login)
#     else:
#         return redirect(url_for('login'))

# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         session['login'] = request.form['login']
#         return redirect(url_for('index'))

# @app.route('/logout')
# def logout():
#     session.pop('login', None)
#     return redirect(url_for('login'))

    # if request.method == 'POST':
    #     if 'username' in session:
    #         return redirect(url_for('views.home'))
    #     else:
    #         username = request.form['username']
    #         session['username'] = username
    #         return render_template('login.html')
    #     return redirect(url_for('views.home'))
    # else:
    #     # if 'username' in session:
    #     #     return redirect(url_for('views.home'))
    #     return render_template('login.html')



    # if request.method == 'POST':
    #     username = request.form['username']
    #     session['username'] = username
    #     return redirect(url_for('views.home'))
    # else:
    #     return render_template('login.html')






# <ul> class="list-group list-group-flush" id='notes'
#   {% for note in user.notes %} 
#   {{ note.data }}
#   {% endfor %}
# </ul> 