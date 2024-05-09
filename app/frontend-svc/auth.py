import os, requests

# GLOBAL ENV
AUTH_SVC = os.getenv('AUTH_SVC')
AUTH_PORT = os.getenv('AUTH_PORT') # 5000

# Function to handle login
def login(request):
    # Gather credentials from the request form
    auth = {
        'email': request.form.get('email'),
        'password': request.form.get('password')
    }
    # If credentials are missing, return an error message with status code 401 (Unathorized)
    if not auth:
        return "missing credentials", 401
    
    # Make a POST request to the authentication service's login endpoint with the credentials
    response = requests.post(
        f"http://{AUTH_SVC}:{AUTH_PORT}/login", data=auth
    )
    
    # Return the response text and status code from the login request
    return response.text, response.status_code

# Function for handle signup
def signup(request):
    # Gather signup information from the request form
    auth = {
        'email': request.form.get('email'),
        'name': request.form.get('name'),
        'password': request.form.get('password'),
    }
    if not auth:
        return "missing credentials", 401
    
    response = requests.post(
        f"http://{AUTH_SVC}:{AUTH_PORT}/signup", data=auth
    )
    
    # Return the response text and status code from the signup request
    return response.text, response.status_code