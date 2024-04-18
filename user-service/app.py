import psycopg2, jwt
from datetime import datetime, timezone, timedelta
from flask import Flask, request
from os import getenv, environ

app = Flask(__name__)

  #     PG_HOST: postgres
  #     PG_DB_NAME: KUSOGE_SHOP
  #     PG_USER: kusoge
  #     PG_PASSWORD: example
  #     PG_AUTH_TABLE: auth_user

def _get_db_connection():
    conn = psycopg2.connect(
        host=getenv('PG_HOST', '127.0.0.1'),
        database=getenv('PG_DB_NAME', 'KUSOGE_SHOP'),
        user = getenv('PG_USER', 'kusoge'),
        password=getenv('PG_PASSWORD', 'example'),
        port=5432
    )
    return conn
    
@app.route('/login', methods=['POST'])
def login():
    auth_table = getenv('PG_AUTH_TABLE', 'auth_user')
    auth = {
        'email': request.form.get('email'),
        'password': request.form.get('password')
    }
    if not auth or not auth['email'] or not auth['password']: 
        return "Couldn't verify! You have empty fields.", 401
    
    conn = _get_db_connection()
    cursor = conn.cursor()
    query = f'SELECT id, email, name, password FROM {auth_table} WHERE email = %s'
    result = cursor.execute(query, (auth['email'],))
    
    if result is None:
        user_credentials = cursor.fetchone()
        if user_credentials is None:
            return "Email address doesn't exist", 404
        
        if auth['email'] != user_credentials[1] or auth['password'] != user_credentials[3]:
            return "Couldn't verify. Incorrect email or password", 404
        else:
            result = f"{user_credentials[0]}:{user_credentials[2]}"
            return result, 200
    else:
        return "Couldn't verify. Incorrect email or password", 404
    
@app.route('/signup', methods=['POST'])
def signup():
    auth_table = getenv('PG_AUTH_TABLE', 'auth_user')
    data = {
        'email': request.form.get('email'),
        'name': request.form.get('name'),
        'password': request.form.get('password')
    }
    if not data or not data['email'] or not data['password'] or not data['name']: 
        return "Couldn't verify! You have empty fields.", 401
    
    conn = _get_db_connection()
    cursor = conn.cursor()
    query = f'INSERT INTO {auth_table}(email, name, password) VALUES(%s, %s, %s) RETURNING *'
    result = cursor.execute(query, (data['email'], data['name'], data['password']))
    conn.commit()
    if result is None:
        return f"Success", 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)