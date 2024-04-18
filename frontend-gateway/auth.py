import os, requests

AUTH_SVC = os.getenv('AUTH_SVC') # user-service

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basic_auth = (auth.username, auth.password)
    
    response = requests.post(
        f"http://{AUTH_SVC}/login", auth=basic_auth
    )
    
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)