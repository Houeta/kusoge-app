import psycopg2, jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, request
from os import getenv, environ

app = Flask(__name__)

def _get_db_connection():
    conn = psycopg2.connect(
        host=getenv('PG_HOST'),
        database=getenv('PG_DB_NAME'),
        user = getenv('PG_USER'),
        password=getenv('PG_PASSWORD'),
        port=5432
    )
    return conn

def _create_jwt(username, secret, auth):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
            "iat": datetime.now(tz=timezone.utc),
            "admin": auth
        },
        secret
    )
    
@app.route('/login', methods=['POST'])
def login():
    auth_table = getenv('PG_AUTH_TABLE')
    auth = request.authorization
    if not auth or not auth.username or not auth.password: 
        return "Couldn't verify! You have empty fields.", 401
    
    conn = _get_db_connection()
    cursor = conn.cursor()
    query = f'SELECT email, password FROM {auth_table} WHERE email = %s'
    result = cursor.execute(query, (auth.username,))
    
    if result is None:
        user_credentials = cursor.fetchone()
        email = user_credentials[0]
        password = user_credentials[1]
        
        if auth.username != email or auth.password != password:
            return "Couldn't verify. Incorrect email or password", 402
        else:
            return _create_jwt(auth.username, environ['JWT_SECRET'], True)
    else:
        return "Couldn't verify", 403 
    
@app.route('/signup', methods=['POST'])
def signup():
    auth = request.authorization
    if not auth or not auth.username or not auth.password: 
        return "Couldn't verify! You have empty fields.", 401
    
    conn = _get_db_connection()
    cursor = conn.cursor()
    query = f'INSERT INTO {getenv('PG_AUTH_TABLE')} (email, name, password) VALUES %s'
    result = cursor.execute(query, (auth.username, auth.name, auth.password))
    if result is None:
        return f"Welcome, {auth.name}"
    
    
@app.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']
    
    if not encoded_jwt:
        return "Unathorized", 401
    
    encoded_jwt = encoded_jwt.split(' ')[1]
    try:
        decoded_jwt = jwt.decode(encoded_jwt, environ['JWT_SECRET'], algorithms=["HS256"])
    except:
        return "Unathorized", 401
    
    return decoded_jwt, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)