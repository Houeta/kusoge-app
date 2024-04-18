import os, requests

AUTH_SVC = os.getenv('AUTH_SVC', 'localhost') # user-service
AUTH_PORT = os.getenv('AUTH_PORT', 5000) # 5000

def login(request):
    auth = {
        'email': request.form.get('email'),
        'password': request.form.get('password')
    }
    if not auth:
        return "missing credentials", 401
    #basic_auth = (auth['username'], auth['password'])
    
    response = requests.post(
        f"http://{AUTH_SVC}:{AUTH_PORT}/login", data=auth
    )
    

    return response.text, response.status_code

def signup(request):
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
    

    return response.text, response.status_code