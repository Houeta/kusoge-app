from flask import Flask, render_template, request

import auth

app = Flask(__name__, template_folder='html-tpl')

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Function for profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Function for login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
     token, err = auth.login(request)
     
     if not err:
         return token
     else:
         return err

# Function for register page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Logout page
@app.route('/logout')
def logout():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=8080)