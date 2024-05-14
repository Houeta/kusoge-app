import logging
from os import getenv

from flask import Flask, request
import psycopg2

logging.basicConfig(filename='app.log', level=logging.DEBUG)
# Initialize Flask application
app = Flask(__name__)

# Function to establish a connect with a PostrgeSQL database
def _get_db_connection():
    conn = psycopg2.connect( # Connect to the postgres db
        host=getenv('PG_HOST'),
        database=getenv('POSTGRES_DB'),
        user = getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        port=5432 # Default postgres port
    )
    return conn # return the db connection

@app.route('/')
def index():
    return "OK!", 200

# Rout to handle use rlogin (POST)
@app.route('/login', methods=['POST'])
def login():
    try:
        auth_table = getenv('PG_AUTH_TABLE')
        auth = {
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        if not auth or not auth['email'] or not auth['password']: 
            return "Couldn't verify! You have empty fields.", 401
        
        # Establish a connection to the DB and create a cursor for executing queries
        conn = _get_db_connection()
        cursor = conn.cursor()
        # Query to retrieve user data based on the provided email
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
            logging.error(f"Error. Check: {result}")
            return "Couldn't verify. Incorrect email or password", 404
    except Exception as e:
        logging.error(f"Error occurred in login: {e}")
        return "Internal Server Error", 500

# Route to handle user signup (POST)
@app.route('/signup', methods=['POST'])
def signup():
    try:
        auth_table = getenv('PG_AUTH_TABLE')
        data = {
            'email': request.form.get('email'),
            'name': request.form.get('name'),
            'password': request.form.get('password')
        }
        if not data or not data['email'] or not data['password'] or not data['name']: 
            return "Couldn't verify! You have empty fields.", 401
        
        # Establish a DB connection and create a cursor
        conn = _get_db_connection()
        cursor = conn.cursor()
        # Insert the new user into the auth table
        query = f'INSERT INTO {auth_table}(email, name, password) VALUES(%s, %s, %s) RETURNING *'
        result = cursor.execute(query, (data['email'], data['name'], data['password'])) # Execute query
        conn.commit() # Commit the transaction to make the changes persistent
        if result is None:
            return f"Success", 201 # Return status code 201 (Created) indicating a successful signup
        else:
            return "Something went wrong", 500  # Return a generic error response
    except Exception as e:
        logging.error(f"Error occurred in signup: {e}")
        return "Internal Server Error", 500

    
@app.route('/healthcheck')
def healthcheck():
    try:
        with _get_db_connection() as connection:
            connection.cursor().execute('SELECT 1')
        db_status, code = 'ok', 200
    except Exception as e:
        db_status, code = e, 500
    return db_status, code

# Start the Flask application when run as a script
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)