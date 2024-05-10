import os

# 3p modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_manager, LoginManager, login_required, logout_user, current_user
import requests

# my modules
from __init__ import User # Importing the User class
import auth # authentication module for login & signup

# Initialize the Flask
app = Flask(__name__, template_folder='html-tpl')
app.secret_key = "super secret key" # secret key for session management

# Initialize FLask-login
login_manager = LoginManager() # Create loginManager instance
login_manager.login_view = 'login' # set default login view
login_manager.init_app(app) # Attach loginManager

# ENV VARIABLES for production service host and port 
prod_svc_hostname = os.getenv('PROD_SVC_HOSTNAME') 
prod_svc_port = os.getenv('PROD_SVC_PORT')
prod_url = f"http://{prod_svc_hostname}:{prod_svc_port}"
AUTH_SVC = os.getenv('AUTH_SVC')
AUTH_PORT = os.getenv('AUTH_PORT')

# User loader for Flask-login
@login_manager.user_loader
def load_user(id):
    return User(id) # Load user based on user ID
    
# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route for the product catalog (GET)
@app.route("/catalog")
def catalog():
    # Retrieve product info from a remote service
    products = requests.get(f"{prod_url}/products")
    print(products, products.json)
    return render_template('catalog.html', products=products.json())

# Route for adding a new product (POST)
@app.route('/catalog', methods=['POST'])
@login_required # Requires user to be logged in
def catalog_post():
    requests.post(f'{prod_url}/products', data=request.form)
    return redirect(url_for('catalog')) # Redireect back to the catalog page

# Route for updating a product (PUT)
@app.route('/catalog/<int:product_id>', methods=['POST'])
@login_required
def catalog_put(product_id):
    requests.put(url=f"{prod_url}/products/{product_id}", data=request.form )
    return redirect(url_for('catalog'))

# Route for deleting a product (DELETE)
@app.route('/catalog/delete/<int:product_id>', methods=['POST'])
@login_required
def catalog_delete(product_id):
    requests.delete(url=f"{prod_url}/products/{product_id}")
    return redirect(url_for('catalog'))

# Route for the profile page (only for logged-in users)
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# Route for the login page (GET)
@app.route('/login')
def login():
    return render_template('login.html') # Render the login page

# Route for handling login request (POST)
@app.route('/login', methods=['POST'])
def login_post():
    # Check if 'remember me' option is selected
    remember = True if request.form.get('remember') else False
    # Using custom authentication logic imported from auth.py
    response_text, status_code = auth.login(request)
    if status_code == 200:
        print(response_text)
        user = User(response_text.split(':')[0], name=response_text.split(':')[1]) # Extract data
        login_user(user, remember=remember) # Log the user in
        return redirect(url_for('profile'))
    elif 500 > status_code >= 400: # Client-side error during login
        flash(response_text) # Display an error message
        return redirect(url_for('login'))
    else:
        return response_text, status_code # Return th error response

# Route for the register page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route for the register page (POST)
@app.route('/signup', methods=['POST'])
def signup_post():
    text, status_code =  auth.signup(request) # perform signup
    if status_code == 201: # Redirect to login after successsful login
        return redirect(url_for('login'))
    elif 500 > status_code >= 400: # client-side err
        flash(text) # Error message
        return redirect(url_for('signup')) # return to signup page
    else:
        return text, status_code # Return the error response

# Route to order (service planned on future)
@app.route('/order', methods=['POST'])
def order():
    pass

# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user() # Log the user out 
    return redirect(url_for('index'))

# Function to perform dependency status check
def check_dependency(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Route for the healthcheck
@app.route('/healthcheck')
def healthcheck():
    auth_status = check_dependency(f"http://{AUTH_SVC}:{AUTH_PORT}")
    catalog_status = check_dependency(prod_url)
    
    if auth_status and catalog_status:
        return "Server is up and running", 200
    else:
        return "Server is experiencing issues", 500
    

# STart the Flask when run as a script
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=8080)