from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_manager, LoginManager, login_required, logout_user, current_user
from __init__ import User

import auth

app = Flask(__name__, template_folder='html-tpl')
app.secret_key = "super secret key"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
    
@login_manager.user_loader
def load_user(id):
    return User(id)
# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Function for profile page
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# Function for login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    remember = True if request.form.get('remember') else False
    response_text, status_code = auth.login(request)
    if status_code == 200:
        print(response_text)
        user = User(response_text.split(':')[0], name=response_text.split(':')[1])
        login_user(user, remember=remember)
        return redirect(url_for('profile'))
    elif 500 > status_code >= 400:
        flash(response_text)
        return redirect(url_for('login'))
    else:
        return response_text, status_code

# Function for register page
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    text, status_code =  auth.signup(request)
    if status_code == 201:
        return redirect(url_for('login'))
    elif 500 > status_code >= 400:
        flash(text)
        return redirect(url_for('signup'))
    else:
        return text, status_code

# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=8080)